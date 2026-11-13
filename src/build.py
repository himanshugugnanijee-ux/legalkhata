#!/usr/bin/env python3
"""Builds the Legal Khata website.  python3 build.py [--preview]
Normal build  -> ../worker/public  (clean URLs, for legalkhata.com)
Preview build -> ../preview        (relative links, for clicking through before going live)"""
import html, json, os, re, shutil, sys
from datetime import date
from content_india import *
from content_world import COUNTRIES, GLOBAL, NRI_SERVICES, NRI_FAQS

OFFLINE = "--offline" in sys.argv
PREVIEW = "--preview" in sys.argv or OFFLINE
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "offline" if OFFLINE else "preview" if PREVIEW else "worker/public")
SITE = "https://legalkhata.com"
TODAY = date.today().isoformat()
PHONE, PHONE_SHOW, WA = "+917048915155", "+91 70489 15155", "917048915155"
EMAIL = "infolegalkhata@gmail.com"
# slug -> (image path, alt text, width, height) shown beside the hero text on that service page
SERVICE_HERO_IMAGES = {
    "income-tax-return": ("/assets/img/tax-savings-bag.jpg", "Tax savings and income tax return filing", 720, 1280),
    "gst-registration": ("/assets/img/gst-coins.jpg", "GST registration and return filing", 1080, 709),
    "gst-return-filing": ("/assets/img/gst-coins.jpg", "GST registration and return filing", 1080, 709),
}
ADDR1, ADDR2 = "D-13/171, Second Floor", "Sector 7, Rohini, Delhi 110085"
MAPS = "https://www.google.com/maps/search/?api=1&query=D-13%2F171%2C%20Second%20Floor%2C%20Sector%207%2C%20Rohini%2C%20Delhi%20110085"
SOCIAL = [("Facebook", "https://www.facebook.com/legalkhata"), ("Instagram", "https://www.instagram.com/legalkhata"),
          ("YouTube", "https://www.youtube.com/@legalkhata7683")]
e = html.escape

IN = dict(code="in", name="India", short="India", lang="en-IN", prefix="")
for c in COUNTRIES:
    c["prefix"] = "/" + c["code"]
    c["the"] = ("the " if c["code"] in ("us", "uk", "ae") else "") + c["name"]
GLOBAL["the"] = "other countries"
GLOBAL["prefix"] = "/global"
EDITIONS = [IN] + COUNTRIES + [GLOBAL]
CHIP = {"global": "INT"}
SVC = {s["slug"]: s for s in SERVICES}

I_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'
I_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 20zm4.4-6c-.2-.1-1.4-.7-1.6-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5 0a6.600 6.600 0 0 1-3.300-2.900c-.2-.4.2-.4.7-1.300.1-.2 0-.3 0-.5l-.7-1.800c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.200 5.200 5.200 0 0 0 1.100 2.700 11.700 11.700 0 0 0 4.500 4c1.700.7 2.300.8 3.100.6a2.700 2.700 0 0 0 1.800-1.200 2.200 2.200 0 0 0 .1-1.300c0-.1-.2-.2-.5-.3z"/></svg>'
I_GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>'
LOGO = '<svg viewBox="0 0 34 34" aria-hidden="true"><rect x="1" y="1" width="32" height="32" rx="5" fill="#0f2233"/><path d="M10 6v22M13 6v22" stroke="#c3162c" stroke-width="1.6"/><path d="M17 12h10M17 17h10M17 22h7" stroke="#eef4ea" stroke-width="2" stroke-linecap="round"/></svg>'

PAGES = []          # every page: dict(ed, path, title, desc, body, alt, schema, crumbs)
ALT = {}            # alt key -> {edition code: path}

def clip(s, max_len):
    """Trim s to max_len at a word boundary (never mid-word), no ellipsis."""
    if len(s) <= max_len: return s
    cut = s[:max_len]
    sp = cut.rfind(" ")
    return (cut[:sp] if sp > 0 else cut).rstrip(" ,|-")

def add(ed, path, title, desc, body, alt=None, schema=None, crumbs=None, noindex=False):
    title = clip(title, 60)
    desc = clip(desc, 160)
    PAGES.append(dict(ed=ed, path=path, title=title, desc=desc, body=body, alt=alt, schema=schema or [], crumbs=crumbs, noindex=noindex))
    if alt: ALT.setdefault(alt, {})[ed["code"]] = path

def home(ed): return ed["prefix"] + "/" if ed["prefix"] else "/"
def p(ed, slug): return ed["prefix"] + "/" + slug
def ul(items, cls=""): return "<ul%s>%s</ul>" % (' class="%s"' % cls if cls else "", "".join("<li>%s</li>" % e(i) for i in items))
def faq_html(faqs): return '<div class="faq">%s</div>' % "".join("<details><summary>%s</summary><p>%s</p></details>" % (e(q), e(a)) for q, a in faqs)
def faq_schema(faqs): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
def crumb_html(crumbs): return '<ol class="crumbs">%s</ol>' % "".join('<li><a href="%s">%s</a></li>' % (u, e(n)) if u else "<li>%s</li>" % e(n) for n, u in crumbs)
def crumb_schema(crumbs, path): return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (u or path)} for i, (n, u) in enumerate(crumbs)]}

def office_schema():
    return {"@context": "https://schema.org", "@type": "AccountingService", "@id": SITE + "/#office", "name": "Legal Khata", "url": SITE + "/",
            "telephone": PHONE, "email": EMAIL, "logo": SITE + "/assets/img/icon-512.png", "image": SITE + "/assets/img/icon-512.png", "priceRange": "₹₹",
            "address": {"@type": "PostalAddress", "streetAddress": ADDR1 + ", Sector 7, Rohini", "addressLocality": "Delhi", "addressRegion": "Delhi", "postalCode": "110085", "addressCountry": "IN"},
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "07:00", "closes": "19:00"}],
            "areaServed": [{"@type": "Place", "name": a["name"] + ", Delhi"} for a in AREAS] + [{"@type": "AdministrativeArea", "name": "Delhi NCR"}],
            "hasMap": MAPS, "sameAs": [u for _, u in SOCIAL]}

def org_schema(ed):
    return {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Legal Khata", "url": SITE + home(ed), "telephone": PHONE, "email": EMAIL,
            "areaServed": ed["name"] if ed["code"] != "global" else "Worldwide", "parentOrganization": {"@id": SITE + "/#office"}}

def form_options(ed):
    if ed["code"] == "in": return [s["name"] for s in SERVICES]
    return [s["name"] for s in ed["services"]] + ["Indian tax return or NRI matter", "Company setup in India"]

