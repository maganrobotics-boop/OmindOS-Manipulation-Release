# OmindOS 机械臂统一工作台

**用户只需要下载一个 Ubuntu 完整包。** 三维工作台、双臂与腰部协同算法、差速与全向底盘导航及运行依赖已包含在同一个包中，无需另外下载算法包。

## 下载并打开

[**下载 Ubuntu 完整包 · 0.3.0**](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/download/v0.3.0/omindos-workbench-0.3.0-linux-x64.tar.gz)

适用 Ubuntu 22.04 x86_64；本版只发布 Ubuntu。无需另装 Python、ROS、Node.js 或 Docker，无需注册或登录，本机仿真可以离线运行。

1. 下载上面的完整包并完整解压。
2. 在解压目录打开终端，运行 `./OmindOS-Workbench`。
3. 程序会自动打开本机工作台；浏览器未自动打开时，访问 `http://127.0.0.1:8085/`。

保留同目录的运行库和模型资源。升级时解压到新目录，已有客户配置保存在用户目录中。

## 包里能做什么

- 三维机器人显示，按客户硬件修改模型、关节限位、TCP 和设备参数，保存及导入导出配置。
- 双臂与共享腰部协同规划、关节路径规划及保守离散碰撞检查。
- 差速或全向底盘地图避障、目标朝向、路径显示和停车确认。
- 先导航，到位停车后再执行双臂任务；支持取消和软件停止。

本版验收本机运动学、路径规划和几何仿真。真实传感器定位、真机驱动及动力学后续联调；Windows 后续升级。

## 使用说明

[底盘导航与地图配置](releases/v0.3.0/NAVIGATION.zh-CN.md) · [双臂、腰部与客户模型配置](releases/v0.3.0/PLANNING.zh-CN.md) · [发行范围与验收记录](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/tag/v0.3.0)

开发者可直接调用同一程序的 [本机 API](releases/v0.3.0/API.zh-CN.md)，无需额外算法包。

[历史版本与开发者独立算法 SDK](HISTORY.zh-CN.md)
