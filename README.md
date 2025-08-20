# Auto Domain Filter

这个仓库使用 GitHub Actions 自动运行 Python 脚本，每两天从以下来源更新过滤后的广告域名列表：

- 广告域名来源：https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro.mini-onlydomains.txt
- 中国域名来源：https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/direct-list.txt

脚本逻辑：
- 获取并清理两个列表（去除注释）。
- 从广告列表中移除中国域名及其子域名。
- 输出到 `filtered_ad_domains.txt` 并提交更新。

## 如何使用
- 克隆仓库：`git clone https://github.com/yourusername/auto-domain-filter.git`
- 输出文件：`filtered_ad_domains.txt` 会自动保持最新。

## Actions 配置
- 每两天自动运行。
- 支持手动触发（在 GitHub Actions 页面）。

如果有问题，检查 Actions 日志。