_fid = [0]
def lead_form(ed, heading, sub, selected=None, tag="h2"):
    _fid[0] += 1; f = "q%d" % _fid[0]
    india = ed["code"] == "in"
    opts = "".join('<option%s>%s</option>' % (" selected" if o == selected else "", e(o)) for o in form_options(ed))
    return f'''<aside class="khata" id="query">
<{tag}>{e(heading)}</{tag}><p class="muted small">{e(sub)}</p>
<form class="lead" novalidate>
<label for="{f}n">Your name<input id="{f}n" name="name" autocomplete="name" required></label>
<label for="{f}p">Phone or WhatsApp number<input id="{f}p" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="{'10-digit mobile number' if india else 'Include your country code'}" required></label>
{'' if india else f'<label for="{f}e">Email<input id="{f}e" name="email" type="email" autocomplete="email"></label>'}
<label for="{f}s">What do you need help with?<select id="{f}s" name="service"><option value="">Choose a service</option>{opts}<option>Something else</option></select></label>
<label for="{f}m">Anything we should know (optional)<textarea id="{f}m" name="message" rows="2"></textarea></label>
<label class="hp" for="{f}c">Leave this empty<input id="{f}c" name="company_site" tabindex="-1" autocomplete="off"></label>
<input type="hidden" name="edition" value="{ed['code']}"><input type="hidden" name="country" value="{e(ed['name'])}">
<p class="err" role="alert" hidden></p>
<button class="btn" type="submit">Get a free call back</button>
<p class="note">No charge for the first consultation. We use your details only to reply to this query.</p>
</form></aside>'''

def wa_href(text="Hello Legal Khata, I have a query."):
    return "https://wa.me/%s?text=%s" % (WA, text.replace(" ", "%20").replace(",", "%2C"))

def cta_row(ed, primary="Send a free query"):
    return f'<div class="cta-row"><a class="btn" href="#query">{primary}</a><a class="btn ghost" href="tel:{PHONE}">{I_PHONE}Call {PHONE_SHOW}</a><a class="btn wa" href="{wa_href()}" target="_blank" rel="noopener">{I_WA}WhatsApp</a></div>'

def band(ed, title, text):
    return f'<section class="band"><div class="wrap"><div class="stack"><h2>{e(title)}</h2><p>{e(text)}</p></div><div class="cta-row"><a class="btn" href="{p(ed, "contact")}">Send a free query</a><a class="btn ghost" href="tel:{PHONE}">{I_PHONE}{PHONE_SHOW}</a><a class="btn wa" href="{wa_href()}" target="_blank" rel="noopener">{I_WA}WhatsApp</a></div></div></section>'

def office_block(heading="Visit our office in Rohini, Delhi"):
    m = "" if PREVIEW else '<iframe title="Map showing the Legal Khata office in Sector 7, Rohini" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=D-13%2F171%2C+Second+Floor%2C+Sector+7%2C+Rohini%2C+Delhi+110085&amp;output=embed"></iframe>'
    if PREVIEW: m = '<div class="callout"><p><strong>Google Map</strong></p><p class="muted">On the live site an interactive Google Map of the Sector 7 office appears here.</p></div>'
    return f'''<section class="sec alt"><div class="wrap office"><div class="stack">
<h2>{e(heading)}</h2>
<address><strong>Legal Khata</strong><br>{ADDR1}<br>{ADDR2}</address>
<dl><dt>Phone</dt><dd><a href="tel:{PHONE}">{PHONE_SHOW}</a></dd><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd><dt>Hours</dt><dd>Monday to Saturday, 7:00 AM to 7:00 PM</dd><dt>Metro</dt><dd>Rohini West and Rohini East, Red Line</dd></dl>
<div class="cta-row" style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn" href="{MAPS}" target="_blank" rel="noopener">Get directions</a><a class="btn ghost" href="tel:{PHONE}">{I_PHONE}Call the office</a></div>
</div><div>{m}</div></div></section>'''

# ---------------------------------------------------------------- chrome
def header(pg):
    ed = pg["ed"]; india = ed["code"] == "in"
    if india:
        cols = "".join('<div><p class="col-label">%s</p>%s</div>' % (dict(GROUPS)[g], "".join('<a href="/%s">%s</a>' % (s, e(SVC[s]["name"])) for s in MENU_SERVICES[g])) for g in ("setup", "reg", "tax"))
        nav = f'''<a href="/">Home</a>
<details><summary>Services</summary><div class="drop">{cols}<a class="all" href="/services">See all services</a></div></details>
<details><summary>Delhi areas</summary><div class="drop two">{"".join('<a href="/%s">%s</a>' % (a["slug"], e(a["name"])) for a in AREAS)}</div></details>
<a href="/due-dates">Due dates</a><a href="/about">About</a><a href="/contact">Contact</a>'''
    else:
        loc = "".join('<a href="%s">%s</a>' % (p(ed, s["slug"]), e(s["name"])) for s in ed["services"])
        nav = f'''<a href="{home(ed)}">Home</a>
<details><summary>Services</summary><div class="drop two">{loc}<a class="all" href="{p(ed, "services")}">See all services</a></div></details>
<a href="{p(ed, "india-services")}">India services for NRIs</a><a href="{p(ed, "about")}">About</a><a href="{p(ed, "contact")}">Contact</a>'''
    links = ""
    for x in EDITIONS:
        href = ALT.get(pg["alt"], {}).get(x["code"]) if pg["alt"] else None
        href = href or home(x)
        cur = ' aria-current="true"' if x is ed else ""
        links += f'<a href="{href}" data-edition-link="{x["code"]}" data-name="{e(x["name"])}"{cur}><b>{CHIP.get(x["code"], x["code"].upper())}</b>{e(x["name"])}</a>'
    country = f'<details class="country"><summary aria-label="Choose your country. Current: {e(ed["name"])}">{I_GLOBE}{e(ed["short"])}</summary><div class="drop"><p>Choose your country. Services, tax terms and contact options change to match.</p>{links}</div></details>'
    strip_mid = "Serving Rohini, North Delhi and all Delhi NCR" if india else "Serving clients in %s from our Delhi office" % e(ed["the"] if ed["code"] != "global" else "every country")
    hours = "Mon to Sat: 7:00 AM to 7:00 PM" if india else "Mon to Sat, 7 AM to 7 PM India time"
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap"><span class="hours">{hours}</span><span>{strip_mid}</span><span><a href="tel:{PHONE}">{PHONE_SHOW}</a></span></div></div>
<div class="geo" hidden><div class="wrap"><span></span><a href="/"></a><button type="button">Stay on this site</button></div></div>
<header class="head"><div class="wrap">
<a class="brand" href="{home(ed)}" aria-label="Legal Khata home"><img src="/assets/img/logo.png" alt="Legal Khata: GST, income tax, registration" width="516" height="173"></a>
<button class="btn ghost sm menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Main">{nav}{country}<a class="btn sm" href="{p(ed, "contact")}">Free query</a></nav>
</div></header>'''

def footer(ed):
    india = ed["code"] == "in"
    if india:
        c1 = "".join('<li><a href="/%s">%s</a></li>' % (s["slug"], e(s["name"])) for s in SERVICES[:9])
        c2 = "".join('<li><a href="/%s">%s</a></li>' % (s["slug"], e(s["name"])) for s in SERVICES[9:])
        c3 = "".join('<li><a href="/%s">%s</a></li>' % (a["slug"], e(a["name"])) for a in AREAS[:8])
        cols = f'<div><p class="col-label">Services</p><ul>{c1}</ul></div><div><p class="col-label">More services</p><ul>{c2}</ul></div><div><p class="col-label">Areas we serve</p><ul>{c3}<li><a href="/services#areas">All Delhi areas</a></li></ul></div>'
    else:
        c1 = "".join('<li><a href="%s">%s</a></li>' % (p(ed, s["slug"]), e(s["name"])) for s in ed["services"])
        c2 = "".join('<li><a href="%s">%s</a></li>' % (p(ed, "india-services"), e(n)) for n, _ in NRI_SERVICES[:5])
        c3 = "".join('<li><a href="%s" data-edition-link="%s" data-name="%s">%s</a></li>' % (home(x), x["code"], e(x["name"]), e(x["name"])) for x in EDITIONS if x is not ed)
        cols = f'<div><p class="col-label">{e(ed["short"])} services</p><ul>{c1}</ul></div><div><p class="col-label">India services</p><ul>{c2}</ul></div><div><p class="col-label">Other countries</p><ul>{c3}</ul></div>'
    return f'''<footer class="foot"><div class="wrap">
