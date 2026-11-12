(function () {
  var WHATSAPP = "201026002033";
  var root = document.documentElement;
  root.classList.add("js");

  function save(key, value) { try { localStorage.setItem(key, value); } catch (e) {} }

  /* ---------- Language: each language is its own page; this only picks the interface strings ---------- */
  var UI = {
    en: { dark: "Dark", light: "Light", needName: "Enter your name and phone number first.",
          hello: "Hello Harvest,", name: "Name", phone: "Phone", interest: "Interested in" },
    ar: { dark: "داكن", light: "فاتح", needName: "اكتب الاسم ورقم الهاتف أولاً.",
          hello: "مرحباً هارفست،", name: "الاسم", phone: "الهاتف", interest: "مهتم بـ" }
  };
  function ui() { return UI[root.lang === "ar" ? "ar" : "en"]; }

  /* ---------- Theme: follows the visitor's system until they choose ---------- */
  var themeBtn = document.getElementById("theme-toggle");
  var systemDark = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  function isDark() {
    var chosen = root.getAttribute("data-theme");
    if (chosen === "dark") return true;
    if (chosen === "light") return false;
    return !!(systemDark && systemDark.matches);
  }
  function paintThemeButton() {
    if (!themeBtn) return;
    var dark = isDark();
    /* the button names the theme you would switch to */
    themeBtn.textContent = dark ? ui().light : ui().dark;
    themeBtn.setAttribute("aria-pressed", dark ? "true" : "false");
  }
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var next = isDark() ? "light" : "dark";
    root.setAttribute("data-theme", next);
    save("harvest-theme", next);
    paintThemeButton();
  });
  if (systemDark && systemDark.addEventListener) systemDark.addEventListener("change", paintThemeButton);

  document.addEventListener("harvest:lang", paintThemeButton);
  paintThemeButton();

  /* ---------- Mobile menu ---------- */
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- Client sector tabs ---------- */
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".tab"));
  function select(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    });
    if (focus) tab.focus();
  }
  if (tabs.length) {
    document.getElementById("tabs").hidden = false;
    select(tabs[0]);
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var forward = root.dir === "rtl" ? "ArrowLeft" : "ArrowRight";
        var back = root.dir === "rtl" ? "ArrowRight" : "ArrowLeft";
        if (e.key === forward) select(tabs[(i + 1) % tabs.length], true);
        if (e.key === back) select(tabs[(i - 1 + tabs.length) % tabs.length], true);
      });
    });
  }

  /* ---------- Programme buttons pre-fill the enquiry form ---------- */
  document.querySelectorAll("[data-interest]").forEach(function (a) {
    a.addEventListener("click", function () {
      var sel = document.getElementById("f-interest");
      if (sel) sel.value = a.getAttribute("data-interest");
    });
  });

  /* ---------- Enquiry form opens WhatsApp with the message written out ---------- */
  var form = document.getElementById("enquiry");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var t = ui();
      var name = document.getElementById("f-name").value.trim();
      var phone = document.getElementById("f-phone").value.trim();
      var sel = document.getElementById("f-interest");
      var interest = sel.options[sel.selectedIndex].textContent;
      var msg = document.getElementById("f-msg").value.trim();
      var err = document.getElementById("f-error");
      if (!name || !phone) {
        err.textContent = t.needName;
        err.hidden = false;
        return;
      }
      err.hidden = true;
      var text = t.hello + "\n" +
        t.name + ": " + name + "\n" +
        t.phone + ": " + phone + "\n" +
        t.interest + ": " + interest + (msg ? "\n" + msg : "");
      var a = document.createElement("a");
      a.href = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(text);
      a.target = "_blank"; a.rel = "noopener";
      document.body.appendChild(a); a.click(); a.remove();
    });
  }

  var y = document.getElementById("year-now");
  if (y) y.textContent = new Date().getFullYear();
})();
