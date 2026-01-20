# hivico.py
"""
Hivico设备API客户端
一个轻量级的Hivico设备通信库
"""

import aiohttp
import asyncio
import logging
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import time

_LOGGER = logging.getLogger(__name__)


class HivicoError(Exception):
    """Base exception for Hivico library"""

    pass


class ConnectionError(HivicoError):
    """Connection error"""

    pass


class DeviceStatus(Enum):
    """Device status enumeration"""

    UNKNOWN = "unknown"
    ONLINE = "online"
    OFFLINE = "offline"
    GROUPED = "grouped"
    STANDALONE = "standalone"


@dataclass
class DeviceInfo:
    """Device information"""

    ip: str
    name: str = ""
    status: DeviceStatus = DeviceStatus.UNKNOWN
    volume: int = 0
    is_master: bool = False
    group_uuid: Optional[str] = None
    last_seen: float = 0.0

    def __post_init__(self):
        if not self.name:
            self.name = f"Device-{self.ip}"
        if self.last_seen == 0:
            self.last_seen = time.time()


class HivicoClient:
    """
    Hivico Client

    Usage example:
        # Asynchronous usage
        async with HivicoClient() as client:
            status = await client.get_device_status("192.168.1.100")

        # Synchronous usage
        client = HivicoClient()
        status = await client.get_device_status("192.168.1.100")
    """

    def __init__(
        self,
        timeout: int = 5,
        debug: bool = False,
        logger: Optional[logging.Logger] = None,
    ):
        """
        initialize HivicoClient

        Args:
            timeout: Request timeout (seconds)
            debug: Whether to enable debug mode
            logger: Custom logger
        """
        self.timeout = timeout
        self.debug = debug
        self._logger = logger or _LOGGER
        self._session: Optional[aiohttp.ClientSession] = None

        # 设备缓存
        self._devices: Dict[str, DeviceInfo] = {}

    async def __aenter__(self):
        """Asynchronous context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Asynchronous context manager exit"""
        await self.close()

    async def connect(self):
        """Create connection session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
            self._logger.debug("HivicoClient session created")

    async def close(self):
        """Close connection session"""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
            self._logger.debug("HivicoClient session closed")

    async def _make_request(
        self, url: str, method: str = "GET"
    ) -> Optional[Dict[str, Any]]:
        """
        common request method
        """
        if self.debug:
            self._logger.debug(f"Making {method} request to {url}")

        try:
            await self.connect()

            async with self._session.request(
                method=method.upper(), url=url
            ) as response:
                text = await response.text()

                if response.status == 200:
                    if text.lower().strip() == "ok":
                        return {"status": "ok"}

                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        return {"raw_response": text}
                else:
                    self._logger.error(
                        f"Request failed: status={response.status}, response={text}"
                    )
                    return None

        except aiohttp.ClientError as err:
            self._logger.error(f"Request error: url={url}, error={err}")
            return None
        except asyncio.TimeoutError:
            self._logger.error(f"Request timeout: url={url}")
            return None
        except Exception as err:
            self._logger.error(f"Unexpected error: {err}")
            return None

    async def get_device_status(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        get device status

        Args:
            ip: Device IP address

        Returns:
            Device status information dictionary, returns None on failure
        """
        url = f"http://{ip}/httpapi.asp?command=getStatusEx"
        result = await self._make_request(url)

        # Update device cache
        if result and ip in self._devices:
            self._devices[ip].last_seen = time.time()
            if result.get("status") == "online":
                self._devices[ip].status = DeviceStatus.ONLINE

        return result

    async def get_device_info(
        self, ip: str, force_refresh: bool = False
    ) -> Optional[DeviceInfo]:
        """
        get device information

        Args:
            ip: Device IP
            force_refresh: Whether to force refresh status

        Returns:
            DeviceInfo object, returns None on failure
        """
        # If device is not in cache or force refresh, get status
        if ip not in self._devices or force_refresh:
            status = await self.get_device_status(ip)
            if not status:
                return None

            device = DeviceInfo(
                ip=ip,
                name=status.get("name", f"Device-{ip}"),
                status=DeviceStatus.ONLINE
                if status.get("status") == "online"
                else DeviceStatus.OFFLINE,
                volume=status.get("volume", 0),
                is_master=status.get("group_info", {}).get("is_master", False),
                group_uuid=status.get("group_info", {}).get("uuid"),
            )

            self._devices[ip] = device
        else:
            device = self._devices[ip]

            # If device hasn't been updated for too long, auto-refresh
            if time.time() - device.last_seen > 60:  # 1分钟
                await self.get_device_status(ip)

        return device

    async def get_slave_devices(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        get slave devices

        Args:
            ip: 主Device IP address

        Returns:
            Slave device list information
        """
        url = f"http://{ip}/httpapi.asp?command=multiroom:getSlaveList"
        return await self._make_request(url)

    async def connect_slave_to_master(
        self,
        slave_ip: str,
        ssid: str,
        wifi_channel: int,
        auth: str,
        encry: str,
        psk: str,
        master_ip: str,
        uuid: str,
    ) -> Optional[Dict[str, Any]]:
        """
        connect slave device to master device
        """
        url = (
            f"http://{slave_ip}/httpapi.asp?"
            f"command=ConnectMasterAp:ssid={ssid}:ch={wifi_channel}:"
            f"auth={auth}:encry={encry}:pwd={psk}:chext=0:"
            f"JoinGroupMaster:eth{master_ip}:wifi{master_ip}:uuid{uuid}"
        )

        self._logger.info(f"Connecting slave {slave_ip} to master {master_ip}")
        return await self._make_request(url)

    async def disconnect_group(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        disconnect device from group
        """
        url = f"http://{ip}/httpapi.asp?command=multiroom:Ungroup"
        self._logger.info(f"Disconnecting group on {ip}")
        return await self._make_request(url)

    async def remove_slave_from_group(
        self, master_ip: str, slave_ip: str
    ) -> Optional[Dict[str, Any]]:
        """
        remove slave device from group
        """
        url = (
            f"http://{master_ip}/httpapi.asp?command=multiroom:SlaveKickout:{slave_ip}"
        )
        self._logger.info(f"Removing slave {slave_ip} from group on {master_ip}")
        return await self._make_request(url)

    async def get_group_info(self, master_ip: str) -> Dict[str, Any]:
        """
        get group information
        """
        master_info = await self.get_device_info(master_ip)
        slaves_data = await self.get_slave_devices(master_ip)

        slaves = []
        if slaves_data and "slaves" in slaves_data:
            slaves = slaves_data["slaves"]

        return {
            "master": master_info.__dict__ if master_info else None,
            "slaves": slaves,
            "group_uuid": master_info.group_uuid if master_info else None,
            "active": master_info is not None and master_info.group_uuid is not None,
        }

    async def set_volume(self, ip: str, volume: int) -> Optional[Dict[str, Any]]:
        """
        set device volume

        Args:
            ip: Device IP
            volume: Volume value (0-100)
        """
        if volume < 0 or volume > 100:
            self._logger.error(f"Volume {volume} out of range (0-100)")
            return None

        url = f"http://{ip}/httpapi.asp?command=setPlayerCmd:setVolume:{volume}"
        result = await self._make_request(url)

        # 更新缓存
        if result and ip in self._devices:
            self._devices[ip].volume = volume

        return result

    async def play(self, ip: str) -> Optional[Dict[str, Any]]:
        """Play"""
        url = f"http://{ip}/httpapi.asp?command=setPlayerCmd:play"
        return await self._make_request(url)

    async def pause(self, ip: str) -> Optional[Dict[str, Any]]:
        """Pause"""
        url = f"http://{ip}/httpapi.asp?command=setPlayerCmd:pause"
        return await self._make_request(url)

    async def stop(self, ip: str) -> Optional[Dict[str, Any]]:
        """Stop"""
        url = f"http://{ip}/httpapi.asp?command=setPlayerCmd:stop"
        return await self._make_request(url)

    async def next_track(self, ip: str) -> Optional[Dict[str, Any]]:
        """Next track"""
        url = f"http://{ip}/httpapi.asp?command=setPlayerCmd:next"
        return await self._make_request(url)

    async def previous_track(self, ip: str) -> Optional[Dict[str, Any]]:
        """Previous track"""
        url = f"http://{ip}/httpapi.asp?command=setPlayerCmd:prev"
        return await self._make_request(url)


# Synchronous wrapper (optional)
class HivicoClientSync:
    """Synchronous wrapper for HivicoClient, for non-async environments"""

    def __init__(self, *args, **kwargs):
        self._client = HivicoClient(*args, **kwargs)
        self._loop = asyncio.new_event_loop()

    def __enter__(self):
        self._loop.run_until_complete(self._client.connect())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._loop.run_until_complete(self._client.close())
        self._loop.close()

    def get_device_status(self, ip: str) -> Optional[Dict[str, Any]]:
        return self._loop.run_until_complete(self._client.get_device_status(ip))

    def get_device_info(
        self, ip: str, force_refresh: bool = False
    ) -> Optional[DeviceInfo]:
        return self._loop.run_until_complete(
            self._client.get_device_info(ip, force_refresh)
        )

    def get_slave_devices(self, ip: str) -> Optional[Dict[str, Any]]:
        return self._loop.run_until_complete(self._client.get_slave_devices(ip))

    def set_volume(self, ip: str, volume: int) -> Optional[Dict[str, Any]]:
        return self._loop.run_until_complete(self._client.set_volume(ip, volume))

    def play(self, ip: str) -> Optional[Dict[str, Any]]:
        return self._loop.run_until_complete(self._client.play(ip))

    def pause(self, ip: str) -> Optional[Dict[str, Any]]:
        return self._loop.run_until_complete(self._client.pause(ip))

    def stop(self, ip: str) -> Optional[Dict[str, Any]]:
        return self._loop.run_until_complete(self._client.stop(ip))


# utility function for device discovery
async def discover_devices(
    network: str = "192.168.1", timeout: float = 2.0
) -> List[DeviceInfo]:
    """
    simple device discovery on the local network

    Note: This is just a simple example, actual usage may require more complex network scanning
    """
    import asyncio
    from contextlib import suppress

    devices = []
    client = HivicoClient(timeout=2)

    # Scan first 20 IPs (example)
    tasks = []
    for i in range(1, 21):
        ip = f"{network}.{i}"
        tasks.append(client.get_device_info(ip))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, DeviceInfo):
            devices.append(result)

    await client.close()
    return devices