<div class="foot-cols"><div class="stack"><img class="foot-logo" src="/assets/img/logo-white.png" alt="Legal Khata" width="516" height="173"><p>{ADDR1}<br>{ADDR2}{"" if india else "<br>India"}</p>
<p><a href="tel:{PHONE}">{PHONE_SHOW}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p><p>Monday to Saturday, 7:00 AM to 7:00 PM{"" if india else " India time"}</p>
<p class="social">{"".join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, n) for n, u in SOCIAL)}</p></div>{cols}</div>
<div class="legal"><span>© {date.today().year} Legal Khata. All rights reserved.</span><span><a href="{p(ed, "about")}">About</a> &nbsp; <a href="{p(ed, "contact")}">Contact</a> &nbsp; <a href="/privacy-policy">Privacy policy</a></span></div>
</div></footer>
<a class="wa-float" href="{wa_href()}" target="_blank" rel="noopener" aria-label="Chat with Legal Khata on WhatsApp">{I_WA}WhatsApp us</a>
<nav class="bar" aria-label="Quick contact"><a href="tel:{PHONE}">{I_PHONE}Call</a><a class="w" href="{wa_href()}" target="_blank" rel="noopener">{I_WA}WhatsApp</a><a class="q" href="{p(ed, "contact")}">Free query</a></nav>'''

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&amp;family=Public+Sans:wght@400;550;650&amp;display=swap">'

def render(pg):
    ed = pg["ed"]; url = SITE + pg["path"]
    alts = ""
    if pg["alt"]:
        for x in EDITIONS:
            h = ALT[pg["alt"]].get(x["code"])
            if h: alts += '<link rel="alternate" hreflang="%s" href="%s">\n' % ("x-default" if x["code"] == "global" else x["lang"], SITE + h)
    schema = "".join('<script type="application/ld+json">%s</script>\n' % json.dumps(s, ensure_ascii=False) for s in pg["schema"])
    body = header(pg) + '\n<main id="main">\n' + pg["body"] + "\n</main>\n" + footer(ed)
    flag = '<script>window.LK_PREVIEW=true;document.documentElement.setAttribute("data-edition","%s")</script>' % ed["code"] if PREVIEW else ""
    if PREVIEW and not OFFLINE and pg["path"] == "/":
        return f'<title>Legal Khata Website Preview</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n<link rel="stylesheet" href="/assets/site.css">\n{body}\n{flag}<script src="/assets/site.js"></script>\n'
    return f'''<!doctype html>
<html lang="{ed['lang']}" data-edition="{ed['code']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(pg['title'])}</title>
<meta name="description" content="{e(pg['desc'])}">
<meta name="robots" content="{'noindex,follow' if pg['noindex'] else 'index,follow'}">
<link rel="canonical" href="{url}">
{alts}<meta property="og:type" content="website">
<meta property="og:site_name" content="Legal Khata">
<meta property="og:title" content="{e(pg['title'])}">
<meta property="og:description" content="{e(pg['desc'])}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#0f2233">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:image" content="https://legalkhata.com/assets/img/icon-512.png">
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
{schema}<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-T9FVQDH');</script>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-T9FVQDH" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
{body}
{flag}<script src="/assets/site.js" defer></script>
</body>
</html>
'''

# ---------------------------------------------------------------- India pages
def ledger_india():
    out = '<div class="ledger">'
    for g, gname in GROUPS:
        rows = "".join('<a href="/%s"><strong>%s</strong><span>%s</span></a>' % (s["slug"], e(s["name"]), e(s["short"])) for s in SERVICES if s["group"] == g)
        out += '<div class="ledger-group"><h3>%s</h3><div class="ledger-rows">%s</div></div>' % (gname, rows)
    return out + "</div>"

def area_chips(): return '<ul class="chips">%s</ul>' % "".join('<li><a href="/%s">%s</a></li>' % (a["slug"], e(a["name"])) for a in AREAS)
HOW = [("Tell us what you need", "Call, WhatsApp or send the query form. The first consultation is free."),
       ("Get a fixed quote", "We list the documents required and quote the fee in writing before starting."),
       ("Share your documents", "Send them on WhatsApp or email, or hand them over at the office."),
       ("We file and report back", "You get the acknowledgement, certificate or return, and reminders for what comes next.")]
def how_html(): return '<ol class="how">%s</ol>' % "".join("<li><h3>%s</h3><p class='muted'>%s</p></li>" % (e(a), e(b)) for a, b in HOW)
def quotes(n=4): return '<div class="grid2">%s</div>' % "".join('<blockquote class="quote" style="margin:0"><p>%s</p><cite>%s</cite></blockquote>' % (e(t), e(w)) for t, w in TESTIMONIALS[:n])

def build_india():
    ed = IN
    # home
    body = f'''<section class="hero"><div class="wrap"><div class="stack-lg">
