# OmindOS Manipulation 客户发行版

本仓库提供机械臂与移动双臂工作台的编译发行包、使用说明、演示视频及校验记录。

## 当前版本

[0.2.0-preview.7 发行页](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/tag/v0.2.0-preview.7)

- **Windows x64**：下载 `omindos-workbench-0.2.0-preview.7-windows-x64.zip`，完整解压后双击 `OmindOS-Workbench.exe`。
- **Linux x64**（Ubuntu 22.04 或更新兼容系统）：下载 `omindos-workbench-0.2.0-preview.7-linux-x64.tar.gz`，完整解压后运行 `./OmindOS-Workbench`。
- 本机三维调参与运动学预览无需另装 Python、ROS、Node.js 或 Docker，浏览器默认地址为 `http://127.0.0.1:8085/`。
- 可选 ROS 2 联动需要独立启动本机预览服务，并使用同一配置目录。详见 [ROS 2 安装与联动说明](ROS2.zh-CN.md)。

## 本次界面更新

主要文字、输入框和按钮调整为 16px，说明文字不低于 14px；提高文字对比度，加宽两侧面板，并改善按钮间距与手机布局。已检查桌面、平板和手机宽度下的布局。

## 已合并功能

本版统一包含开发仓 PR #2 的双 RM75-B 七轴与二指夹爪、PR #3 的 ROS 2 预览界面和本机桥接，以及 PR #6 的通信配置；PR #11 补齐了桌面启动器的 `--runtime-url` 入口与打包验收。

支持三维参数配置、版本保存与导入导出、15 个主体关节 ±0.1° 点动、正弦预览、左右夹爪独立开合、底盘参考运动、设备通信配置和软件停止联锁。ROS 2 面板支持保存并加载、试运行、停止及姿态反馈。

[30 秒手爪演示视频](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/download/v0.2.0-preview.6/OmindOS-Manipulation-Gripper-Demo-30s.mp4)：细节特写、左右独立开合与双臂联动。视频沿用 preview.4 的同一模型，属于运动学演示。

## 安装、升级与核验

保留解压目录中的运行库和资源，不能只复制可执行文件。默认配置存储在用户目录的 `OmindOS/workbench-configurations`；升级解压不会删除旧配置，需要新版参考模型时重新加载并写入参数。

下载 `SHA256SUMS` 后核对压缩包：
- Windows PowerShell：`Get-FileHash .\omindos-workbench-0.2.0-preview.7-windows-x64.zip -Algorithm SHA256`，与校验文件比对。
- Linux：`sha256sum omindos-workbench-0.2.0-preview.7-linux-x64.tar.gz`，与校验文件比对。
- 解压后可运行 `OmindOS-Workbench.exe --verify`（Windows）或 `./OmindOS-Workbench --verify`（Linux）核对内部文件。

包内提供完整 `README.zh-CN.md`、`ROS2.zh-CN.md`、`MANIFEST.json`、`VALIDATION.json` 与第三方许可。GitHub 自动生成的 Source code 附件是发行仓库说明快照，不是安装包。

Windows 2022 / Ubuntu 22.04 原生构建各通过 45 项单元测试，打包前与重新解压后各通过 14 项可执行程序检查。本次桥接检查使用本机协议测试服务，没有重新进行真实 ROS 2/DDS 或真机验收。preview.6 的历史 ROS 2 验证记录保留在旧发行页；测试方式与边界见本版附件 `RELEASE_SUMMARY.json`。

## 预览范围

**真机驱动尚未接通，未通过真机验收。** 通信设置只保存配置，不建立设备连接或发送真机指令。ROS 2 服务仅做关节预览；`runtime_applied=true` 不代表真实设备已连接。软件停止联锁不能代替硬件急停。

当前为运动学与静态重力预览，未包含碰撞、接触、侧滑或平衡验证。Windows 原生 ROS 2 节点及 WSL 部署不在本次验收范围。后端业务源码不随包提供；浏览器资源、模型参数和第三方许可说明保留。Windows 包暂未签名。

[保留的 preview.6 发行版](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/tag/v0.2.0-preview.6)

[保留的 preview.4 发行版](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/tag/v0.2.0-preview.4)

## 历史发行版

以下版本从 Omind-Robotics 原发行仓保留，原标签、附件与 SHA256 不变；说明按原发行时的功能范围保存。

| 版本 | 内容与适用范围 | 使用说明 |
| --- | --- | --- |
| [v0.2-runtime.1](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/tag/v0.2-runtime.1) | Linux 离线规划运行包，含十五关节规划、碰撞检查、客户 API 与模型；约 291 MB | [完整说明](history/v0.2-runtime.1/README.md) |

`runtime.1` 是独立的离线规划运行包，桌面 `preview.7` 是三维调参与 ROS 2 预览工作台。两种交付内容分别保留；旧版规划／碰撞 API 不代表已集成到当前桌面工作台。
