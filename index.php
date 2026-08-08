<?php
$locale       = 'in';
$page_title   = 'Legal Khata | Company Registration, GST & Tax (India) · Bookkeeping (Australia)';
$meta_desc    = 'Legal Khata helps businesses register, stay compliant and manage their books — company registration, GST and tax filing in India, and outsourced bookkeeping in Australia.';
$canonical    = 'https://www.legalkhata.com/';
$hreflang_in  = 'https://www.legalkhata.com/in/';
$hreflang_au  = 'https://www.legalkhata.com/au/';
$hreflang_def = 'https://www.legalkhata.com/';
$schema_json  = '<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Legal Khata",
  "url": "https://www.legalkhata.com/",
  "logo": "https://www.legalkhata.com/assets/img/logo.png",
  "sameAs": [
    "https://www.facebook.com/legalkhata",
    "https://www.instagram.com/legalkhata/",
    "https://www.youtube.com/channel/UCQqO8y7aUGpNc-1quC77spA"
  ],
  "contactPoint": [{
    "@type": "ContactPoint",
    "telephone": "+91-70489-15155",
    "contactType": "customer service",
    "areaServed": ["IN", "AU"]
  }]
}
</script>';
include 'includes/header.php';
?>

<section class="hero ledger-lines">
  <div class="wrap" style="grid-template-columns:1fr; text-align:center;">
    <div>
      <div class="eyebrow" style="justify-content:center;">Welcome to Legal Khata</div>
      <h1>One practice. Two ledgers.<br>India registrations &amp; tax — Australia bookkeeping.</h1>
      <p class="lede center" style="margin:0 auto 2rem;max-width:56ch;">
        Choose your country to see services, pricing and compliance timelines built specifically for you.
      </p>
    </div>
  </div>
</section>

<section>
  <div class="wrap grid-2">
    <div class="card">
      <span class="idx">🇮🇳 INDIA</span>
      <h3>Company Registration, GST &amp; Tax</h3>
      <p>Private Limited &amp; LLP registration, GST registration and returns, income tax filing, MSME/Udyam and full bookkeeping support for Indian businesses.</p>
      <a class="btn btn-brass" href="/in/">Go to India Services →</a>
    </div>
    <div class="card">
      <span class="idx">🇦🇺 AUSTRALIA</span>
      <h3>Outsourced Bookkeeping</h3>
      <p>Xero &amp; MYOB certified bookkeeping, BAS preparation, payroll and STP, and white-label support for Australian accounting firms.</p>
      <a class="btn btn-brass" href="/au/">Go to Australia Services →</a>
    </div>
  </div>
</section>

<?php include 'includes/footer.php'; ?>
