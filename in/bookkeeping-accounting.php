<?php
$locale       = 'in';
$page_title   = 'Bookkeeping & Accounting Services in India | Legal Khata';
$meta_desc    = 'Monthly bookkeeping and accounting for Indian small businesses — bank reconciliation, ledgers, GST-ready books and financial statements. Fixed monthly pricing.';
$canonical    = 'https://www.legalkhata.com/in/bookkeeping-accounting.php';
$hreflang_in  = $canonical;
$hreflang_au  = 'https://www.legalkhata.com/au/bookkeeping-services.php';
$hreflang_def = $canonical;
$breadcrumb   = [['label'=>'Home','url'=>'/in/'], ['label'=>'Bookkeeping & Accounting','url'=>'#']];
$schema_json  = '<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","serviceType":"Bookkeeping and Accounting",
"provider":{"@type":"ProfessionalService","name":"Legal Khata","areaServed":"IN"},
"areaServed":{"@type":"Country","name":"India"}}
</script>';
include '../includes/header.php';
?>
<section class="hero ledger-lines">
  <div class="wrap">
    <div>
      <div class="eyebrow">Accounting</div>
      <h1>Bookkeeping &amp; Accounting Services</h1>
      <p class="lede">Books of accounts kept accurate and current, every month — so your GST returns,
      income tax filing and lender or investor reporting are never held up by messy records.</p>
      <div class="hero-actions">
        <a href="/in/contact.php" class="btn btn-brass">Get a Bookkeeping Quote</a>
      </div>
    </div>
    <div class="ledger-card">
      <div class="row"><span>Bank reconciliation</span><span>Monthly</span></div>
      <div class="row"><span>Ledger maintenance</span><span>Ongoing</span></div>
      <div class="row"><span>GST-ready books</span><span>Included</span></div>
      <div class="row"><span>Financial statements</span><span>Quarterly</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap two-col">
    <div>
      <h2>What's included</h2>
      <ul class="check-list">
        <li>Sales and purchase ledger entries</li>
        <li>Bank and cash reconciliation</li>
        <li>Accounts payable &amp; receivable tracking</li>
        <li>GST-ready books, aligned with your return filings</li>
        <li>Monthly/quarterly Profit &amp; Loss and Balance Sheet</li>
        <li>Year-end books handover to your CA/auditor</li>
      </ul>
    </div>
    <div>
      <h2>Who this is for</h2>
      <ul class="check-list">
        <li>Small and growing businesses without an in-house accountant</li>
        <li>Startups needing investor-ready financials</li>
        <li>Proprietors and partnerships filing GST returns monthly</li>
        <li>Companies preparing for their statutory audit</li>
      </ul>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="cta-banner">
      <div><h2>Let us keep your books.</h2><p>Free consultation and a fixed monthly quote.</p></div>
      <a href="/in/contact.php" class="btn btn-brass">Book Free Consultation</a>
    </div>
  </div>
</section>
<?php include '../includes/footer.php'; ?>
