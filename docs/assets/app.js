/* DesignVault Z 交互：分类过滤 + 实时搜索 + 哈希路由（卡片版式对齐原 FlowUs 画廊） */
(function () {
  "use strict";

  var CAT_ORDER = ["设计神器", "AI 网站", "灵感网站", "素材网站", "实用网站", "中文字体", "西文字体", "品牌规范", "设计知识", "设计便利"];
  var DEFAULT_DESC = {
    "设计神器": "在线效果生成器 · 即开即用",
    "AI 网站": "AI 生成工具",
    "灵感网站": "设计灵感参考",
    "素材网站": "设计素材资源",
    "实用网站": "在线实用工具",
    "中文字体": "免费可商用中文字体",
    "西文字体": "免费可商用西文字体",
    "品牌规范": "品牌与设计系统规范",
    "设计知识": "设计学习资源",
    "设计便利": "设计师效率工具"
  };

  var state = { cat: "全部", q: "" };

  var grid = document.getElementById("grid");
  var chipsEl = document.getElementById("chips");
  var searchInput = document.getElementById("searchInput");
  var sectionTitle = document.getElementById("sectionTitle");
  var sectionCount = document.getElementById("sectionCount");
  var emptyEl = document.getElementById("empty");
  var backTop = document.getElementById("backTop");

  // ---------- favicon 限流队列（并发 6，代理 → 站点直连 → 字母兜底） ----------
  var faQueue = [];
  var faActive = 0;

  function faPump() {
    while (faActive < 6 && faQueue.length) {
      faActive++;
      faLoad(faQueue.shift());
    }
  }

  function faLoad(job) {
    var holder = job.holder;
    var img = new Image();
    img.alt = "";
    img.referrerPolicy = "no-referrer";
    var done = false;
    var finish = function (ok) {
      if (done) return;
      done = true;
      faActive--;
      if (ok && img.naturalWidth) {
        holder.textContent = "";
        holder.appendChild(img);
      }
      faPump();
    };
    img.onload = function () { finish(true); };
    img.onerror = function () {
      if (done) return;
      img.onload = function () { finish(true); };
      img.onerror = function () { finish(false); };
      img.src = "https://" + job.domain + "/favicon.ico";
    };
    img.src = "https://favicon.im/" + job.domain + "?larger=true";
  }

  // ---------- 分类按钮（原版样式：文字 + 全角括号计数） ----------
  var catCount = {};
  DATA.forEach(function (it) { catCount[it.cat] = (catCount[it.cat] || 0) + 1; });

  var cats = ["全部"].concat(CAT_ORDER.filter(function (c) { return catCount[c]; }));
  cats.forEach(function (cat) {
    var el = document.createElement("button");
    el.className = "chip";
    el.dataset.cat = cat;
    var n = cat === "全部" ? DATA.length : catCount[cat];
    el.textContent = cat + "（" + n + "）";
    el.addEventListener("click", function () { setCat(cat); });
    chipsEl.appendChild(el);
  });

  // ---------- 过滤与渲染 ----------
  function apply() {
    var q = state.q.trim().toLowerCase();
    var list = DATA.filter(function (it) {
      if (state.cat !== "全部" && it.cat !== state.cat) return false;
      if (!q) return true;
      var hay = (it.name + " " + (it.desc || DEFAULT_DESC[it.cat] || "") + " " +
        (it.tags || []).join(" ") + " " + it.cat + " " + it.host).toLowerCase();
      return hay.indexOf(q) > -1;
    });

    sectionTitle.textContent = state.cat === "全部" ? "全部" : state.cat;
    sectionCount.textContent = list.length + " 项";

    var frag = document.createDocumentFragment();
    list.forEach(function (it) { frag.appendChild(card(it)); });
    grid.innerHTML = "";
    grid.appendChild(frag);
    emptyEl.hidden = list.length > 0;
    faPump();
  }

  var DOC_ICON_SVG =
    '<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' +
    '<path fill="currentColor" fill-opacity="0.85" d="M11.15 1c.27 0 .53.11.72.31l4.85 5.1c.18.19.28.44.28.7v9.19c0 .7-.26 1.38-.75 1.89-.49.51-1.16.8-1.87.8H5.62c-.71 0-1.39-.3-1.87-.81-.49-.51-.76-1.19-.76-1.89V3.7c0-.7.26-1.39.75-1.9.48-.51 1.15-.8 1.86-.8h5.55zM5.62 3c-.14 0-.28.06-.4.19-.12.13-.2.31-.2.51v12.6c0 .2.08.38.2.51.12.13.26.19.4.19h8.76c.15 0 .29-.06.41-.19.12-.13.19-.31.19-.51V8h-3.4a1 1 0 0 1-1-1V3H5.62zM13 6h1.58L13 4.34V6zm-.25 7.25a.75.75 0 0 1 0 1.5h-6a.75.75 0 0 1 0-1.5h6zm0-3a.75.75 0 0 1 0 1.5h-6a.75.75 0 0 1 0-1.5h6z"/></svg>';

  var GO_ICON_SVG =
    '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M7 17L17 7M9 7h8v8"/></svg>';

  function card(it) {
    var a = document.createElement("a");
    a.className = "card";
    a.href = it.url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.title = it.name;

    // 封面区：居中站点图标
    var cover = document.createElement("div");
    cover.className = "card-cover";
    var icon = document.createElement("div");
    icon.className = "site-icon";
    icon.textContent = it.name.charAt(0).toUpperCase();
    cover.appendChild(icon);

    var domain = (it.host || "").replace(/^www\./, "");
    if (domain && /^https?:$/.test(location.protocol || "https:")) {
      faQueue.push({ holder: icon, domain: domain });
    }

    // 标题栏：文档小图标 + 名称
    var title = document.createElement("div");
    title.className = "card-title";
    var docIcon = document.createElement("span");
    docIcon.innerHTML = DOC_ICON_SVG;
    var name = document.createElement("span");
    name.className = "card-name";
    name.textContent = it.name;
    title.appendChild(docIcon);
    title.appendChild(name);

    var go = document.createElement("div");
    go.className = "card-go";
    go.innerHTML = GO_ICON_SVG;

    a.appendChild(cover);
    a.appendChild(title);
    a.appendChild(go);
    return a;
  }

  // ---------- 状态与路由 ----------
  function setCat(cat) {
    state.cat = cat;
    Array.prototype.forEach.call(chipsEl.children, function (c) {
      c.classList.toggle("active", c.dataset.cat === cat);
    });
    apply();
    history.replaceState(null, "", cat === "全部" ? "#" : "#" + encodeURIComponent(cat));
    var active = chipsEl.querySelector(".chip.active");
    if (active && active.scrollIntoView) {
      active.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
    }
  }

  searchInput.addEventListener("input", function () {
    state.q = this.value;
    apply();
  });

  window.addEventListener("hashchange", function () {
    var h = decodeURIComponent(location.hash.replace(/^#/, ""));
    if (!h || cats.indexOf(h) > -1) setCat(h || "全部");
  });

  window.addEventListener("scroll", function () {
    backTop.classList.toggle("show", window.scrollY > 500);
  }, { passive: true });
  backTop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // 初始：支持 #中文字体 直达
  var init = decodeURIComponent(location.hash.replace(/^#/, ""));
  setCat(cats.indexOf(init) > -1 ? init : "全部");
})();
