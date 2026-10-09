# OmindOS 发行仓维护约定

## 项目首页

用户已于 2026-10-09 确认：所有 OmindOS 项目的发行首页格式借鉴 Navigation，后续继续沿用。

参考首页：https://github.com/maganrobotics-boop/OmindOS-Navigation-Release

维护 README 时遵循 [首页统一格式](docs/HOMEPAGE_TEMPLATE.zh-CN.md)：项目用途 → 一个 Ubuntu 完整包下载入口 → 当前功能 → 实际工作台截图 → 客户参数配置 → 登录与 API → 更多资料。新项目也沿用这一结构，根据实际功能填写内容。

普通用户只需要一个完整安装包。历史版本、SDK、校验文件和内部实现细节放在资料页。核实当前版本、平台、依赖、下载链接和截图，准确区分已发行功能、开发预览与真机验收。

本仓目前主机端交付只开发 Ubuntu，Windows 后续安排。修改首页文字和图片时，无需重新构建安装包；保持现有发行附件和验收记录。
