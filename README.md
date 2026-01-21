# HiVi Speaker Integration

[English](./README.md) | [简体中文](./README_zh.md)

A Home Assistant custom integration for seamless control of HiVi Multi-Room speaker systems, enabling whole-home audio synchronization.

![multi_room](https://swan-smart-static-2.swanspeakers.com/pic1/multi_room_1.png)

## ✨ Features

- **Auto-Discovery**: Automatically detects all HiVi Multi-Room speakers on your local network
- **Multi-Room Sync**: Select multiple speakers for synchronized playback throughout your home
- **Seamless Control**: Easily control all HiVi speakers through the Home Assistant interface
- **Configuration Flow**: User-friendly setup wizard
- **Entity Management**: Creates media player entities for each speaker with play/pause/volume controls
- **Supported Models**: Compatible with HiVi M5A, M3AMKIII, H6, H8, H5MKII, M500, M300MKII, M200MKII(WiFi), M200D, M100MKIII, M80W, MT1-MAX, MT1-MINI, T200MKII, MS2 series
- **Compatibility**: Works with all HiVi speakers supporting Multi-Room functionality

## 📦 Installation

### Method 1: HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top-right corner
4. Select "Custom repositories"
5. Add the repository URL: `https://github.com/swansmart/hivi_speaker`
6. Set the category to "Integration"
7. Click "Add"
8. Search for "HiVi Speaker" in the integration list
9. Click "Install"
10. Restart Home Assistant

### Method 2: Manual Installation

1. Download the latest https://github.com/swansmart/hivi_speaker/releases
2. Copy the `custom_components/hivi_speaker` folder to your Home Assistant configuration directory
3. Restart Home Assistant
4. Go to **Settings** > **Devices & Services**
5. Click **+ Add Integration**
6. Search for "HiVi Speaker"

## ⚙️ Configuration

### Initial Setup

1. After restarting Home Assistant, navigate to **Settings** > **Devices & Services**
2. Click **+ Add Integration** in the bottom-right corner
3. Search for and select **HiVi Speaker**
4. The integration will automatically scan your network for HiVi speakers
5. Follow the configuration wizard to complete setup

### Automatic Discovery

The integration automatically scans your local network for available HiVi Multi-Room speakers. Discovered devices will appear in the integration page.

## 🎵 Usage

### Basic Controls

The integration creates a media player entity for each discovered HiVi speaker. You can control them through:

- **Play/Pause**: Control playback on individual speakers
- **Volume Control**: Adjust volume for each speaker independently
- **Media Selection**: Choose and play different media files to connected speakers
- **Sync Management**: Select one or more other speakers as synchronized "child" speakers for multi-room playback

### Multi-Room Synchronization

**Configuration Interface:**
Each HiVi speaker device in Home Assistant includes a configuration area where you can manage synchronization settings. In this area, you'll find:

- A switch list of all other available HiVi speakers in your network
- Each switch represents a potential "child" speaker
- Toggle the switch ON to establish a synchronization connection
- Toggle the switch OFF to disconnect the synchronization

**How to Set Up Synchronization:**

1. Navigate to the HiVi speaker device in Home Assistant
2. Expand the configuration section
3. You'll see a list of switches, each labeled with another speaker's name
4. Toggle ON the switches for speakers you want to synchronize with the current speaker
5. The selected speakers will immediately become "child" speakers of the current "master" speaker
6. Any media played on the master speaker will now synchronize to all connected child speakers

**Connection Behavior:**
- **When switch is ON**: Establishes a real-time connection, and the child speaker starts playing synchronized audio
- **When switch is OFF**: Disconnects the synchronization, and the child speaker returns to standalone mode
- **Dynamic Changes**: You can add or remove synchronized speakers at any time without interrupting playback
- **Multiple Masters**: Each speaker can independently control its own set of child speakers

**Visual Example:**
```
Living Room Speaker Configuration
├── [✓] Kitchen Speaker   ← Switch ON (synchronized)
├── [✓] Bedroom Speaker   ← Switch ON (synchronized)
├── [ ] Bathroom Speaker  ← Switch OFF (not synchronized)
└── [ ] Office Speaker    ← Switch OFF (not synchronized)
```

**Benefits:**
- **Simple Toggle Interface**: Easy ON/OFF control for synchronization
- **Real-time Connection**: Connections are established immediately when toggled
- **Independent Control**: Each speaker maintains its own sync configuration
- **Flexible Setup**: Create different sync groups for different scenarios
- **No Disruption**: Change sync settings without interrupting ongoing playback

**Usage Tips:**
- Create a "whole house" group by selecting the master living room speaker and toggling ON all other speakers
- For parties, set up the main speaker to sync with kitchen and patio speakers
- In the morning, synchronize bedroom and bathroom speakers for a morning routine
- Easily change configurations based on time of day or activity

**Important Notes:**
- Synchronization connections can be established at any time, regardless of playback status
- You can have multiple independent sync groups simultaneously
- All synchronized speakers must be on the same local network

## 🔧 Troubleshooting

### Common Issues

**Q: No speakers are found**
- Ensure HiVi speakers are powered on and connected to the same local network as Home Assistant
- Check firewall settings to ensure mDNS (port 5353/UDP) is allowed
- Restart both Home Assistant and your speakers
- Verify that your HiVi speakers support Multi-Room functionality

**Q: Speakers are out of sync during playback**
- Ensure all speakers have the latest firmware installed
- Check network latency; it is recommended to optimize network connection for better synchronization performance.
- Reduce the number of speakers in the synchronized group

**Q: Integration fails to load**
- Check the Home Assistant logs for error messages
- Verify all files are correctly installed in the `custom_components` directory
- Try reinstalling the integration
- Ensure you're using a supported Home Assistant version

**Q: Speakers disconnect frequently**
- Check Wi-Fi signal strength
- Ensure your router can handle the number of connected devices
- Consider assigning static IP addresses to your speakers
- Update your router's firmware

### Enabling Debug Logs

Add the following to your `configuration.yaml` for detailed logging:

```yaml
# configuration.yaml
logger:
  default: warning
  logs:
    custom_components.hivi_speaker: debug
```

After adding this configuration, restart Home Assistant and check the logs for detailed information.

## 📱 Supported Devices

- All HiVi speakers with Multi-Room functionality
- HiVi audio devices supporting mDNS discovery

## 🐛 Reporting Issues

If you encounter any problems or have feature suggestions:

1. First check the #common-issues section above
2. Search existing https://github.com/swansmart/hivi_speaker/issues to see if your problem has already been reported
3. Create a new issue with the following information:
   - Detailed description of the problem
   - Steps to reproduce
   - Home Assistant version
   - Integration version
   - Logs (with debug mode enabled if possible)
   - Speaker model and firmware version

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/swansmart/hivi_speaker.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

## 📄 License

Please see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: https://github.com/swansmart/hivi_speaker
- **Issue Tracker**: https://github.com/swansmart/hivi_speaker/issues
- **Changelog**: See CHANGELOG.md

## Version History

- **0.1.0** (2026-01-20)
  - Initial release
  - Automatic discovery of HiVi Multi-Room speakers
  - Basic playback controls (play, pause, volume)
  - Multi-room synchronization support
  - Configuration flow implementation
  - Media player entity creation for each speaker

---

**Note**: Before using this integration, ensure your HiVi speakers have Multi-Room functionality enabled and are connected to your network. For optimal performance, we recommend using a stable network connection and keeping your speakers' firmware up to date.
