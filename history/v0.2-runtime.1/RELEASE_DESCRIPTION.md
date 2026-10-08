移动底盘＋俯仰腰关节＋双 RM75-B 七轴机械臂，上半身十五关节。

下载下方 `OmindOS-Manipulation-0.2-Customer-Release-Linux-amd64.zip` 与 `SHA256SUMS-Customer-Release`，按仓库 README 校验、解压并运行。完整 ZIP 包含客户端、封装运行程序、URDF/网格、参数、API 示例、使用说明和验收记录。

- 55 项回归通过；脱离源码目录的独立安装与运行验收通过。
- 验证底盘到达/连续停稳后的十五关节规划、碰撞拦截、URDF 修改、取消与超时。
- Linux x86_64；构建及验证环境 glibc 2.39。其他平台需单独验证。
- 当前用于离线几何规划和仿真记录联动，不发送真机运动命令；真机尚未验收。
- 不附送核心算法 `.py` 源码。运行程序采用 Python 编译字节码及依赖库封装，不是源码加密。

ZIP SHA-256：`3cb2895821526cb0f1d9816b5f3fb7f8e89ba664859f74086838f6bdc569b770`

GitHub 自动生成的 Source code 仅为本公开入口的文档快照，不是可运行客户包。