<h1>GST, income tax and company registration services in Rohini, Delhi</h1>
<p class="lede">Legal Khata is a business, tax and compliance consultancy in Sector 7, Rohini. We register your business, file your returns on time and keep your books in order, for a fixed fee agreed before we start.</p>
<ul class="facts"><li>Office in Sector 7, Rohini, near Rohini West metro</li><li>Open Monday to Saturday, 7 AM to 7 PM</li><li>Free first consultation</li><li>Documents accepted on WhatsApp</li></ul>
{cta_row(ed)}</div>
{lead_form(ed, "Send a free query", "Tell us what you need. We call back during office hours, usually the same day.")}
</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>What we handle for businesses and individuals in Delhi</h2><p class="muted">Each service has its own page with the documents required, the steps and the usual time taken.</p></div>{ledger_india()}</div></section>
<section class="sec green"><div class="wrap"><div class="sec-head"><h2>How working with us goes</h2></div>{how_html()}</div></section>
<section class="sec" id="areas"><div class="wrap"><div class="sec-head"><h2>A local tax and compliance team for Rohini and North Delhi</h2><p class="muted">Clients in Rohini, Pitampura, Netaji Subhash Place and Shalimar Bagh can walk in or ask for a visit. The rest of Delhi NCR works with us online, with document pickup when needed.</p></div>{area_chips()}</div></section>
<section class="sec alt"><div class="wrap"><div class="sec-head"><h2>What our clients say</h2></div>{quotes()}</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>Questions people ask before they call</h2></div>{faq_html(HOME_FAQS)}</div></section>
{office_block()}
{band(ed, "Have a notice, a deadline or a new business to register?", "Send the details now and a member of our team will call you back.")}'''
    add(ed, "/", "GST, ITR & Company Registration in Rohini, Delhi | Legal Khata",
        "Tax and compliance consultants in Sector 7, Rohini, Delhi. GST registration and returns, income tax returns, company registration, trademark and accounting. Free first consultation. Call +91 70489 15155.",
        body, alt="home", schema=[office_schema(), faq_schema(HOME_FAQS), {"@context": "https://schema.org", "@type": "WebSite", "name": "Legal Khata", "url": SITE + "/"}])

    # services index
    body = f'''<section class="hero slim"><div class="wrap"><div class="stack-lg">{crumb_html([("Home", "/"), ("Services", None)])}
<h1>Tax, registration and accounting services in Rohini, Delhi</h1><p class="lede">Registrations, tax returns, company compliance and accounting from one office in Sector 7, Rohini. Choose a service to see the documents, steps and timelines.</p>{cta_row(ed)}</div>
{lead_form(ed, "Not sure which service you need?", "Describe your situation and we will point you to the right one.")}</div></section>
<section class="sec"><div class="wrap">{ledger_india()}</div></section>
<section class="sec green" id="areas"><div class="wrap"><div class="sec-head"><h2>Areas of Delhi we serve</h2></div>{area_chips()}</div></section>
{band(ed, "Talk to our team today", "The first consultation is free and there is no obligation.")}'''
    add(ed, "/services", "GST, Tax & Registration Services in Rohini, Delhi | Legal Khata",
        "All services from Legal Khata, Rohini: GST, income tax, TDS, company and LLP registration, trademark, FSSAI, MSME, ROC filing and bookkeeping.", body, alt="services",
        schema=[crumb_schema([("Home", "/"), ("Services", None)], "/services")])

    # service pages
    for s in SERVICES:
        path = "/" + s["slug"]; crumbs = [("Home", "/"), ("Services", "/services"), (s["name"], None)]
        related = [x for x in SERVICES if x["group"] == s["group"] and x is not s][:4]
        if len(related) < 3: related += [x for x in SERVICES if x["slug"] in ("gst-registration", "income-tax-return", "accounting-bookkeeping") and x is not s and x not in related][:3 - len(related)]
        hero_img = SERVICE_HERO_IMAGES.get(s["slug"])
        hero_visual = f'<img class="hero-photo" src="{hero_img[0]}" alt="{e(hero_img[1])}" width="{hero_img[2]}" height="{hero_img[3]}" loading="eager">' if hero_img else ""
        body = f'''<section class="hero slim"><div class="wrap"><div class="stack-lg">{crumb_html(crumbs)}
<h1>{e(s["name"])} in Rohini, Delhi</h1><p class="lede">{e(s["short"])}</p>{cta_row(ed, "Get a quote for this")}</div><div>{hero_visual}</div></div></section>
<section class="sec"><div class="wrap two"><div class="prose">
<p>{e(s["intro"])}</p>
<h2>What we handle</h2>{ul(s["handle"])}
<h2>Documents you need</h2>{ul(s["docs"])}<p class="muted small">Requirements vary with the type of business. We send you an exact checklist after a short call.</p>
<h2>How the process works</h2><ol class="steps">{"".join("<li><span>%s</span></li>" % e(x) for x in s["steps"])}</ol>
<h2>How long it takes</h2><p>{e(s["time"])}</p>
<div class="callout"><p><strong>Fees.</strong> We quote a fixed professional fee before starting, with government fees shown separately. Call <a href="tel:{PHONE}">{PHONE_SHOW}</a> or send the form for today's quote.</p></div>
<h2>Frequently asked questions</h2>{faq_html(s["faqs"])}
<h2>Related services</h2><ul class="chips" style="padding:0">{"".join('<li><a href="/%s">%s</a></li>' % (x["slug"], e(x["name"])) for x in related)}</ul>
<p class="muted small">Legal Khata, {ADDR1}, {ADDR2}. Serving Rohini, Pitampura, Netaji Subhash Place, Shalimar Bagh and all Delhi NCR.</p>
</div><div class="side">{lead_form(ed, "Ask about " + s["name"], "Free consultation. We reply during office hours.", selected=s["name"], tag="h3")}</div></div></section>
{band(ed, "Start your " + s["name"].lower().replace("gst", "GST").replace("llp", "LLP").replace("roc", "ROC").replace("tds", "TDS").replace("fssai", "FSSAI").replace("msme", "MSME").replace("cma", "CMA").replace("(iec)", "(IEC)").replace("(dsc)", "(DSC)").replace("udyam", "Udyam") + " today", "Send your details and we will call you with the document list and fee.")}'''
        add(ed, path, "%s in Rohini, Delhi | Legal Khata" % s["name"],
            "%s Legal Khata, Sector 7, Rohini, Delhi. Free first consultation: %s." % (s["short"], PHONE_SHOW), body,
            schema=[crumb_schema(crumbs, path), faq_schema(s["faqs"]),
                    {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["short"], "provider": {"@id": SITE + "/#office"}, "areaServed": ["Rohini", "Delhi", "Delhi NCR"], "url": SITE + path}])

    # area pages
    top = ["gst-registration", "gst-return-filing", "income-tax-return", "company-registration", "trademark-registration", "accounting-bookkeeping", "tds-return", "roc-annual-filing"]
    for a in AREAS:
        path = "/" + a["slug"]; n = a["name"]; crumbs = [("Home", "/"), ("Delhi areas", "/services#areas"), (n, None)]
        rohini = n == "Rohini"
        faqs = [("Is there a GST and income tax consultant near me in %s?" % n, ("Yes. Legal Khata's office is at %s, %s, open Monday to Saturday from 7 AM to 7 PM." % (ADDR1, ADDR2)) if rohini else ("Legal Khata serves %s from its office in Sector 7, Rohini. %s" % (n, a["travel"]))),
                ("Can I get GST registration and ITR filing done in %s without visiting an office?" % n, "Yes. Send your documents on WhatsApp or email. We prepare everything, take your approval and file online. A visit is needed only if you prefer one."),
                ("Do you visit clients in %s?" % n, "Yes, by appointment. For regular accounting work we can arrange a visiting accountant or document pickup, depending on the volume of work.")]
        near = [x for x in AREAS if x is not a][:6] if rohini else [AREAS[0]] + [x for x in AREAS[1:] if x is not a][:5]
        rows = "".join('<a href="/%s"><strong>%s in %s</strong><span>%s</span></a>' % (s, e(SVC[s]["name"]), e(n), e(SVC[s]["short"])) for s in top)
        extra = ('<h2>Walk in to our Sector 7 office</h2><p>We are on the second floor of D-13/171, Sector 7, a short ride from Rohini West and Rohini East metro stations on the Red Line and close to the Sector 7 and Sector 8 markets. Shop owners from the Rohini district centres, residents of the group housing societies and professionals from every sector use the office for same-day document drop and signing.</p>' if rohini else
                 f'<h2>How we serve {e(n)} from Rohini</h2><p>{e(a["travel"])} The nearest metro for most of the area is {e(a["metro"])}. Documents travel by WhatsApp and email, and originals are collected when a filing needs them.</p>')
        body = f'''<section class="hero"><div class="wrap"><div class="stack-lg">{crumb_html(crumbs)}
