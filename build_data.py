# -*- coding: utf-8 -*-
"""将抓取快照清洗为站点数据：data/source-snapshot.json -> docs/assets/data.js
仅提取事实性元数据（名称/URL/分类标签），描述文字为本项目自行撰写。"""
import json
import re
from urllib.parse import urlparse

JUNK_URL = re.compile(
    r"(instagram\.com|threads\.net|patreon\.com|freight\.cargo\.site|cdn\.|"
    r"gstatic\.com|xiaohongshu\.com|weixin\.qq\.com|favicon|open-graph|"
    r"\.(png|jpe?g|webp|ico|gif|svg)(\?|$)|github\.com/[A-Za-z0-9_-]+/?$)", re.I)
FONT_DOMAINS = ("maoken.com", "befonts.com", "fonts.google.com", "fontesk.com",
                "atipofoundry.com", "pixelbuddha.net", "fontshare.com")


def clean_title(t):
    t = re.sub(r"^(副本)+", "", t or "").strip()
    return t


def pick_urls(urls):
    return [u for u in urls if not JUNK_URL.search(u)]


def host(u):
    try:
        return urlparse(u).netloc.replace("www.", "")
    except Exception:
        return ""


# ---------- 字体清洗 ----------
def clean_fonts(records, cat, suffix):
    out, seen = [], set()
    for r in records:
        if r["category"] != cat:
            continue
        title = clean_title(r["title"])
        parts = [p.strip() for p in title.split("◯")]
        name = parts[0].strip()
        tags = [p for p in parts[1:] if p and p != suffix]
        urls = pick_urls(r.get("urls", []))
        # 优先官方/字体站链接，网盘链接仅作兜底
        urls.sort(key=lambda u: (
            0 if any(d in u for d in FONT_DOMAINS) else
            1 if "pan.baidu" not in u else 2))
        if not urls or not name:
            continue
        if name.lower() in seen:
            continue
        seen.add(name.lower())
        out.append({
            "name": name, "url": urls[0], "cat": cat,
            "tags": tags, "desc": "免费可商用" + (" · " + " / ".join(tags[:3]) if tags else ""),
        })
    return out


# ---------- 非字体：人工核对过的主链接修正 ----------
OVERRIDE = {
    "伪3D切片在线编辑器": "https://sift.constraint.systems/",
    "点阵图像效果生成网站": "https://eduardadu.github.io/Digitiles/create.html",
    "动态粒子效果生成网站": "https://collidingscopes.github.io/particular-drift/",
    "动态时钟在线编辑器": "https://spacetypegenerator.com/crashclock",
    "超现实像素效果一键生成网站": "https://collapse.constraint.systems/",
    "音频可视化效果生成网站": "https://mikevandersanden.com/tools/save-our-sound/index.html",
    "动态卡片效果生成网站": "https://animos.app/editor",
    "故障图像效果生成网站": "https://editor.isf.video/u/VIDVOX",
    "ASCII字符编码效果生成网站": "http://www.injosoft.com/",
    "线性交织文字效果生成网站": "https://kintype.ksawerykomputery.pl/",
    "图像波点化生成网站": "https://lego-art-remix.com/",
    "图像动态错位故障效果生成网站": "https://flow.constraint.systems/",
    "图像转光栅效果生成网站": "https://www.tooooools.app/",
    "像素字体效果生成网站": "https://typedither.vercel.app/",
    "3D动态字一键生成器": "https://spacetypegenerator.com/boost",
    "图像风格化像素融合效果生成网站": "https://mosaic.constraint.systems/",
    "动态时钟效果生成网站": "https://spacetypegenerator.com/clutterclock",
    "动态弥散渐变效果生成网站": "https://gradients.juangarcia.ch/",
    "西文字体自定义生成网站": "https://doodlefonts.app/",
    "抽象图形效果生成网站": "https://cpreid2.github.io/blobSketch/",
    "图像变形效果生成网站": "https://tri.constraint.systems/",
    "动态浮雕效果生成网站": "https://www.tooooools.app/",
    "液态金属生成器": "https://app.paper.design/playground/liquid-metal",
    "热成像效果生成网站": "https://paper.design/",
    "螺旋图形在线编辑器": "https://vbuckenham.com/epicycles/",
    "弥散渐变效果生成网站": "https://meshgradient.in/",
    "迷幻效果在线生成网站": "https://tools.dia.tv/ouroborus/",
    "动态特效自动生成网": "https://moshpro.app/lite/",
    "图像轮廓艺术化效果生成器（自制）": "https://zolab-contour.netlify.app/",
    "ASCII字符编码效果生成器（自制）": "https://zolab-ascii.netlify.app/",
    "伪立体渐变效果生成网站": "https://gradientor.afterimage.cc/",
    "图像溶解效果生成网站": "https://jake-welch-design.github.io/noise-painting-generator/",
    "网状背景自定义生成网站": "https://moire.constraint.systems/",
    "动态螺旋文字效果生成网站": "https://pacohardt.com/type-pattern/index.html",
    "AI语音克隆神器 Voicebox": "https://voicebox.sh/",
    "图像拉伸效果生成网站": "https://constraint.systems/",
    "复古网屏效果生成网站": "https://www.tooooools.app/effects/crt",
    "3D动态粒子效果一键生成网站": "https://matrix.spline.design/",
    "监控风效果生成网站": "https://brand-generator.stoyanov.works/",
    "万花筒背景一键生成网站": "https://hua.kuaitu.cc/#/",
    "半调网屏一键生成网站": "https://halftonemaker.com/zh-CN",
    "超椭圆图形生成网站": "https://steel-stylus-87069225.figma.site/",
    "超椭圆图形生成网站": "https://steel-stylus-87069225.figma.site/",
}

