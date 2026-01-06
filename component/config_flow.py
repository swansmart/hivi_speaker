"""Config flow for the HiVi Speaker integration."""

import voluptuous as vol

import ipaddress

from homeassistant import config_entries

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import callback

from .const import DOMAIN


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HiVi Speaker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input.get(CONF_HOST)
            port = user_input.get(CONF_PORT)

            if not host or not port:
                errors["base"] = "missing_host_port"
            else:
                # 2. 检查IP地址格式
                try:
                    ipaddress.ip_address(host)  # 需要导入 ipaddress
                except ValueError:
                    errors["host"] = "invalid_ip_address"

                # 3. 检查端口范围
                try:
                    port_num = int(port)
                    if not (1 <= port_num <= 65535):
                        errors["port"] = "invalid_port"
                except ValueError:
                    errors["port"] = "invalid_port"

                # 4. 如果没有错误，检查是否重复
                if not errors:
                    # use host:port as unique_id
                    unique_id = f"{host}:{port}"
                    await self.async_set_unique_id(unique_id)
                    self._abort_if_unique_id_configured()

            if not errors:
                return self.async_create_entry(
                    title=f"HiVi Speaker {unique_id}",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default=""): str,
                    vol.Required(CONF_PORT, default=8092): int,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """返回选项流 - 添加 Add Group 选项"""
        return HiViSpeakerOptionsFlow(config_entry)


class HiViSpeakerOptionsFlow(config_entries.OptionsFlow):
    """选项流 - 支持多个分支"""

    def __init__(self, config_entry):
        """初始化"""
        self.config_entry = config_entry
        self._action = ""  # 存储用户选择的操作
        self._group_name = ""

    async def async_step_init(self, user_input=None):
        """第一步：显示操作选择菜单"""
        if user_input is not None:
            # 用户选择了操作类型
            self._action = user_input["action"]

            # 根据选择进入不同分支
            if self._action == "add_sync_group":
                return await self.async_step_add_sync_group()
            elif self._action == "remove_sync_group":
                return await self.async_step_remove_sync_group()
            elif self._action == "manage_groups":
                return await self.async_step_manage_groups()

        # 显示操作选择菜单
        return self.async_show_menu(
            step_id="init",
            menu_options={
                "add_sync_group": "添加同步组",
                "remove_sync_group": "删除同步组",
                "manage_groups": "管理分组",
            },
            description_placeholders={"device": self.config_entry.title},
        )

    async def async_step_add_sync_group(self, user_input=None):
        """添加同步组"""
        errors = {}

        if user_input is not None:
            group_name = user_input.get("group_name", "").strip()
            auto_sync = user_input.get("auto_sync", True)

            if not group_name:
                errors["group_name"] = "组名不能为空"
            else:
                # 调用添加同步组服务
                await self.hass.services.async_call(
                    DOMAIN,
                    "add_sync_group",
                    {
                        "name": group_name,
                        "auto_sync": auto_sync,
                        "entry_id": self.config_entry.entry_id,
                    },
                )

                # 显示成功消息
                return self.async_show_form(
                    step_id="add_sync_group",
                    data_schema=vol.Schema({}),  # 空表单
                    description_placeholders={
                        "message": f"✅ 同步组 '{group_name}' 已添加！"
                    },
                )

        # 显示添加同步组表单
        return self.async_show_form(
            step_id="add_sync_group",
            data_schema=vol.Schema(
                {
                    vol.Required("group_name", default=""): str,
                    vol.Optional("auto_sync", default=True): bool,
                }
            ),
            errors=errors,
            description_placeholders={"device": self.config_entry.title},
        )

    async def async_step_remove_sync_group(self, user_input=None):
        """删除同步组"""
        errors = {}

        if user_input is not None:
            group_name = user_input.get("group_name", "").strip()

            if not group_name:
                errors["group_name"] = "请选择要删除的组"
            else:
                # 调用删除同步组服务
                await self.hass.services.async_call(
                    DOMAIN,
                    "remove_sync_group",
                    {"name": group_name, "entry_id": self.config_entry.entry_id},
                )

                # 显示成功消息
                return self.async_show_form(
                    step_id="remove_sync_group",
                    data_schema=vol.Schema({}),
                    description_placeholders={
                        "message": f"✅ 同步组 '{group_name}' 已删除！"
                    },
                )

        # 获取现有的分组列表（这里需要你实现获取分组的方法）
        existing_groups = ["客厅组", "卧室组", "厨房组"]  # 示例数据

        if not existing_groups:
            return self.async_show_form(
                step_id="remove_sync_group",
                data_schema=vol.Schema({}),
                description_placeholders={"message": "⚠️ 当前没有同步组可删除"},
            )

        # 显示删除同步组表单
        return self.async_show_form(
            step_id="remove_sync_group",
            data_schema=vol.Schema(
                {
                    vol.Required("group_name"): vol.In(
                        {group: group for group in existing_groups}
                    ),
                    vol.Optional("confirm", default=False): bool,
                }
            ),
            errors=errors,
            description_placeholders={
                "device": self.config_entry.title,
                "group_count": str(len(existing_groups)),
            },
        )

    async def async_step_manage_groups(self, user_input=None):
        """管理分组（更多选项）"""
        if user_input is not None:
            action = user_input.get("action")

            if action == "list_groups":
                # 列出所有分组
                await self.hass.services.async_call(
                    DOMAIN, "list_groups", {"entry_id": self.config_entry.entry_id}
                )
                message = "已列出所有分组，请查看日志"

            elif action == "sync_all":
                # 同步所有分组
                await self.hass.services.async_call(
                    DOMAIN, "sync_all_groups", {"entry_id": self.config_entry.entry_id}
                )
                message = "正在同步所有分组..."

            elif action == "back":
                # 返回主菜单
                return await self.async_step_init()

            # 显示操作结果
            return self.async_show_form(
                step_id="manage_groups",
                data_schema=vol.Schema({}),
                description_placeholders={"message": f"✅ {message}"},
            )

        # 显示管理分组菜单
        return self.async_show_form(
            step_id="manage_groups",
            data_schema=vol.Schema(
                {
                    vol.Required("action"): vol.In(
                        {
                            "list_groups": "列出所有分组",
                            "sync_all": "同步所有分组",
                            "back": "返回主菜单",
                        }
                    )
                }
            ),
            description_placeholders={"device": self.config_entry.title},
        )


class HiViSpeakerOptionsFlow_1(config_entries.OptionsFlow):
    """选项流 - 只有一个 Add Group 功能"""

    def __init__(self, config_entry):
        """初始化"""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """显示选项菜单"""
        # 直接显示 Add Group 表单
        return await self.async_step_add_group()

    async def async_step_add_group(self, user_input=None):
        """添加分组的表单"""
        errors = {}

        if user_input is not None:
            # 用户输入了组名
            group_name = user_input.get("group_name", "").strip()

            if not group_name:
                errors["group_name"] = "分组名称不能为空"
            else:
                # 调用 add_group 服务
                await self.hass.services.async_call(
                    DOMAIN, "add_group", {"name": group_name}
                )

                # 显示成功消息
                return self.async_show_form(
                    step_id="add_group",
                    data_schema=vol.Schema(
                        {
                            vol.Required("group_name", default=""): str,
                        }
                    ),
                    description=f"✅ 分组 '{group_name}' 已添加！",
                )

        # 显示表单
        return self.async_show_form(
            step_id="add_group",
            data_schema=vol.Schema(
                {
                    vol.Required("group_name", default=""): str,
                }
            ),
            errors=errors,
            description_placeholders={"entry_name": self.config_entry.title},
        )