<h1>GST, income tax and company registration services in {e(n)}, Delhi</h1>
<p class="lede">{"Legal Khata is based in Sector 7, Rohini." if rohini else "Legal Khata serves " + e(n) + " from its office in Sector 7, Rohini."} We cover {e(a["localities"])}.</p>
<ul class="facts"><li>Free first consultation</li><li>Fixed fee quoted before work starts</li><li>Documents accepted on WhatsApp</li><li>{"Walk in Monday to Saturday" if rohini else "Visits and pickup by appointment"}</li></ul>
{cta_row(ed)}</div>{lead_form(ed, "Free query for " + n + " clients", "We call back during office hours, usually the same day.")}</div></section>
<section class="sec"><div class="wrap"><div class="prose" style="max-width:76ch">
<h2 style="margin-top:0">Accounting and tax help for {e(n)}</h2><p>{e(a["mix"])}</p>
<p>Whether you run a shop, a clinic, a consultancy or a company, or you are a salaried person with a return to file, you deal with one team that knows your file and reminds you before each due date.</p>{extra}</div></div></section>
<section class="sec green"><div class="wrap"><div class="sec-head"><h2>Services most requested in {e(n)}</h2></div><div class="ledger"><div class="ledger-rows">{rows}</div></div><p style="margin-top:18px"><a href="/services">See all services</a></p></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>Questions from {e(n)} clients</h2></div>{faq_html(faqs)}</div></section>
<section class="sec alt"><div class="wrap"><div class="sec-head"><h2>Nearby areas we also serve</h2></div><ul class="chips">{"".join('<li><a href="/%s">%s</a></li>' % (x["slug"], e(x["name"])) for x in near)}</ul></div></section>
{office_block("Our office in Rohini, Delhi")}'''
        add(ed, path, "GST, ITR & Accounting Services in %s, Delhi | Legal Khata" % n,
            "Tax and compliance services in %s, Delhi: GST registration and returns, income tax returns, company registration and bookkeeping from Legal Khata, Rohini. Call %s." % (n, PHONE_SHOW), body,
            schema=[office_schema(), crumb_schema(crumbs, path), faq_schema(faqs)])

    # due dates
    rows = "".join("<tr><td>%s</td><td><strong>%s</strong></td><td>%s</td></tr>" % (e(a), e(b), e(c)) for a, b, c in DUE_DATES)
    crumbs = [("Home", "/"), ("Due dates", None)]
    body = f'''<section class="hero slim"><div class="wrap"><div class="stack-lg">{crumb_html(crumbs)}<h1>GST, income tax, TDS and ROC due dates</h1>
<p class="lede">The statutory dates that recur every year for Indian businesses. The government often extends individual deadlines, so call us to confirm the date for the current period.</p>{cta_row(ed, "Ask us to track your dates")}</div>
{lead_form(ed, "Never miss a due date", "We send reminders and file before the deadline.")}</div></section>
<section class="sec"><div class="wrap"><div class="scroll"><table class="dates"><thead><tr><th>Due date</th><th>Compliance</th><th>Applies to</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="muted small" style="margin-top:16px">Dates falling on a holiday and dates changed by notification may differ. This page is general information and not advice for a specific case.</p></div></section>
{band(ed, "Behind on a return?", "We clear pending GST, TDS, ITR and ROC filings and work out the late fee before you pay.")}'''
    add(ed, "/due-dates", "GST, Income Tax, TDS & ROC Due Dates | Legal Khata, Rohini", "Compliance calendar for Indian businesses: GSTR-1, GSTR-3B, TDS, advance tax, income tax return and ROC annual filing due dates.", body, schema=[crumb_schema(crumbs, "/due-dates")])

    # about
    crumbs = [("Home", "/"), ("About", None)]
    body = f'''<section class="hero slim"><div class="wrap"><div class="stack-lg">{crumb_html(crumbs)}<h1>About Legal Khata, tax and compliance consultants in Rohini</h1>
