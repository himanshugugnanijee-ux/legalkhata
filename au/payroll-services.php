<?php
$locale       = 'au';
$page_title   = 'Payroll Services Australia | Single Touch Payroll | Legal Khata';
$meta_desc    = 'Outsourced payroll processing for Australian small businesses — accurate pay runs, superannuation and ATO-compliant Single Touch Payroll (STP) reporting.';
$canonical    = 'https://www.legalkhata.com/au/payroll-services.php';
$hreflang_in  = 'https://www.legalkhata.com/in/bookkeeping-accounting.php';
$hreflang_au  = $canonical;
$hreflang_def = $canonical;
$breadcrumb   = [['label'=>'Home','url'=>'/au/'], ['label'=>'Payroll Services','url'=>'#']];
$schema_json  = '<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","serviceType":"Payroll Services",
"provider":{"@type":"ProfessionalService","name":"Legal Khata","areaServed":"AU"},
"areaServed":{"@type":"Country","name":"Australia"}}
</script>';
include '../includes/header.php';
?>
<section class="hero ledger-lines">
  <div class="wrap">
    <div>
      <div class="eyebrow">Payroll</div>
      <h1>Payroll Services &amp; Single Touch Payroll</h1>
      <p class="lede">Accurate pay runs, correct superannuation calculations and ATO-compliant
      Single Touch Payroll (STP) reporting — every pay cycle, without the admin load on you.</p>
      <div class="hero-actions">
        <a href="/au/contact.php" class="btn btn-brass">Get a Payroll Quote</a>
      </div>
    </div>
    <div class="ledger-card">
      <div class="row"><span>Pay run frequency</span><span>Weekly/Fortnightly/Monthly</span></div>
      <div class="row"><span>STP reporting</span><span>Every pay event</span></div>
      <div class="row"><span>Superannuation</span><span>Calculated &amp; tracked</span></div>
      <div class="row"><span>Payslips</span><span>Issued automatically</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap two-col">
    <div>
      <h2>What's included</h2>
      <ul class="check-list">
        <li>Employee pay runs processed on schedule</li>
        <li>Superannuation guarantee calculated correctly per employee</li>
        <li>Single Touch Payroll (STP) reporting to the ATO each pay event</li>
        <li>Payslip generation and distribution</li>
        <li>Leave accrual tracking (annual, personal/sick)</li>
        <li>End-of-year finalisation for income statements</li>
      </ul>
    </div>
    <div>
      <h2>Works with your software</h2>
      <p>We run payroll inside Xero, MYOB or QuickBooks Online payroll modules — no separate
      system to reconcile against your books later.</p>
      <div>
        <span class="badge">Xero Payroll</span>
        <span class="badge">MYOB Payroll</span>
        <span class="badge">QuickBooks Payroll</span>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="cta-banner">
      <div><h2>Take payroll off your plate.</h2><p>Free consultation, fixed monthly pricing.</p></div>
      <a href="/au/contact.php" class="btn btn-brass">Book Free Consultation</a>
    </div>
  </div>
</section>
<?php include '../includes/footer.php'; ?>
