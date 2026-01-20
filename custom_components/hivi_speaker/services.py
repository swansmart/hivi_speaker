from homeassistant.core import HomeAssistant
import voluptuous as vol
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_services(hass: HomeAssistant):
    """设置服务"""

    async def async_handle_refresh(call):
        """处理刷新服务"""
        # for entry_id, device_manager in hass.data[DOMAIN].items():
        #     await device_manager.refresh_discovery()

        if DOMAIN not in hass.data:
            _LOGGER.warning(f"{DOMAIN} 未初始化")
            return

        for entry_id, domain_data in hass.data[DOMAIN].items():
            if "device_manager" in domain_data:
                device_manager = domain_data["device_manager"]
                await device_manager.refresh_discovery()
                _LOGGER.debug(f"refresh discovery is called")

    async def async_handle_postpone_discovery(call):
        """处理延迟服务"""

        if DOMAIN not in hass.data:
            _LOGGER.warning(f"{DOMAIN} 未初始化")
            return

        for entry_id, domain_data in hass.data[DOMAIN].items():
            if "device_manager" in domain_data:
                device_manager = domain_data["device_manager"]
                await device_manager.postpone_discovery()
                _LOGGER.debug(f"postpone discovery is called")

    async def async_handle_remove_device(call):
        """处理删除设备服务"""
        speaker_device_id = call.data["speaker_device_id"]

        if DOMAIN not in hass.data:
            _LOGGER.warning(f"{DOMAIN} 未初始化")
            return

        for entry_id, domain_data in hass.data[DOMAIN].items():
            if "device_manager" in domain_data:
                device_manager = domain_data["device_manager"]
                success = await device_manager.remove_device(speaker_device_id)
                if success:
                    _LOGGER.debug("remove device %s is called", speaker_device_id)
                    break

    hass.services.async_register(
        DOMAIN, "refresh_discovery", async_handle_refresh, schema=vol.Schema({})
    )

    hass.services.async_register(
        DOMAIN,
        "postpone_discovery",
        async_handle_postpone_discovery,
        schema=vol.Schema({}),
    )

    hass.services.async_register(
        DOMAIN,
        "remove_device",
        async_handle_remove_device,
        schema=vol.Schema(
            {
                vol.Required("speaker_device_id"): str,
            }
        ),
    )
