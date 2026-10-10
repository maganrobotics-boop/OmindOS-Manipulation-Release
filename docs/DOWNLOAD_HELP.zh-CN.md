# 下载、校验与常见问题

[返回首页](../README.md) · [安装与首次使用](GET_STARTED.zh-CN.md)

## 我应该下载哪个？

普通用户下载 [Ubuntu 0.3.1 完整安装包](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/download/v0.3.1/omindos-workbench-0.3.1-linux-x64.tar.gz)，约 88 MB。工作台和算法在同一个包内，不需要另装轻量工作台或 runtime.2。

本版适用 Ubuntu 22.04 / 24.04 x86_64。Windows 后续安排；Jetson ARM64 不使用这个 x64 包。

## 如何校验下载？

[下载校验文件](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/download/v0.3.1/omindos-workbench-0.3.1-linux-x64.tar.gz.sha256)，与安装包放在同一目录，然后运行：

```bash
sha256sum -c omindos-workbench-0.3.1-linux-x64.tar.gz.sha256
```

该安装包的 SHA256 为：

```text
daa2d604f403759fd30825e4d8c886b8065bc2ad727ba176677b9b443bd9a81d
```

完整解压后，也可在包目录验证内部文件：

```bash
./OmindOS-Workbench --verify
```

## 浏览器没有自动打开

确认工作台程序仍在运行，手动访问 `http://127.0.0.1:8085/`。使用自定义端口时，浏览器地址也要改成相同端口。

启动程序时如提示没有执行权限，在解压目录运行 `chmod +x OmindOS-Workbench` 后重试。保留整个解压目录，不要只复制可执行文件。

## 需要登录或联网吗？

本机工作台不需要注册或登录，运行和本机仿真可离线。首次下载安装包需要网络。

## 可以在自己的程序中调用吗？

可以。同一安装包提供本机 API，默认只监听 `127.0.0.1:8085`。无需另装算法包，工作台程序需保持运行。[API 文档与示例](../releases/v0.3.1/API.zh-CN.md)

## 如何升级？

将新包解压到新目录，再运行新程序。已有客户配置保存在用户目录；升级前可导出备份。旧版与独立算法 SDK 见[历史版本](../HISTORY.zh-CN.md)。

## 正式版验收哪些内容？

0.3.1 包含完整 RM75-B / 6FB / 6F CAD。128 项源码回归、10 项原浏览器回归、46 项安装包接口检查、9 项完整 CAD 界面检查通过；正式包另通过独立解压、完整性校验和版本启动检查。

0.3.1 正式版验收本机运动学、路径规划和几何仿真，包含差速 / 全向导航，以及停车后的双臂与腰部协同。动力学、传感器定位、真机驱动和抓取接触后续升级。

[发行说明与附件](https://github.com/maganrobotics-boop/OmindOS-Manipulation-Release/releases/tag/v0.3.1)
