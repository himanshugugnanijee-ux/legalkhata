# Legal Khata — Full Website Package

A complete, working PHP website: India section (`/in/`) and Australia section (`/au/`), a
functional country switcher, hreflang tags, and JSON-LD schema (Organization, ProfessionalService,
Service, FAQPage) on every page. All 18 pages have been syntax-checked and rendered successfully.

## Folder structure

```
/
├── index.php                 Landing page (country splash)
├── robots.txt
├── sitemap.xml
├── includes/
│   ├── header.php            Shared <head>, nav, hreflang, schema hooks
│   └── footer.php            Shared footer
├── assets/
│   ├── css/style.css         All site styling (ledger/paper-book design system)
│   └── js/main.js            Mobile menu + country switcher
├── in/                       India section
│   ├── index.php
│   ├── private-limited-company-registration.php
│   ├── llp-registration.php
│   ├── gst-registration.php
│   ├── income-tax-return-filing.php
│   ├── bookkeeping-accounting.php
│   ├── msme-udyam-registration.php
│   ├── about.php
│   └── contact.php
└── au/                        Australia section
    ├── index.php
    ├── bookkeeping-services.php
    ├── bas-lodgement.php
    ├── payroll-services.php
    ├── xero-bookkeeping.php
    ├── outsourced-bookkeeping-for-accountants.php
    ├── about.php
    └── contact.php
```

## How to upload (cPanel / FTP)

1. **Back up your current site first** — most hosts offer one-click backup in cPanel.
2. Open File Manager (or FTP with FileZilla) and go to your site root — usually `public_html`.
3. Upload every file and folder from this package into `public_html`, **keeping the folder structure exactly as-is**. This will replace your current `index.php`, `about.php`, `services.php`, etc. — that's intentional, this is the new site.
4. Confirm your host runs PHP 7.4 or newer (any standard shared host does — GoDaddy, Hostinger, Bluehost, etc. all support this by default).
5. Visit `https://www.legalkhata.com/` in a browser and click through both the India and Australia sections.

## Things you must do before this is fully live

1. **Contact forms have no backend yet.** Both `/in/contact.php` and `/au/contact.php` submit to
   `contact-handler.php`, which doesn't exist yet — that's intentional, since sending mail requires
   your host's mail settings. Easiest options:
   - Use a form service like Formspree or Web3Forms (free tier, just change the `action=""` URL) — no backend code needed.
   - Or ask your host/developer to add a 10-line PHP mail script using `PHPMailer`.
2. **Replace placeholder stats and testimonials** — the "10+ years," "2,500+ filings," and quoted
   testimonials are placeholders in the right format. Swap in your real numbers and real client
   quotes (with permission) before launch.
3. **Add a logo image.** The header currently uses a text "LK" mark. Drop a real logo into
   `assets/img/logo.png` and swap the `<span class="mark">LK</span>` in `includes/header.php` for
   an `<img>` tag once you have one.
4. **Google Search Console** — submit `sitemap.xml`, then use URL Inspection → Request Indexing on
   `/in/` and `/au/` first (your two most important pages).
5. **Phone/email/address** — double-check every instance of the phone number, email and India
   office address across the site is current.

## Extending this later

Every page follows the same pattern: set the PHP variables at the top (`$locale`, `$page_title`,
`$meta_desc`, `$canonical`, schema), then `include` the header, write your content sections using
the existing CSS classes (`.hero`, `.card`, `.service-list`, `.faq`, `.cta-banner`, etc.), then
`include` the footer. Copy any existing `/au/` page as a starting point for new Australia pages
(e.g. accounts-payable-receivable, EOFY cleanup, industry pages for tradies/NDIS), and copy `/in/`
pages the same way for new India pages (trademark registration, FSSAI, TDS return, etc.) — these
are listed in the original strategy document if you want the fuller roadmap.
