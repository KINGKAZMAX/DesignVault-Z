# 🗂️ DesignVault Z · 设计资源库

> 设计师资源导航站：神器网站 · AI 工具 · 灵感网站 · 素材 · 实用工具 · 免费中文字体 · 免费西文字体 · 品牌规范 · 设计知识 · 设计便利

**在线访问**：[https://kingkazmax.github.io/DesignVault-Z/](https://kingkazmax.github.io/DesignVault-Z/)

## ✨ 项目特点

- **363+ 精选资源**，覆盖 10 个分类，持续更新
- **纯静态、零依赖**：HTML + CSS + JS，无需构建，加载飞快
- **实时搜索**：按名称 / 描述 / 标签 / 域名即时过滤
- **分类直达**：支持 `#中文字体` 哈希路由分享
- **Favicon 自动抓取**：卡片自动展示站点图标（DuckDuckGo Icons），失败时回退字母头像
- **响应式**：桌面 / 平板 / 手机自适应布局

## 📁 目录结构

```
docs/
├── index.html          # 页面骨架
├── assets/
│   ├── style.css       # FlowUs 风格样式（暖橙点缀 / 白卡片 / 圆角）
│   ├── app.js          # 过滤 / 搜索 / 路由逻辑
│   └── data.js         # 站点数据（由 build_data.py 生成）
data/
└── source-snapshot.json  # 采集原始快照（仅元数据）
build_data.py           # 数据清洗构建脚本
```

## 🛠️ 本地开发

```bash
# 1. 直接预览
cd docs && python -m http.server 8930
# 打开 http://127.0.0.1:8930

# 2. 重新构建数据（修改 source-snapshot.json 后）
python build_data.py
```

## ➕ 如何添加资源

编辑 `build_data.py` 中对应分类的清单，或直接在 `docs/assets/data.js` 中追加：

```js
{ "name": "资源名", "url": "https://example.com", "cat": "素材网站",
  "tags": ["免费"], "desc": "一句话说明", "host": "example.com" }
```

## ⚖️ 声明

本站仅收录资源**链接与事实性元数据**（名称 / 分类 / 标签），描述文字为本项目撰写。各资源版权归原作者所有，商用前请自行确认授权。

整理思路参考了设计师社区公开分享的资源收藏库（如 FlowUs 上的「Zo 收藏库」等），特此致谢。

## 📄 License

页面代码采用 [MIT License](LICENSE) 发布。
