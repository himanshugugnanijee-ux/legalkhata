# Legal Khata — SEO & Site Architecture Plan
### Goal: Rank on Google in India (GST/company registration) AND Australia (bookkeeping), modeled on RegisterKaro.in

---

## 1. The single biggest fix: make the country switcher real

Right now "India / Australia / Canada" at the top is just text — it doesn't change the URL, so Google only ever indexes one blended page and can never rank it for country-specific searches.

**Fix: give each country its own URL folder.**

```
legalkhata.com/in/          → India homepage
legalkhata.com/in/gst-registration
legalkhata.com/in/private-limited-company-registration
...

legalkhata.com/au/          → Australia homepage
legalkhata.com/au/bookkeeping-services
legalkhata.com/au/bas-lodgement
...
```

The dropdown becomes a simple link: selecting "Australia" takes the user to `/au/` (or the AU-equivalent of the page they're on), instead of hiding/showing content with JavaScript.

**Then add hreflang tags** to every page so Google knows which version to show which searcher:

```html
<link rel="alternate" href="https://www.legalkhata.com/in/bookkeeping-services" hreflang="en-in" />
<link rel="alternate" href="https://www.legalkhata.com/au/bookkeeping-services" hreflang="en-au" />
<link rel="alternate" href="https://www.legalkhata.com/bookkeeping-services" hreflang="x-default" />
```

This single change is what lets you legitimately rank in both Google.co.in and Google.com.au — without it, no amount of content will get you ranking cleanly in both markets at once.

(Skip Canada for now — you have no dedicated services or content for it yet. A thin/empty country page hurts you more than it helps. Add it later once you have real Canada-specific offerings.)

---

## 2. Recommended page structure (India side)

Mirror RegisterKaro's depth — one URL per searchable service, not one page trying to cover everything:

**Company Incorporation**
- Private Limited Company Registration
- LLP Registration
- One Person Company Registration
- Partnership Firm Registration
- Sole Proprietorship Registration

**Registrations**
- GST Registration
- MSME / Udyam Registration
- FSSAI License Registration
- Import Export Code (IEC)
- Trademark Registration
- Shop & Establishment Registration

**Taxation**
- Income Tax Return Filing
- GST Return Filing
- TDS Return Filing
- ROC Annual Compliance / Annual Filing

**Bookkeeping & Accounting (India)**
- Bookkeeping & Accounting Services
- Payroll Processing
- Virtual CFO Services

**Tools (huge, low-effort traffic driver — RegisterKaro gets significant search volume from these)**
- GST Calculator
- Income Tax Calculator
- Compliance Due Date Calendar (you already have `due-dates.php` — turn it into an interactive, indexable calendar page instead of a static list)

Every one of the `#` placeholder links in your current menu should become a real page before anything else — those are searches you're currently losing 100% of.

---

## 3. Recommended page structure (Australia side) — this is your priority

Since Australian bookkeeping is your actual specialism, this is where you're leaving the most money on the table. Suggested pages:

**Core service pages**
- Bookkeeping Services Australia
- BAS Agent Services / BAS Lodgement
- Payroll Services Australia (Single Touch Payroll / STP)
- Accounts Payable & Receivable Management
- Bank Reconciliation Services
- End of Financial Year (EOFY) Bookkeeping & Cleanup
- Virtual CFO Services Australia

**Software-specific pages (very high commercial intent, low competition — do these early)**
- Xero Bookkeeping Services
- MYOB Bookkeeping Services
- QuickBooks Online Bookkeeping Services

**B2B offering (if this applies to you — many Indian bookkeeping firms serve Australian accounting practices, not just end businesses)**
- Outsourced Bookkeeping for Australian Accountants & CPA Firms
- White-Label Bookkeeping Support

**Industry pages (people search "bookkeeper for tradies," "bookkeeping for NDIS providers," etc. constantly)**
- Bookkeeping for Tradies & Construction
- Bookkeeping for NDIS Providers
- Bookkeeping for Hospitality & Cafes
- Bookkeeping for Real Estate Agents / Property Managers

**Trust-building pages**
- About Us / Our Team (mention any Xero/MYOB certifications, ICB or BAS agent registration if held — Australians specifically look for "registered BAS agent")
- Pricing / Packages
- Case Studies
- Blog (ATO due dates, STP changes, super guarantee rate changes, EOFY checklists)

I built a complete example of the flagship page below so your developer has an exact template to copy for the rest.

---

## 4. Keyword targets

**India (sample — expand with Google Keyword Planner / Ubersuggest for volume)**
- gst registration online
- private limited company registration india
- llp registration online
- income tax return filing online
- gst registration consultant near me
- company registration consultant delhi / rohini
- msme udyam registration online
- gst return filing services

**Australia (sample)**
- bookkeeping services australia
- outsourced bookkeeping australia
- xero bookkeeper australia
- bas agent services
- small business bookkeeping services
- virtual bookkeeper australia
- bookkeeping services for accountants australia
- remote bookkeeping services australia
- bookkeeping for tradies
- online bookkeeping services

Long-tail, question-style keywords ("how much does a bookkeeper cost in australia," "do i need a bas agent") are worth targeting via blog posts — they convert well and are far less competitive than the head terms above.

---

## 5. Technical SEO checklist

- [ ] Pick one canonical domain format (`https://www.legalkhata.com`) and 301-redirect all variants (`http://`, non-www) to it — right now your own site links inconsistently between `legalkhata.com` and `www.legalkhata.com`.
- [ ] Unique `<title>` and meta description on every page (150–160 characters), written for humans, not stuffed with keyword lists. Drop the old `meta-keywords` tag content-style stuffing — Google ignores that tag entirely now; it only helps in Bing marginally.
- [ ] Add `Organization` + `ProfessionalService` schema (JSON-LD) sitewide, with separate `LocalBusiness` schema for your India address and, if you have one, an Australian registered address/ABN.
- [ ] Wrap your existing FAQ section in `FAQPage` schema — you already have good FAQ content, it's just not marked up, so it's not eligible for the FAQ rich snippet in search results.
- [ ] Add `BreadcrumbList` schema once you have nested URLs (`/in/registrations/gst-registration`).
- [ ] Generate and submit an XML sitemap in Google Search Console (and Bing Webmaster Tools) — submit `/in/` and `/au/` sections, ideally as separate sitemap files referenced from one sitemap index.
- [ ] Compress and convert images (`logos.jpg`, `jd.png`, etc.) to WebP; add descriptive `alt` text to every image (currently missing).
- [ ] Fix all `#` placeholder links — an unindexed, non-existent page is a dead end for both users and Google's crawler.
- [ ] Set up (or claim) a separate Google Business Profile for your Australian presence if you have any Australian registration/address — this is what gets you into the Google Maps 3-pack for "bookkeeper near me" searches in Australia.
- [ ] Real testimonials with a star-rating schema (`Review`/`AggregateRating`) once you have genuine reviews collected — don't fabricate these, Google actively penalizes fake review markup.
- [ ] Start a blog and publish consistently — this is the #1 reason RegisterKaro outranks smaller firms: they publish frequently on exactly the questions people search.

---

## 6. Suggested rollout order

1. Fix broken `#` links → real pages (start with Bookkeeping/Accounting since that's core business)
2. Build out `/au/` bookkeeping service pages (use the template below)
3. Make the country switcher functional + add hreflang
4. Add schema markup sitewide
5. Build out remaining `/in/` service pages
6. Launch blog, publish 2–4 posts/month per country
7. Add calculators/tools pages
8. Ongoing: Google Business Profile, backlinks/directory listings, review collection