<p class="lede">A khata is the account book a business is run from. We named the practice after it because keeping that book right is the job: registrations done properly, returns filed on time and accounts that tell the owner the truth.</p>{cta_row(ed)}</div>
{lead_form(ed, "Talk to us", "The first consultation is free.")}</div></section>
<section class="sec"><div class="wrap"><div class="prose">
<h2 style="margin-top:0">Who we are</h2><p>Legal Khata is a business, tax and compliance consultancy working from Sector 7, Rohini, Delhi. Our team handles business registration, GST, income tax, TDS, company law compliance and bookkeeping for shop owners, professionals, start-ups, companies and salaried individuals.</p>
<h2>How we work</h2>{ul(["You get a fixed quote in writing before any work starts.", "One person is responsible for your file and answers your calls.", "Documents can be sent on WhatsApp or email, or handed over at the office.", "We remind you before each due date instead of after it.", "You receive a copy of every acknowledgement, challan and certificate."])}
<h2>Who we work with</h2><p>Most of our clients are in Rohini, Pitampura, Netaji Subhash Place, Shalimar Bagh and the rest of Delhi NCR. We also file Indian returns for NRIs and provide accounting and tax support to clients in other countries. Use the country button at the top of the page to see those services.</p>
<h2>What clients say</h2></div>{quotes()}</div></section>
{office_block()}'''
    add(ed, "/about", "About Legal Khata | Tax & Compliance Consultants in Rohini, Delhi", "Legal Khata is a business, tax and compliance consultancy in Sector 7, Rohini, Delhi. GST, income tax, company registration and accounting.", body, alt="about",
        schema=[office_schema(), crumb_schema(crumbs, "/about")])

    # contact
    crumbs = [("Home", "/"), ("Contact", None)]
    body = f'''<section class="hero"><div class="wrap"><div class="stack-lg">{crumb_html(crumbs)}<h1>Contact Legal Khata in Rohini, Delhi</h1>
<p class="lede">Send the form, call or WhatsApp. We reply during office hours, Monday to Saturday, 7:00 AM to 7:00 PM.</p>
<div class="cta-row"><a class="btn ghost" href="tel:{PHONE}">{I_PHONE}Call {PHONE_SHOW}</a><a class="btn wa" href="{wa_href()}" target="_blank" rel="noopener">{I_WA}WhatsApp us</a><a class="btn ghost" href="mailto:{EMAIL}">Email us</a></div>
<p class="muted">{EMAIL}</p></div>{lead_form(ed, "Send a free query", "Tell us what you need and the best number to reach you.")}</div></section>
{office_block()}
<section class="sec"><div class="wrap"><div class="sec-head"><h2>Before you get in touch</h2></div>{faq_html(HOME_FAQS[:5])}</div></section>'''
    add(ed, "/contact", "Contact Legal Khata | Office in Sector 7, Rohini, Delhi", "Call +91 70489 15155 or visit Legal Khata at D-13/171, Second Floor, Sector 7, Rohini, Delhi 110085. Open Monday to Saturday, 7 AM to 7 PM.", body, alt="contact",
        schema=[office_schema(), crumb_schema(crumbs, "/contact")])

    # privacy
    body = f'''<section class="sec"><div class="wrap"><div class="prose"><h1>Privacy policy</h1>
<p>This policy explains how Legal Khata handles information you send through this website.</p>
<h2>What we collect</h2><p>When you send a query we collect your name, phone number, email address if given, the service you chose, your message and the page you sent it from. Our hosting provider also records your approximate country.</p>
<h2>How we use it</h2><p>We use these details only to reply to your query and to provide the services you ask for. We do not sell or rent your information.</p>
<h2>Who sees it</h2><p>Your query is stored in our practice management system and emailed to our office. Documents you share for filing are submitted to the relevant government portal on your instructions.</p>
<h2>Keeping and deleting it</h2><p>We keep query details for as long as needed to respond and, for clients, for the period professional and tax rules require. To ask for correction or deletion, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>Legal Khata, {ADDR1}, {ADDR2}. Phone {PHONE_SHOW}.</p></div></div></section>'''
    add(ed, "/privacy-policy", "Privacy Policy | Legal Khata", "How Legal Khata collects, uses and protects information you share through this website, forms and WhatsApp.", body)
    body = f'''<section class="sec"><div class="wrap"><div class="prose"><h1>We could not find that page</h1><p>The page may have moved. These links cover most of what people look for.</p>
<ul><li><a href="/">Home</a></li><li><a href="/services">All services</a></li><li><a href="/contact">Contact us</a></li></ul>{cta_row(ed, "Send a free query")}</div></div></section>
<section class="sec green"><div class="wrap"><div style="max-width:460px">{lead_form(ed, "Send a free query", "Tell us what you were looking for.")}</div></div></section>'''
    add(ed, "/404", "Page not found | Legal Khata", "Page not found.", body, noindex=True)

# ---------------------------------------------------------------- country editions
WORLD_HOW = [("Tell us what you need", "Send the form or message us on WhatsApp. We reply within one working day."),
             ("Agree scope and a fixed fee", "You get a written scope, timeline and fee in your currency before work begins."),
             ("Share access and documents", "We work inside your accounting software or from documents you upload."),
             ("Review and file", "You review the finished work. Filing is done by you or your local adviser, or by us in India.")]

def build_world(ed):
    g = ed["code"] == "global"; name = ed["the"] if not g else "your country"; short = ed["short"]
    gen_faqs = [("How do we work together across time zones?", "Our office works 7 AM to 7 PM India time, Monday to Saturday. We agree a reply window that overlaps with your day, and handle everything by email, WhatsApp and video call."),
                ("How are fees quoted and paid?", "We quote a fixed fee in %s before starting. Payment is by international bank transfer or card." % ed["currency"])]
    def ledger():
        return '<div class="ledger"><div class="ledger-rows">%s</div></div>' % "".join('<a href="%s"><strong>%s</strong><span>%s</span></a>' % (p(ed, s["slug"]), e(s["name"]), e(s["short"])) for s in ed["services"])
    def nri_ledger(n=8):
        return '<div class="ledger"><div class="ledger-rows">%s</div></div>' % "".join('<a href="%s"><strong>%s</strong><span>%s</span></a>' % (p(ed, "india-services"), e(a), e(b)) for a, b in NRI_SERVICES[:n])
    how = '<ol class="how">%s</ol>' % "".join("<li><h3>%s</h3><p class='muted'>%s</p></li>" % (e(a), e(b)) for a, b in WORLD_HOW)
    hours = '<p class="muted">Our team is online 7 AM to 7 PM India time, Monday to Saturday.<span data-local-hours></span></p>'
    h1 = "Accounting and tax support in %s, and Indian tax help for %s" % (ed["the"], ed["people"]) if not g else "Indian tax help for NRIs and outsourced accounting, wherever you live"
    faqs = NRI_FAQS[:2] + gen_faqs + [ed["services"][0]["faq"]]
    body = f'''<section class="hero"><div class="wrap"><div class="stack-lg"><h1>{e(h1)}</h1><p class="lede">{e(ed["intro"])}</p>
