# 客户程序调用 API

普通用户只下载一个 Ubuntu 完整包即可。工作台运行时，同一程序提供本机 HTTP JSON API；开发者可用 Python、C++、JavaScript、ROS 节点或其他语言的 HTTP 客户端调用，不必再安装独立算法包。

本版 API 只监听本机 `127.0.0.1`，默认端口 8085；默认无登录或 API Key。跨机器调用和其他网页的跨域调用不在本版范围。接口返回的是运动学、规划或几何仿真结果，尚不发送真机驱动指令。

## 启动和读取状态

完整解压 Ubuntu 包后，在包目录运行：

```bash
./OmindOS-Workbench --no-browser
curl http://127.0.0.1:8085/v1/workbench-state
curl http://127.0.0.1:8085/v1/navigation-config
```

用 `--port 8086` 修改端口，客户端地址也相应改为 `http://127.0.0.1:8086`。前端界面可以不打开，但可执行程序必须保持运行。POST 使用 `Content-Type: application/json`。

## 常用接口

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/v1/workbench-active-profile` | 读取已写入程序的客户配置和当前联锁状态 |
| POST | `/v1/workbench-active-profile` | 校验并写入完整客户 profile；使旧运动结果失效 |
| GET | `/v1/planning-config` | 读取参考双臂、腰部与 TCP 映射 |
| POST | `/v1/planning-start` | 启动关节路径或双手共同位移规划 |
| GET | `/v1/planning-task/{task_id}` | 读取规划状态与成功结果中的路径帧 |
| POST | `/v1/planning-cancel` | 用 `{"task_id":"返回的任务ID"}` 取消规划 |
| GET | `/v1/navigation-config` | 读取导航默认参数和支持的两种底盘 |
| POST | `/v1/navigation-start` | 启动导航，可选到位停车后继续双臂规划 |
| GET | `/v1/navigation-task/{task_id}` | 读取导航位姿、路径、命令、停车状态及双臂结果 |
| POST | `/v1/navigation-cancel` | 用 task_id 取消当前导航 |
| POST | `/v1/robot-model` | 用 URDF、关节值和底盘位姿计算三维模型与正运动学 |
| POST | `/v1/workbench-stop` | 软件停止；`{"engaged":true}` 停止，复位需当前 motion_epoch |

导航请求必须提供 `profile`、`start` 和 `goal`。可选 `config`、`base_pose`、`mapping`、`obstacles` 和 `manipulation`。距离用米，关节角度和 yaw 用弧度。两种 drive_type 为 `differential` 和 `omnidirectional`。

导航任务提交后，每 0.1–0.5 秒读取一次任务状态；读取同时续期客户端连接。连续超过 3 秒未读取会停止导航并使任务失败。导航活动状态为 planning、navigating、aligning、parking、manipulation_planning；仅导航的成功终态为 parked；带 manipulation 的整合任务成功终态为 succeeded。failed 或 canceled 不要当作成功。导航期间其他运动请求返回 423。参数错误返回 400，未知任务返回 404；POST 类型错误返回 415。

成功导航结果中的 navigation 包含实际仿真 base_pose、pose、path、cmd_vel、parking_confirmed 和 stable_stop_s。带 manipulation 的任务在确认停车后调用双臂与共享腰部算法；其 result 包含 frames、validated_samples、误差和 navigation_map_checked。不带 manipulation 的导航任务 result 为 null，应读取 navigation。

## 可运行示例

[下载客户侧示例](examples/api_client.py)。工作台本身无需 Python；以下代码仅演示客户使用 Python 标准库调用接口，客户程序也可选其他语言。

```bash
python3 api_client.py
python3 api_client.py --drive omnidirectional
```

示例使用随包参考机器人，在空地图中导航到 X=0.12 m、Y=0.10 m、yaw=0.10 rad，确认停车后双手共同沿 X 移动 0.005 m，最后打印结果。它不会覆盖已保存的客户参数。实际项目应替换 profile、start、mapping、base_pose、goal 和地图；参考关节名称不适用于所有硬件。

其他请求字段和碰撞范围见 [导航说明](NAVIGATION.zh-CN.md) 与 [规划说明](PLANNING.zh-CN.md)。取消或软件停止不归零，解除软件停止不自动续跑。软件停止不是硬件急停。
