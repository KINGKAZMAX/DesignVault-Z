/* DesignVault-Z 交互逻辑：分类过滤 + 实时搜索 + 哈希路由 */
(function () {
  "use strict";

  var CAT_ORDER = ["设计神器", "AI 网站", "灵感网站", "素材网站", "实用网站", "中文字体", "西文字体", "品牌规范", "设计知识", "设计便利"];
  var CAT_ICON = {
    "设计神器": "✨", "AI 网站": "🤖", "灵感网站": "💡", "素材网站": "📦",
    "实用网站": "🧰", "中文字体": "🇨🇳", "西文字体": "🔤", "品牌规范": "📘",
    "设计知识": "📚", "设计便利": "⚡"
  };

  var state = { cat: "全部", q: "" };

  var grid = document.getElementById("grid");
  var chipsEl = document.getElementById("chips");
  var searchInput = document.getElementById("searchInput");
  var sectionTitle = document.getElementById("sectionTitle");
  var sectionCount = document.getElementById("sectionCount");
  var emptyEl = document.getElementById("empty");
  var statsEl = document.getElementById("stats");
  var backTop = document.getElementById("backTop");

  // ---------- 渲染分类 ----------
  var catCount = {};
  DATA.forEach(function (it) { catCount[it.cat] = (catCount[it.cat] || 0) + 1; });

  var cats = ["全部"].concat(CAT_ORDER.filter(function (c) { return catCount[c]; }));
  cats.forEach(function (cat) {
    var el = document.createElement("button");
    el.className = "chip";
    el.dataset.cat = cat;
    var n = cat === "全部" ? DATA.length : catCount[cat];
    el.innerHTML = (CAT_ICON[cat] ? CAT_ICON[cat] + " " : "") + esc(cat) + ' <span class="n">' + n + "</span>";
    el.addEventListener("click", function () { setCat(cat); });
    chipsEl.appendChild(el);
  });

  // ---------- 顶部统计 ----------
  statsEl.innerHTML =
    '<span><b>' + DATA.length + "</b>个精选资源</span>" +
    '<span><b>' + Object.keys(catCount).length + "</b>个分类</span>" +
    '<span><b>' + DATA.filter(function (d) { return d.cat.indexOf("字体") > -1; }).length + "</b>款免费可商用字体</span>" +
    '<span><b>' + catCount["设计神器"] + "</b>个在线神器</span>";

  // ---------- 过滤 ----------
  function apply() {
    var q = state.q.trim().toLowerCase();
    var list = DATA.filter(function (it) {
      if (state.cat !== "全部" && it.cat !== state.cat) return false;
      if (!q) return true;
      var hay = (it.name + " " + (it.desc || "") + " " + (it.tags || []).join(" ") + " " + it.cat + " " + it.host).toLowerCase();
      return hay.indexOf(q) > -1;
    });

    sectionTitle.textContent = (CAT_ICON[state.cat] ? CAT_ICON[state.cat] + " " : "") + state.cat;
    sectionCount.textContent = list.length + " 项";

    var frag = document.createDocumentFragment();
    list.forEach(function (it) { frag.appendChild(card(it)); });
    grid.innerHTML = "";
    grid.appendChild(frag);
    emptyEl.hidden = list.length > 0;
  }

  function card(it) {
    var a = document.createElement("a");
    a.className = "card";
    a.href = it.url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";

    var icon = document.createElement("div");
    icon.className = "favicon";
    icon.textContent = it.name.charAt(0).toUpperCase();
    var domain = it.host.replace(/^www\./, "");
    if (domain && /^https?:$/.test(location.protocol || "https:")) {
      // 直接加载目标站点 favicon，失败则保留字母头像
      var img = new Image();
      img.loading = "lazy";
      img.alt = "";
      img.referrerPolicy = "no-referrer";
      img.src = "https://" + domain + "/favicon.ico";
      img.onload = function () {
        if (img.naturalWidth > 1) { icon.textContent = ""; icon.appendChild(img); }
      };
    }

    var nameBox = document.createElement("div");
    var name = document.createElement("div");
    name.className = "card-name";
    name.textContent = it.name;
    var hostEl = document.createElement("span");
    hostEl.className = "card-host";
    hostEl.textContent = domain;
    nameBox.appendChild(name);
    nameBox.appendChild(hostEl);

    var top = document.createElement("div");
    top.className = "card-top";
    top.appendChild(icon);
    top.appendChild(nameBox);

    var go = document.createElement("div");
    go.className = "card-go";
    go.innerHTML = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M7 17L17 7M9 7h8v8"/></svg>';

    a.appendChild(top);
    a.appendChild(go);

    if (it.desc) {
      var d = document.createElement("div");
      d.className = "card-desc";
      d.textContent = it.desc;
      a.appendChild(d);
    }

    var tags = (it.tags || []).slice(0, 3);
    if (tags.length) {
      var box = document.createElement("div");
      box.className = "card-tags";
      tags.forEach(function (t) {
        var s = document.createElement("span");
        s.className = "tag";
        s.textContent = t;
        box.appendChild(s);
      });
      a.appendChild(box);
    }
    return a;
  }

  // ---------- 状态 ----------
  function setCat(cat) {
    state.cat = cat;
    Array.prototype.forEach.call(chipsEl.children, function (c) {
      c.classList.toggle("active", c.dataset.cat === cat);
    });
    apply();
    if ("#" + cat !== decodeURIComponent(location.hash).replace(/^#/, "#")) {
      history.replaceState(null, "", cat === "全部" ? "#" : "#" + encodeURIComponent(cat));
    }
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

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  // 初始：支持 #中文字体 直达
  var init = decodeURIComponent(location.hash.replace(/^#/, ""));
  setCat(cats.indexOf(init) > -1 ? init : "全部");
})();