<ul class="facts"><li>Dedicated accounts and tax team in Delhi</li><li>Fixed fee quoted in {e(ed["currency"])}</li><li>Works in {e(ed["software"])}</li><li>Reply within one working day</li></ul>
{cta_row(ed)}{hours}</div>{lead_form(ed, "Send a free query", "Tell us what you need. We reply within one working day.")}</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>{"Services for businesses in " + e(ed["the"]) if not g else "Services for businesses and accounting firms"}</h2><p class="muted">{e(ed["how"])}</p></div>{ledger()}</div></section>
<section class="sec green"><div class="wrap"><div class="sec-head"><h2>Indian tax and compliance for {e(ed["people"])}</h2><p class="muted">{e(ed["nri"])}</p></div>{nri_ledger()}</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>How working with us goes</h2></div>{how}</div></section>
<section class="sec alt"><div class="wrap"><div class="sec-head"><h2>Common questions</h2></div>{faq_html(faqs)}</div></section>
{band(ed, "Tell us what you need", "A short message is enough to start. We reply with scope, timeline and a fixed fee.")}'''
    add(ed, home(ed), ("Accounting & Tax Services in %s | Legal Khata" % short) if not g else "NRI Tax Services & Outsourced Accounting Worldwide | Legal Khata",
        ed["intro"], body, alt="home", schema=[org_schema(ed), faq_schema(faqs)])

    crumbs = [("Home", home(ed)), ("Services", None)]
    body = f'''<section class="hero slim"><div class="wrap"><div class="stack-lg">{crumb_html(crumbs)}<h1>{"Accounting and tax services in " + e(ed["the"]) if not g else "Services for clients worldwide"}</h1><p class="lede">{e(ed["how"])}</p>{cta_row(ed)}</div>
{lead_form(ed, "Not sure what you need?", "Describe your situation and we will suggest the right service.")}</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>{e(short)} services</h2></div>{ledger()}</div></section>
<section class="sec green"><div class="wrap"><div class="sec-head"><h2>India services</h2><p class="muted">{e(ed["nri"])}</p></div>{nri_ledger()}</div></section>
{band(ed, "Get a fixed quote", "Tell us what you need and we reply within one working day.")}'''
    add(ed, p(ed, "services"), "Accounting, Tax & Company Services in %s | Legal Khata" % short if not g else "Global Accounting & NRI Tax Services | Legal Khata",
        "Services from Legal Khata for clients in %s: bookkeeping, tax return preparation, company formation support and Indian tax for NRIs." % name, body, alt="services", schema=[crumb_schema(crumbs, p(ed, "services"))])

    for s in ed["services"]:
        path = p(ed, s["slug"]); crumbs = [("Home", home(ed)), ("Services", p(ed, "services")), (s["name"], None)]
        faqs = [s["faq"]] + gen_faqs
        others = [x for x in ed["services"] if x is not s]
        where = (" in " + ed["the"]) if not g and ed["short"] not in s["name"] and "UK" not in s["name"] and "Canada" not in s["name"] and "UAE" not in s["name"] else ""
        body = f'''<section class="hero slim"><div class="wrap"><div class="stack-lg">{crumb_html(crumbs)}<h1>{e(s["name"])}{e(where)}</h1><p class="lede">{e(s["short"])}</p>{cta_row(ed, "Get a quote for this")}</div><div></div></div></section>
<section class="sec"><div class="wrap two"><div class="prose"><p>{e(s["intro"])}</p>
<h2>What we handle</h2>{ul(s["handle"])}
<h2>What we need from you</h2>{ul(s["need"])}
<div class="callout"><p><strong>Who files.</strong> {e(ed["how"])}</p></div>
<h2>How the process works</h2><ol class="steps">{"".join("<li><span><strong>%s.</strong> %s</span></li>" % (e(a), e(b)) for a, b in WORLD_HOW)}</ol>
<h2>Frequently asked questions</h2>{faq_html(faqs)}
<h2>Related services</h2><ul class="chips" style="padding:0">{"".join('<li><a href="%s">%s</a></li>' % (p(ed, x["slug"]), e(x["name"])) for x in others)}<li><a href="{p(ed, "india-services")}">India services for NRIs</a></li></ul>
</div><div class="side">{lead_form(ed, "Ask about " + s["name"], "We reply within one working day.", selected=s["name"], tag="h3")}</div></div></section>
{band(ed, "Get a fixed quote", "Tell us about your business and we reply with scope, timeline and fee.")}'''
        add(ed, path, "%s%s | Legal Khata" % (s["name"], where), "%s %s" % (s["short"], "Fixed fee quoted in %s by Legal Khata, with a reply within one working day." % ed["currency"]), body,
            schema=[crumb_schema(crumbs, path), faq_schema(faqs), {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "description": s["short"], "provider": {"@id": SITE + "/#office"}, "areaServed": ed["name"] if not g else "Worldwide", "url": SITE + path}])

    crumbs = [("Home", home(ed)), ("India services", None)]; path = p(ed, "india-services")
    items = "".join("<h3>%s</h3><p>%s</p>" % (e(a), e(b)) for a, b in NRI_SERVICES)
    body = f'''<section class="hero slim"><div class="wrap"><div class="stack-lg">{crumb_html(crumbs)}<h1>Indian tax and compliance for {e(ed["people"])}</h1>
<p class="lede">Income tax returns, property sales, repatriation and company matters in India, handled from our Delhi office without you having to travel.</p>{cta_row(ed)}{hours}</div><div></div></div></section>
<section class="sec"><div class="wrap two"><div class="prose"><div class="callout"><p>{e(ed["nri"])}</p></div>
<h2>What we do for you in India</h2>{items}
<h2>What we usually need</h2>{ul(["PAN and passport copy", "Details of your stay in India during the year", "Indian bank statements, including NRE and NRO accounts", "Rent, interest, dividend and sale documents", "Form 26AS and AIS access, or your income tax portal login"])}
<h2>Frequently asked questions</h2>{faq_html(NRI_FAQS)}</div>
<div class="side">{lead_form(ed, "Ask about your India matter", "We reply within one working day.", selected="Indian tax return or NRI matter", tag="h3")}</div></div></section>
{band(ed, "Selling property or filing a return in India?", "Tell us the details early. Planning before the transaction usually saves the most tax.")}'''
    add(ed, path, ("NRI Tax Filing in India from %s | Legal Khata" % ("the " + short if short in ("USA","UK","UAE") else short)) if not g else "NRI Tax Filing in India from Abroad | Legal Khata",
        "Indian income tax returns, property sale TDS, Form 15CA and 15CB, and company compliance for %s. Handled online from Delhi." % ed["people"], body, alt="india-services",
        schema=[crumb_schema(crumbs, path), faq_schema(NRI_FAQS)])

    crumbs = [("Home", home(ed)), ("About", None)]
    body = f'''<section class="hero slim"><div class="wrap"><div class="stack-lg">{crumb_html(crumbs)}<h1>About Legal Khata</h1>
