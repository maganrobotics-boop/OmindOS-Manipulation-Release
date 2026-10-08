# OmindOS Manipulation 客户发行版

本仓库提供 OmindOS 机械臂与移动双臂工作台的编译发行包、使用说明及校验记录。

## 当前版本

[0.2.0-preview.4 发行页](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/tag/v0.2.0-preview.4)

- Windows x64：完整解压后双击 `OmindOS-Workbench.exe`。
- Linux x64（Ubuntu 22.04 或更新兼容系统）：完整解压后执行 `./OmindOS-Workbench`。
- 无需另装 Python、ROS、Node.js 或 Docker；程序使用本机浏览器界面，默认地址 `http://127.0.0.1:8085/`。

提供三维参数配置、参数版本保存与导入导出、十五个主体关节 ±0.1° 点动、单臂/双臂/主体关节正弦预览、底盘参考运动预览、左右机械臂/腰部/底盘通信配置和软件急停联锁。

**本版是真机驱动尚未接通的预览版。通信设置只保存配置，不建立设备连接或发送真机指令；软件急停不能代替硬件急停。** 当前是运动学与静态重力预览，未包含碰撞、接触或平衡验证。

后端业务源码不随包提供；浏览器资源、模型参数和第三方许可说明保留。Windows 包暂未签名。

请从发行页下载与操作系统对应的完整安装包和 `SHA256SUMS`。GitHub 自动生成的 Source code 压缩包仅是发行仓库快照，不是安装包。