# 名称去重时的重命名（同类多款工具）
RENAME = {
    "ASCII字符编码效果生成网站": "ASCII 图片转字符画 · Injosoft",
    "ASCII字符编码效果生成网站 ": "",
    "ASCII字符编码效果生成器（自制）": "ASCII 字符画生成器 · ZoLab",
    "ASCII效果生成网站": "ASCII 动效生成器 · Aniso",
    "图像风格化效果生成网站": None,  # 有多条同名，逐条在附加清单里人工收录
    "像素化效果生成网站": None,
    "图像风格化像素融合效果生成网站": "像素马赛克融合生成器 · Mosaic",
}


def clean_tools(records):
    out, seen_hosts = [], {}
    for r in records:
        if r["category"] != "设计神器":
            continue
        title = clean_title(r["title"])
        title = RENAME.get(title, title)
        if not title:
            continue
        url = OVERRIDE.get(clean_title(r["title"]))
        if not url:
            cand = pick_urls(r.get("urls", []))
            if not cand:
                continue
            url = cand[0]
        h = host(url)
        if h in seen_hosts:
            continue
        seen_hosts[h] = 1
        out.append({"name": title, "url": url, "cat": "设计神器", "tags": ["在线生成器"], "desc": ""})
    return out


def by_cat(records, cat, tag=None):
    out = []
    for r in records:
        if r["category"] != cat:
            continue
        title = clean_title(r["title"])
        urls = pick_urls(r.get("urls", []))
        if not urls:
            continue
        out.append({"name": title, "url": urls[0], "cat": cat, "tags": [tag] if tag else [], "desc": ""})
    return out


