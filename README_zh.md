# HiVi 音箱集成

[English](./README.md) | [简体中文](./README_zh.md)

一个用于无缝控制 HiVi 多房间音箱系统的 Home Assistant 自定义集成，实现全屋音频同步。

![multi_room](https://swan-smart-static-2.swanspeakers.com/pic1/multi_room_1.png)

## ✨ 功能特性

- **自动发现**：自动检测本地网络上的所有 HiVi 多房间音箱
- **多房间同步**：选择多个音箱进行全屋同步播放
- **无缝控制**：通过 Home Assistant 界面轻松控制所有 HiVi 音箱
- **配置流程**：用户友好的设置向导
- **实体管理**：为每个音箱创建媒体播放器实体，支持播放/暂停/音量控制
- **支持型号**：兼容 HiVi M5A、M3AMKIII、H6、H8、H5MKII、M500、M300MKII、M200MKII(WiFi)、M200D、M100MKIII、M80W、MT1-MAX、MT1-MINI、T200MKII、MS2 系列
- **兼容性**：适用于所有支持多房间功能的 HiVi 音箱

## 📦 安装方法

### 方法 1：HACS（推荐）

1. 在 Home Assistant 实例中打开 HACS
2. 点击"集成"
3. 点击右上角的三个点
4. 选择"自定义仓库"
5. 添加仓库 URL：`https://github.com/swansmart/hivi_speaker`
6. 将类别设置为"集成"
7. 点击"添加"
8. 在集成列表中搜索"HiVi Speaker"
9. 点击"安装"
10. 重启 Home Assistant

### 方法 2：手动安装

1. 下载最新版本 https://github.com/swansmart/hivi_speaker/releases
2. 将 `custom_components/hivi_speaker` 文件夹复制到 Home Assistant 配置目录
3. 重启 Home Assistant
4. 转到 **设置** > **设备与服务**
5. 点击 **+ 添加集成**
6. 搜索"HiVi Speaker"

## ⚙️ 配置

### 初始设置

1. 重启 Home Assistant 后，导航到 **设置** > **设备与服务**
2. 点击右下角的 **+ 添加集成**
3. 搜索并选择 **HiVi Speaker**
4. 集成将自动扫描网络中的 HiVi 音箱
5. 按照配置向导完成设置

### 自动发现

集成会自动扫描本地网络中可用的 HiVi 多房间音箱。发现的设备将显示在集成页面中。

## 🎵 使用方法

### 基本控制

集成为每个发现的 HiVi 音箱创建一个媒体播放器实体。您可以通过以下方式控制它们：

- **播放/暂停**：控制单个音箱的播放
- **音量控制**：独立调节每个音箱的音量
- **媒体选择**：选择并向连接的音箱播放不同的媒体文件
- **同步管理**：选择一个或多个其他音箱作为同步的"子"音箱进行多房间播放

### 多房间同步

**配置界面：**
Home Assistant 中的每个 HiVi 音箱设备都包含一个配置区域，您可以在其中管理同步设置。在此区域中，您将找到：

- 网络中所有其他可用 HiVi 音箱的开关列表
- 每个开关代表一个潜在的"子"音箱
- 将开关切换到 ON 以建立同步连接
- 将开关切换到 OFF 以断开同步

**如何设置同步：**

1. 导航到 Home Assistant 中的 HiVi 音箱设备
2. 展开配置部分
3. 您将看到一个开关列表，每个开关都标有另一个音箱的名称
4. 将要与当前音箱同步的音箱开关切换到 ON
5. 选定的音箱将立即成为当前"主"音箱的"子"音箱
6. 在主音箱上播放的任何媒体现在都将同步到所有连接的子音箱

**连接行为：**
- **开关为 ON 时**：建立实时连接，子音箱开始播放同步音频
- **开关为 OFF 时**：断开同步，子音箱返回独立模式
- **动态更改**：您可以随时添加或移除同步音箱而不会中断播放
- **多个主音箱**：每个音箱可以独立控制自己的子音箱组

**视觉示例：**
```
客厅音箱配置
├── [✓] 厨房音箱   ← 开关 ON（已同步）
├── [✓] 卧室音箱   ← 开关 ON（已同步）
├── [ ] 浴室音箱   ← 开关 OFF（未同步）
└── [ ] 书房音箱   ← 开关 OFF（未同步）
```

**优势：**
- **简单切换界面**：轻松的 ON/OFF 同步控制
- **实时连接**：切换时立即建立连接
- **独立控制**：每个音箱维护自己的同步配置
- **灵活设置**：为不同场景创建不同的同步组
- **无中断**：更改同步设置而不会中断正在进行的播放

**使用技巧：**
- 通过选择主客厅音箱并将所有其他音箱开关切换到 ON 来创建"全屋"组
- 对于聚会，设置主音箱与厨房和露台音箱同步
- 早上，同步卧室和浴室音箱用于晨间例行程序
- 根据一天中的时间或活动轻松更改配置

**重要提示：**
- 同步连接可以随时建立，无论主音箱是否正在播放媒体，您都可以设置同步关系
- 您可以同时拥有多个独立的同步组
- 所有同步音箱必须在同一本地网络上

## 🔧 故障排除

### 常见问题

**问：未找到音箱**
- 确保 HiVi 音箱已开机并与 Home Assistant 连接在同一本地网络上
- 检查防火墙设置以确保允许 mDNS（端口 5353/UDP）
- 重启 Home Assistant 和您的音箱
- 验证您的 HiVi 音箱是否支持多房间功能

**问：播放期间音箱不同步**
- 确保所有音箱都安装了最新固件
- 检检查网络延迟；建议优化网络连接以获得更好的同步效果
- 减少同步组中的音箱数量

**问：集成加载失败**
- 检查 Home Assistant 日志中的错误消息
- 验证所有文件是否已正确安装在 `custom_components` 目录中
- 尝试重新安装集成
- 确保您使用的是受支持的 Home Assistant 版本

**问：音箱频繁断开连接**
- 检查 Wi-Fi 信号强度
- 确保您的路由器能够处理连接的设备数量
- 考虑为您的音箱分配静态 IP 地址
- 更新您的路由器固件

### 启用调试日志

将以下内容添加到您的 `configuration.yaml` 以获取详细日志：

```yaml
# configuration.yaml
logger:
  default: warning
  logs:
    custom_components.hivi_speaker: debug
```

添加此配置后，重启 Home Assistant 并检查日志以获取详细信息。

## 📱 支持的设备

- 所有支持多房间功能的 HiVi 音箱
- 支持 mDNS 发现的 HiVi 音频设备

## 🐛 问题报告

如果您遇到任何问题或有功能建议：

1. 首先查看上面的 #常见问题 部分
2. 搜索现有问题 https://github.com/swansmart/hivi_speaker/issues 查看您的问题是否已被报告
3. 创建新问题并提供以下信息：
   - 问题的详细描述
   - 重现步骤
   - Home Assistant 版本
   - 集成版本
   - 日志（如果可能，请启用调试模式）
   - 音箱型号和固件版本

## 🤝 贡献

欢迎贡献！您可以通过以下方式帮助：

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

### 开发设置

```bash
# 克隆仓库
git clone https://github.com/swansmart/hivi_speaker.git

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows 上：venv\Scripts\activate

```

## 📄 许可证

详情请见 [LICENSE](LICENSE) 文件。

## 📞 支持

- **文档**：https://github.com/swansmart/hivi_speaker
- **问题跟踪器**：https://github.com/swansmart/hivi_speaker/issues
- **变更日志**：参见 CHANGELOG.md
- **讨论**：访问我们的 https://github.com/swansmart/hivi_speaker/discussions

## 版本历史

- **0.1.0** (2024-01-20)
  - 初始发布
  - 自动发现 HiVi 多房间音箱
  - 基本播放控制（播放、暂停、音量）
  - 多房间同步支持
  - 配置流程实现
  - 为每个音箱创建媒体播放器实体

---

**注意**：在使用此集成之前，请确保您的 HiVi 音箱已启用多房间功能并连接到您的网络。为获得最佳性能，我们建议使用稳定的网络连接并保持音箱固件更新。
