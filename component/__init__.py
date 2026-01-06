"""The HiVi Speaker integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import (
    ConfigEntryError,
    ConfigEntryAuthFailed,
    ConfigEntryNotReady,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
_PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR]

# TODO Create ConfigEntry type alias with API object
# Alias name should be prefixed by integration name
# type New_NameConfigEntry = ConfigEntry[MyApi]  # noqa: F821


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HiVi Speaker from a config entry."""

    try:
        # TODO 1. Create API instance
        # TODO 2. Validate the API connection (and authentication)
        # TODO 3. Store an API object for your platforms to access
        entry.runtime_data = None

        # await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

        # 注册一个简单的服务，用于 Add Group
        async def handle_add_group(call):
            """处理添加分组"""
            group_name = call.data.get("name", "新分组")
            _LOGGER.info(f"🎯 添加分组: {group_name}")

            # 发送事件通知前端
            hass.bus.async_fire(
                f"{DOMAIN}_group_added",
                {"name": group_name, "entry_id": entry.entry_id},
            )

        hass.services.async_register(DOMAIN, "add_group", handle_add_group)

        return True
    except Exception as err:  # pylint: disable=broad-except
        raise ConfigEntryError(f"Unexpected error: {err}")


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)

    # 清理服务
    if hass.services.has_service(DOMAIN, "add_group"):
        hass.services.async_remove(DOMAIN, "add_group")

    return True