def main():
    data = json.load(open("data/source-snapshot.json", encoding="utf-8"))
    items = []

    items += clean_tools(data)
    fonts_cn = clean_fonts(data, "中文字体", "免费中文字体")
    fonts_en = clean_fonts(data, "西文字体", "免费西文字体")
    items += fonts_cn + fonts_en

    # 灵感网站（抓取可靠部分）
    insp_keep = {
        "World Vector Logo": "https://worldvectorlogo.com/",
        "Logo Ground": "https://www.logoground.com/",
        "Pinterest": "https://www.pinterest.com/",
        "Interface In Game": "https://interfaceingame.com/",
        "Maxibestof": "https://maxibestof.one/websites",
        "Branding Style Guides": "https://brandingstyleguides.com/",
        "Another Graphic": "https://anothergraphic.org/",
        "Logo Book": "https://logobook.com/",
        "The Moving Poster": "https://themovingposter.com/",
        "Giacomo Bagnara": "https://www.giacomobagnara.com/",
        "站酷": "https://www.zcool.com.cn/",
        "Behance": "https://www.behance.net/",
        "Artstation": "https://www.artstation.com/",
        "Notefolio": "https://notefolio.net/",
        "Typo Graphic Posters": "https://www.typographicposters.com/archive",
    }
    for name, url in insp_keep.items():
        items.append({"name": name, "url": url, "cat": "灵感网站", "tags": [], "desc": ""})

    # 设计工作室（灵感）
    studios = [
        ("A Black Cover", "https://ablackcover.com/", "品牌 / 平面"),
        ("立入禁止 Naeo", "https://www.studionaeo.com/", "品牌 / 平面"),
        ("条件反射 Reflex", "http://www.reflexdesign.cn/", "品牌 / 平面"),
        ("Tam", "https://tamvt.com/", "艺术 / 品牌"),
        ("UDL", "https://u-d-l.com/", "品牌 / 空间"),
        ("Pocca", "https://pocca.design/", "品牌 / 平面"),
        ("Triangle Studio", "http://www.triangle-studio.co.kr/", "品牌 / 包装"),
        ("702design 理所", "http://www.reesaw.com/", "包装 / 书籍"),
        ("王志弘 Wang Zhihong", "https://wangzhihong.com/", "书籍设计"),
        ("Pentagram", "https://www.pentagram.com/", "国际知名 / 品牌"),
        ("Studio Dumbar", "https://www.studiodumbar.com/", "动态品牌 / 荷兰"),
        ("Collins", "https://www.wearecollins.com/", "品牌 / 美国"),
        ("Koto", "https://koto.studio/", "品牌 / 科技感"),
        ("Made Thought", "https://www.madethought.com/", "品牌 / 英国"),
        ("&Walsh", "https://www.andwalsh.com/", "品牌 / 美国"),
        ("Bureau Borsche", "https://www.bureauborsche.com/", "平面 / 德国"),
    ]
    for name, url, tag in studios:
        items.append({"name": name, "url": url, "cat": "灵感网站", "tags": ["工作室", tag], "desc": ""})

    # 素材网站（抓取可靠部分 + 检索补充）
    assets = [
        ("Unsplash", "https://unsplash.com/", "免费高清图片，无需署名可商用"),
        ("Pexels", "https://www.pexels.com/", "免费图片与视频素材"),
        ("Pixabay", "https://pixabay.com/", "图片 / 矢量 / 视频综合素材"),
        ("LS Graphics", "https://www.ls.graphics/", "高质量样机与模板，部分免费"),
        ("Mockups Design", "https://mockups-design.com/", "免费 PSD 样机下载"),
        ("Mockup World", "https://www.mockupworld.co/", "免费样机聚合"),
        ("Unblast", "https://unblast.com/", "样机 / UI / 图标素材"),
        ("Wannathis", "https://wannathis.one/mockups/free", "3D 质感样机，部分免费"),
        ("Freepik", "https://www.freepik.com/", "矢量 / 图片 / PSD 海量素材"),
        ("Texturelabs", "https://texturelabs.org/", "免费高质量纹理背景"),
        ("Resource Boy", "https://resourceboy.com/", "免费设计资源合集"),
        ("Three D Scans", "https://threedscans.com/", "开源石膏 3D 模型库"),
        ("Emojipedia", "https://emojipedia.org/", "Emoji 图鉴（注意授权，非商用）"),
        ("Coverr", "https://coverr.co/", "免费商用短视频"),
        ("Mixkit", "https://mixkit.co/", "免费视频 / 音乐 / 模板"),
        ("iconfont 阿里图标库", "https://www.iconfont.cn/", "国内最大图标 /插画素材库"),
        ("unDraw", "https://undraw.co/", "免费无版权插画（可改色）"),
        ("Humaaans", "https://www.humaaans.com/", "人物插画自由组合"),
        ("Haikei", "https://haikei.app/", "SVG 背景 / 波浪 / 斑点生成素材"),
        ("Blobmaker", "https://www.blobmaker.app/", "有机形状斑点生成器"),
    ]
    for name, url, desc in assets:
        items.append({"name": name, "url": url, "cat": "素材网站", "tags": [], "desc": desc})

    # AI 网站（抓取可靠部分 + 检索补充）
    ais = [
        ("Midjourney", "https://www.midjourney.com/", "图像质量标杆级 AI 绘画"),
        ("Lovart", "https://www.lovart.ai/zh/home", "无限画布 AI 设计智能体"),
        ("Tapnow", "https://app.tapnow.ai/home", "图像 / 视频生成，无限画布"),
        ("Recraft", "https://www.recraft.ai/", "AI 矢量 / 品牌套件生成"),
        ("Krea", "https://www.krea.ai/", "实时 AI 图像生成与增强"),
        ("Ideogram", "https://ideogram.ai/", "文字排版表现力强的 AI 绘图"),
        ("Stable Diffusion", "https://stability.ai/", "开源图像生成模型生态"),
        ("Adobe Firefly", "https://firefly.adobe.com/", "Adobe 家族 AI 生成工具"),
        ("Meshy", "https://www.meshy.ai/zh/discover", "图生 3D 模型 AI"),
        ("Tripo3D", "https://www.tripo3d.ai/zh", "三维模型 AI 生成"),
        ("LiblibAI", "https://www.liblib.art/", "国内模型 / 工作流分享社区"),
        ("即梦", "https://jimeng.jianying.com/ai-tool/home", "图像 / 视频同款生成"),
        ("小云雀", "https://xyq.jianying.com/", "短剧 / 视频生成"),
        ("Flova", "https://flova.tv/zh-CN/", "短剧制作与视频 Skill"),
        ("豆包", "https://www.doubao.com/", "通用智能助手"),
        ("ChatGPT", "https://chatgpt.com/", "通用智能助手 / 氛围编程"),
        ("Gemini", "https://gemini.google.com/", "通用智能助手"),
    ]
    for name, url, desc in ais:
        items.append({"name": name, "url": url, "cat": "AI 网站", "tags": [], "desc": desc})

    # 实用网站
    utils = [
        ("TinyPNG", "https://tinypng.com/", "图片无损压缩"),
        ("Squoosh", "https://squoosh.app/", "谷歌在线图片压缩 / 转格式"),
        ("Photopea", "https://www.photopea.com/", "浏览器里的免费 PS"),
        ("remove.bg", "https://www.remove.bg/", "一键抠图去背景"),
        ("Remove Photos", "https://remove.photos/", "在线图像处理工具箱"),
        ("Coolors", "https://coolors.co/", "配色方案快速生成"),
        ("中国色", "https://www.zhongguose.com/", "中国传统色色谱"),
        ("日本传统色", "https://nipponcolors.com/", "日本传统色色谱"),
        ("Bigjpg", "https://bigjpg.com/", "AI 图片无损放大"),
        ("求字体网", "https://www.qiuziti.com/", "字体识别 / 找字体"),
        ("字数统计 · 易测网", "https://www.eteste.com/", "在线字数统计"),
        ("草料二维码", "https://cli.im/", "二维码生成器"),
        ("找台词", "http://www.zhaotaici.cn/", "影视台词搜索"),
        ("HackerTyper", "https://hackertyper.net/", "假代码生成（娱乐）"),
        ("NCM 转 MP3", "https://ncm.worthsee.com/", "网易云 NCM 格式转换"),
        ("绿色视频下载", "https://greenvideo.cc/", "主流平台视频下载"),
        ("个人所得税计算器", "http://shui.00cha.net/lwbc.asp", "个税在线计算"),
        ("潮汕话在线翻译", "http://www.chaofayin.com/", "潮汕话翻译"),
    ]
    for name, url, desc in utils:
        items.append({"name": name, "url": url, "cat": "实用网站", "tags": [], "desc": desc})

    # 品牌规范 / 设计系统（公开官方页面）
    brands = [
        ("Branding Style Guides", "https://brandingstyleguides.com/", "全球品牌手册聚合目录"),
        ("IBM Design", "https://www.ibm.com/design", "IBM 品牌与设计语言"),
        ("Atlassian Design", "https://atlassian.design/", "Atlassian 设计系统"),
        ("Spotify Design", "https://spotify.design/", "Spotify 设计团队与品牌"),
        ("Uber Brand", "https://brand.uber.com/", "Uber 品牌规范"),
        ("Material Design 3", "https://m3.material.io/", "谷歌 Material 设计系统"),
        ("Apple HIG", "https://developer.apple.com/design/human-interface-guidelines/", "苹果人机界面指南"),
        ("Fluent 2", "https://fluent2.microsoft.design/", "微软 Fluent 设计系统"),
        ("Lightning DS", "https://www.lightningdesignsystem.com/", "Salesforce 设计系统"),
        ("Ubuntu Design", "https://design.ubuntu.com/", "Ubuntu 品牌与设计资源"),
        ("GOV.UK Design", "https://design-system.service.gov.uk/", "英国政府设计系统"),
        ("USWDS", "https://designsystem.digital.gov/", "美国政府设计系统"),
    ]
    for name, url, desc in brands:
        items.append({"name": name, "url": url, "cat": "品牌规范", "tags": [], "desc": desc})

    # 设计知识
    learn = [
        ("Google Design", "https://design.google/", "谷歌设计与研究文章"),
        ("Figma Best Practices", "https://www.figma.com/best-practices/", "Figma 官方设计方法论"),
        ("Laws of UX", "https://lawsofux.com/", "用户体验设计法则合集"),
        ("NN/g Articles", "https://www.nngroup.com/articles/", "尼尔森诺曼集团 UX 研究"),
        ("Smashing Magazine", "https://www.smashingmagazine.com/", "前端 / 设计深度文章"),
        ("Refactoring UI", "https://www.refactoringui.com/", "界面设计实用方法论"),
        ("Practical Typography", "https://practicaltypography.com/", "排版实用指南"),
        ("Type Scale", "https://type-scale.com/", "字号层级比例工具与讲解"),
        ("Typewolf", "https://www.typewolf.com/", "字体搭配灵感与站点排版范例"),
    ]
    for name, url, desc in learn:
        items.append({"name": name, "url": url, "cat": "设计知识", "tags": [], "desc": desc})

    # 设计便利
    handy = [
        ("AE 文本动效速查", "https://blog.motionisland.com/after-effects-presets-text-animation/", "AE 文字动画预设速查手册"),
        ("Fontpair", "https://www.fontpair.co/", "Google Fonts 字体搭配参考"),
        ("Fonts In Use", "https://fontsinuse.com/", "真实作品中的字体使用案例"),
        ("Animista", "https://animista.net/", "CSS 动画即调即用"),
        ("Cubic-Bezier", "https://cubic-bezier.com/", "缓动曲线调试"),
        ("UI Gradients", "https://uigradients.com/", "渐变配色速查"),
        ("Can I Use", "https://caniuse.com/", "浏览器兼容性速查"),
        ("CSS-Tricks", "https://css-tricks.com/", "前端技巧与速查表"),
    ]
    for name, url, desc in handy:
        items.append({"name": name, "url": url, "cat": "设计便利", "tags": [], "desc": desc})

    # 设计神器的自动描述补齐（按域名/名称关键词给一句事实描述）
    TOOL_DESC = [
        ("constraint.systems", "Grant Custer 出品的实时图像效果实验工具"),
        ("tooooools", "Precar Dan 的图像效果小工具集"),
        ("spacetypegenerator", "Kiel D M 的动态字体效果生成器"),
        ("paper.design", "paper.design 在线设计工作台"),
        ("halftone", "半调网屏效果生成工具"),
    ]
    for it in items:
        if it["desc"]:
            continue
        for key, desc in TOOL_DESC:
            if key in it["url"]:
                it["desc"] = desc
                break

    # 汇总输出
    seen = set()
    final = []
    for it in items:
        key = (it["name"].lower(), it["cat"])
        if key in seen or not it["name"] or not it["url"]:
            continue
        seen.add(key)
        it["host"] = host(it["url"])
        final.append(it)

    json.dump(final, open("data/items-clean.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # 生成 data.js
    cats = {}
    for it in final:
        cats[it["cat"]] = cats.get(it["cat"], 0) + 1
    js = ("// DesignVault-Z 站点数据（名称/链接/分类为事实性元数据，描述为本项目撰写）\n"
          "const DATA = " + json.dumps(final, ensure_ascii=False, indent=1) + ";\n")
    open("docs/assets/data.js", "w", encoding="utf-8").write(js)
    print(json.dumps(cats, ensure_ascii=False, indent=1))
    print("TOTAL:", len(final))


if __name__ == "__main__":
    main()
