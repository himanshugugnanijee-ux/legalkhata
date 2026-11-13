/* Legal Khata site script: query forms, country memory, local-time hours, menus. */
(function () {
  var WA = "917048915155";
  var PREVIEW = !!window.LK_PREVIEW;
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* mobile menu */
  var head = document.querySelector(".head"), mb = document.querySelector(".menu-btn");
  if (mb) mb.addEventListener("click", function () {
    var open = head.classList.toggle("open");
    mb.setAttribute("aria-expanded", open ? "true" : "false");
  });
  /* close dropdowns on outside click or Escape, keep one open at a time */
  var dds = [].slice.call(document.querySelectorAll(".nav details"));
  dds.forEach(function (d) {
    d.addEventListener("toggle", function () { if (d.open) dds.forEach(function (o) { if (o !== d) o.open = false; }); });
  });
  document.addEventListener("click", function (e) { dds.forEach(function (d) { if (d.open && !d.contains(e.target)) d.open = false; }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") dds.forEach(function (d) { d.open = false; }); });

  /* remember the chosen country */
  [].forEach.call(document.querySelectorAll("[data-edition-link]"), function (a) {
    a.addEventListener("click", function () { store("lk_edition", a.getAttribute("data-edition-link")); });
  });

  /* office hours shown in the visitor's own time */
  [].forEach.call(document.querySelectorAll("[data-local-hours]"), function (el) {
    try {
      var now = new Date();
      var y = now.getUTCFullYear(), m = now.getUTCMonth(), d = now.getUTCDate();
      var open = new Date(Date.UTC(y, m, d, 1, 30)), close = new Date(Date.UTC(y, m, d, 13, 30)); /* 7:00 and 19:00 IST */
      var f = new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit" });
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
      if (tz && tz !== "Asia/Kolkata" && tz !== "Asia/Calcutta") el.textContent = " That is " + f.format(open) + " to " + f.format(close) + " in your time zone.";
    } catch (e) {}
  });

  /* suggest the visitor's country edition (never redirects) */
  var geo = document.querySelector(".geo");
  if (geo && !PREVIEW && !store("lk_edition") && window.fetch) {
    fetch("/api/geo").then(function (r) { return r.json(); }).then(function (j) {
      var c = (j && j.country || "").toLowerCase();
      if (c === "gb") c = "uk";
      var cur = document.documentElement.getAttribute("data-edition");
      var link = document.querySelector('[data-edition-link="' + c + '"]');
      if (!c || c === cur || !link) return;
      geo.querySelector("span").textContent = "You seem to be visiting from " + link.getAttribute("data-name") + ".";
      var a = geo.querySelector("a"); a.href = link.href; a.textContent = "Open the " + link.getAttribute("data-name") + " site";
      a.addEventListener("click", function () { store("lk_edition", c); });
      geo.hidden = false;
    }).catch(function () {});
    geo.querySelector("button").addEventListener("click", function () { geo.hidden = true; store("lk_edition", document.documentElement.getAttribute("data-edition")); });
  }

  /* query forms */
  function waLink(d) {
    var t = "Hello Legal Khata, I am " + d.name + ". I need help with: " + (d.service || "a query") + "." +
      (d.message ? " " + d.message : "") + " My phone: " + d.phone + "." + (d.country ? " (" + d.country + ")" : "");
    return "https://wa.me/" + WA + "?text=" + encodeURIComponent(t);
  }
  [].forEach.call(document.querySelectorAll("form.lead"), function (form) {
    var err = form.querySelector(".err"), btn = form.querySelector("button[type=submit]");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var d = {};
      [].forEach.call(form.elements, function (el) { if (el.name) d[el.name] = (el.value || "").trim(); });
      var digits = (d.phone || "").replace(/\D/g, "");
      if (!d.name || d.name.length < 2) { err.textContent = "Please enter your name."; err.hidden = false; return; }
      if (digits.length < 8 || digits.length > 15) { err.textContent = "Please enter a valid phone number, with country code if you are outside India."; err.hidden = false; return; }
      err.hidden = true;
      d.page = location.pathname; d.referrer = document.referrer || "";
      var link = waLink(d);
      var box = document.createElement("div"); box.className = "done"; box.setAttribute("role", "status");
      box.innerHTML = "<strong>Opening WhatsApp…</strong><p>Tap <b>send</b> in WhatsApp to deliver your query to Legal Khata. We will call you back on " + esc(d.phone) + " during office hours.</p>" +
        (PREVIEW ? "<p class='note'>Preview only: on the live site this opens WhatsApp with your query pre-filled.</p>" : "") +
        "<a class='btn wa' target='_blank' rel='noopener' href='" + link + "'>Open WhatsApp again</a>";
      form.replaceWith(box);
      try { if (window.gtag) window.gtag("event", "generate_lead", { service: d.service || "", edition: d.edition || "" }); } catch (x) {}
      if (PREVIEW) return;
      /* open WhatsApp straight away with the query pre-filled, addressed to Legal Khata */
      window.open(link, "_blank", "noopener");
      /* best-effort background save; WhatsApp delivery above does not depend on this */
      try { fetch("/api/lead", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(d) }).catch(function () {}); } catch (x) {}
    });
  });
})();