<p class="lede">A business, tax and accounting consultancy in Delhi, India, working with clients {"in " + e(ed["the"]) if not g else "around the world"}.</p>{cta_row(ed)}</div>{lead_form(ed, "Talk to us", "We reply within one working day.")}</div></section>
<section class="sec"><div class="wrap"><div class="prose"><h2 style="margin-top:0">What we do</h2><p>{e(ed["intro"])}</p>
<h2>How we work with overseas clients</h2><p>{e(ed["how"])}</p>{ul(["A written scope and fixed fee before work begins", "One named contact for your file", "Work done inside your own software, with access you control", "Replies within one working day"])}
<h2>Where we are</h2><p>{ADDR1}, {ADDR2}, India. Phone and WhatsApp {PHONE_SHOW}. Email {EMAIL}.</p>{hours}</div></div></section>
{band(ed, "Tell us what you need", "We reply with scope, timeline and a fixed fee.")}'''
    add(ed, p(ed, "about"), "About Legal Khata | Accounting & Tax Support for %s" % short, "Legal Khata is a business, tax and accounting consultancy in Delhi, India, supporting clients in %s." % name, body, alt="about", schema=[org_schema(ed), crumb_schema(crumbs, p(ed, "about"))])

    crumbs = [("Home", home(ed)), ("Contact", None)]
    body = f'''<section class="hero"><div class="wrap"><div class="stack-lg">{crumb_html(crumbs)}<h1>Contact Legal Khata from {e(ed["the"]) if not g else "anywhere"}</h1>
<p class="lede">Send the form or message us on WhatsApp. We reply within one working day.</p>
<div class="cta-row"><a class="btn wa" href="{wa_href()}" target="_blank" rel="noopener">{I_WA}WhatsApp {PHONE_SHOW}</a><a class="btn ghost" href="mailto:{EMAIL}">Email us</a><a class="btn ghost" href="tel:{PHONE}">{I_PHONE}Call</a></div>
<p class="muted">{EMAIL}</p>{hours}<p class="muted">Office: {ADDR1}, {ADDR2}, India.</p></div>{lead_form(ed, "Send a free query", "Include your country code so we can call or message you.")}</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>Before you get in touch</h2></div>{faq_html(gen_faqs + NRI_FAQS[2:])}</div></section>'''
    add(ed, p(ed, "contact"), "Contact Legal Khata | %s" % (ed["name"] if not g else "Worldwide"), "Contact Legal Khata for accounting, tax and NRI services in %s. WhatsApp %s." % (name, PHONE_SHOW), body, alt="contact", schema=[org_schema(ed), crumb_schema(crumbs, p(ed, "contact"))])

# ---------------------------------------------------------------- output
def out_file(path):
    if path.endswith("/"): return (path + "index.html").lstrip("/")
    return path.lstrip("/") + ".html"

def relink(doc, path):
    here = os.path.dirname(out_file(path))
    def fix(m):
        attr, target = m.group(1), m.group(2)
        frag = ""
        if "#" in target: target, frag = target.split("#", 1); frag = "#" + frag
        f = target.lstrip("/") if "." in target.rsplit("/", 1)[-1] else out_file(target)
        return '%s="%s%s"' % (attr, os.path.relpath(f, here or "."), frag)
    return re.sub(r'(href|src)="(/[^"]*)"', fix, doc)

def main():
    build_india()
    for c in COUNTRIES + [GLOBAL]: build_world(c)
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    for f in ("site.css", "site.js"): shutil.copy(os.path.join(ROOT, "..", "assets", f), os.path.join(OUT, "assets", f))
    shutil.copytree(os.path.join(ROOT, "..", "assets", "img"), os.path.join(OUT, "assets", "img"))
    if True:
        shutil.copy(os.path.join(ROOT, "..", "assets", "img", "favicon.ico"), os.path.join(OUT, "favicon.ico"))
        open(os.path.join(OUT, "site.webmanifest"), "w").write(json.dumps({"name": "Legal Khata", "short_name": "Legal Khata", "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}], "theme_color": "#0f2233", "background_color": "#ffffff", "display": "browser"}))
    for pg in PAGES:
        doc = render(pg)
        if PREVIEW: doc = relink(doc, pg["path"])
        f = os.path.join(OUT, out_file(pg["path"]))
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, "w", encoding="utf-8").write(doc)
    if not PREVIEW:
        urls = "".join("<url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n" % (SITE, pg["path"], TODAY) for pg in PAGES if not pg["noindex"])
        open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)
        open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: %s/sitemap.xml\n" % SITE)
        open(os.path.join(OUT, "_headers"), "w").write("/assets/*\n  Cache-Control: public, max-age=604800\n")
        # 301s for legacy URLs still indexed/linked from the pre-rebuild site, so they
        # consolidate into their current equivalents instead of diluting relevance/crawl budget.
        redirects = """/australia/Xero_Book_Keeper /au/bookkeeping 301
/australia/Xero_Book_Keeper.php /au/bookkeeping 301
/australia/bas-lodgement /au/bas-preparation 301
/australia/bookkeeping-reconciliation.php /au/bookkeeping 301
/australia/accounting-and-tax-support-services /au/services 301
/australia/contact.php /au/contact 301
/australia/* /au/ 301
/canada/index.php /ca/ 301
/canada/about.php /ca/about 301
/canada/bookkeeping.php /ca/bookkeeping 301
/canada/cra-business-number /ca/incorporation 301
/canada/cra-business-number.php /ca/incorporation 301
/canada/gst-hst /ca/gst-hst-returns 301
/canada/payroll.php /ca/bookkeeping 301
/canada/corporate-compliance.php /ca/corporate-tax-return 301
/canada/* /ca/ 301
/private-limited-registration.php /private-limited-registration 301
/trademark-registration.php /trademark-registration 301
/services.php /services 301
/contact.php /contact 301
/about.php /about 301
/opc-reg.php /opc-reg 301
"""
        open(os.path.join(OUT, "_redirects"), "w").write(redirects)
        open(os.path.join(OUT, "wrangler.jsonc"), "w").write(json.dumps({"name": "legalkhata", "compatibility_date": "2026-11-12", "assets": {"directory": "."}}, indent="\t") + "\n")
        open(os.path.join(OUT, ".assetsignore"), "w").write(".git\n.github\nwrangler.jsonc\n")
    print(len(PAGES), "pages ->", os.path.normpath(OUT))

main()
