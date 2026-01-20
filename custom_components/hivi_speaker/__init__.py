from .device import HIVIDevice
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .const import DOMAIN, DISCOVERY_UPDATED
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.device_registry import DeviceEntry
import logging

# from .media_player import async_update_media_player_entities
# from .switch import async_update_control_entities
from .device_manager import HIVIDeviceManager
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up the config entry"""

    # Create device manager
    device_manager = HIVIDeviceManager(hass, config_entry)
    await device_manager.async_setup()

    # Store to hass data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(config_entry.entry_id, {})
    hass.data[DOMAIN][config_entry.entry_id]["device_manager"] = device_manager

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(
        config_entry, ["media_player", "switch"]
    )

    # Register services
    await async_setup_services(hass)

    # # Listen for device updates
    # async def async_handle_discovery_update():
    #     """Handle device discovery update"""
    #     await async_update_entities(hass, config_entry)

    # async_dispatcher_connect(hass, DISCOVERY_UPDATED, async_handle_discovery_update)

    return True


async def async_update_entities(hass: HomeAssistant, config_entry: ConfigEntry):
    """Update all entities"""
    device_manager = hass.data[DOMAIN][config_entry.entry_id]
    registry = device_manager.registry

    # Update media_player entities
    # await async_update_media_player_entities(hass, config_entry, registry)

    # Update switch and button entities
    # await async_update_control_entities(hass, config_entry, registry)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload config entry and clean up related resources"""
    _LOGGER.debug("Starting to unload config entry %s", entry.entry_id)

    # Get stored data (may have been partially cleaned up)
    data = hass.data.get(DOMAIN, {}).get(entry.entry_id, {})

    # 1) Clean up device manager (cancel background tasks, etc.)
    device_manager = data.get("device_manager")
    if device_manager:
        try:
            await device_manager.async_cleanup()
        except Exception:  # noqa: BLE001
            _LOGGER.exception("Exception occurred while cleaning up device_manager")

    # 2) Standard platform unloading
    try:
        unload_ok = await hass.config_entries.async_unload_platforms(
            entry, ["media_player", "switch"]
        )
    except Exception:  # noqa: BLE001
        _LOGGER.exception("Failed to call async_unload_platforms")
        unload_ok = False

    # 3) Remove instances bound to this entry from entity_platform (prevent residue)
    if "entity_platform" in hass.data:
        platforms = hass.data["entity_platform"].get(DOMAIN, [])
        if platforms:
            filtered = [
                p
                for p in platforms
                if not getattr(getattr(p, "config_entry", None), "entry_id", None)
                == entry.entry_id
            ]
            hass.data["entity_platform"][DOMAIN] = filtered

    # 4) Clean up devices in device registry belonging to this config entry
    try:
        dev_reg = async_get_device_registry(hass)
        for device in list(dev_reg.devices.values()):
            # Compatible with old and new attributes: prioritize config_entries (list), otherwise use single config_entry_id
            config_entries = getattr(device, "config_entries", None)
            if config_entries:
                if entry.entry_id in config_entries:
                    dev_reg.async_remove_device(device.id)
            else:
                if getattr(device, "config_entry_id", None) == entry.entry_id:
                    dev_reg.async_remove_device(device.id)
    except Exception:  # noqa: BLE001
        _LOGGER.exception("Exception occurred while cleaning up device registry")

    # 5) Clean up this extension's entry from hass.data
    try:
        if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            if not hass.data[DOMAIN]:
                hass.data.pop(DOMAIN, None)
    except Exception:  # noqa: BLE001
        _LOGGER.exception("Exception occurred while cleaning up hass.data")

    if not unload_ok:
        _LOGGER.error(
            "Platform unloading partially failed (unload_ok=False), there may be residual entities or platforms"
        )
    else:
        _LOGGER.debug("Config entry %s unloaded successfully", entry.entry_id)

    return unload_ok


def remove_platforms_by_entry_id(hass, entry_id):
    """Remove all platform instances with specified entry_id"""
    if "entity_platform" not in hass.data:
        return False

    platforms = hass.data["entity_platform"].get(DOMAIN, [])
    new_platforms = [
        p
        for p in platforms
        if not hasattr(p, "config_entry") or p.config_entry.entry_id != entry_id
    ]

    hass.data["entity_platform"][DOMAIN] = new_platforms
    return len(platforms) != len(new_platforms)


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device_entry: DeviceEntry
) -> bool:
    """Clean up associated devices when config entry is removed"""
    # Check if device belongs to current config entry (via device identifiers)
    # Your device identifier format: (DOMAIN, f"{config_entry.entry_id}_terminal_1")
    for identifier in device_entry.identifiers:
        if identifier[0] == DOMAIN and config_entry.entry_id in identifier[1]:
            # Allow deletion of this device
            return True
    return False  # Do not delete devices not belonging to current entry


async def async_remove_config_entry_device(hass, config_entry, device_entry):
    """Handle removal of a device from the UI/device registry.

    Return True to allow Home Assistant to remove the device entry.
    """
    try:
        device_manager = hass.data[DOMAIN][config_entry.entry_id]["device_manager"]
        if device_manager is None:
            _LOGGER.debug(
                "Device manager not found, allowing device deletion %s", device_entry.id
            )
            return False

        ha_device_id = device_entry.id

        speaker_device_id = None

        device_dict = (
            device_manager.device_data_registry.get_device_dict_by_ha_device_id(
                ha_device_id, default=None
            )
        )
        if device_dict is None:
            pass
        else:
            device_obj = HIVIDevice(**device_dict)
            speaker_device_id = device_obj.speaker_device_id

        await device_manager.async_remove_device_with_entities(ha_device_id)
        _LOGGER.debug(
            "Requested device manager to delete device %s and its entities",
            ha_device_id,
        )

        # remove switch/button/select entities associated with this device
        if speaker_device_id:
            await device_manager.remove_control_entities_by_speaker_device_id(
                speaker_device_id
            )
            _LOGGER.debug(
                "Requested device manager to delete control entities associated with speaker device ID %s",
                speaker_device_id,
            )

        return True

    except Exception as exc:
        # Catch all exceptions, log and allow deletion to avoid blocking user
        _LOGGER.exception(
            "Exception occurred in async_remove_config_entry_device, allowing deletion to avoid blocking: %s",
            exc,
        )
        return True
