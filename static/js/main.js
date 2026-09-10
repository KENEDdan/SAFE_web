(function () {
  "use strict";

  // ---- Theme toggle (persisted) ----
  var htmlEl = document.documentElement;
  var toggle = document.getElementById("themeToggle");

  function syncToggle() {
    if (!toggle) return;
    var dark = htmlEl.getAttribute("data-theme") === "dark";
    var icon = toggle.querySelector(".theme-icon");
    var label = toggle.querySelector(".theme-label");
    if (icon) icon.textContent = dark ? "☀️" : "\u{1F319}";
    if (label) label.textContent = dark ? "Light" : "Dark";
  }

  if (toggle) {
    syncToggle();
    toggle.addEventListener("click", function () {
      var next = htmlEl.getAttribute("data-theme") === "dark" ? "light" : "dark";
      htmlEl.setAttribute("data-theme", next);
      try { localStorage.setItem("safe-theme", next); } catch (e) {}
      syncToggle();
    });
  }

  // ---- Mobile drawer ----
  var burger = document.getElementById("burger");
  var drawer = document.getElementById("drawer");
  var overlay = document.getElementById("drawerOverlay");

  function closeDrawer() {
    if (drawer) drawer.classList.remove("open");
    if (overlay) overlay.classList.remove("open");
  }

  if (burger && drawer && overlay) {
    burger.addEventListener("click", function (e) {
      e.stopPropagation();
      drawer.classList.toggle("open");
      overlay.classList.toggle("open");
    });
    overlay.addEventListener("click", closeDrawer);
    drawer.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeDrawer);
    });
  }

  // ---- Django formset "add row" ----
  var addRowBtn = document.querySelector("[data-formset-add]");
  if (addRowBtn) {
    addRowBtn.addEventListener("click", function () {
      var container = document.getElementById("formset-rows");
      var totalForms = document.querySelector("[name$='-TOTAL_FORMS']");
      var template = document.getElementById("empty-form-template");
      if (!container || !totalForms || !template) return;
      var idx = parseInt(totalForms.value, 10);
      container.insertAdjacentHTML(
        "beforeend",
        template.innerHTML.replace(/__prefix__/g, idx)
      );
      totalForms.value = idx + 1;
    });
  }
})();
