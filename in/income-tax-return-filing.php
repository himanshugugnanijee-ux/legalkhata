<?php
$locale       = 'in';
$page_title   = 'Income Tax Return (ITR) Filing Online in India | Legal Khata';
$meta_desc    = 'File your Income Tax Return online with an expert reviewing every entry — for salaried individuals, freelancers, proprietors and companies. Accurate, on-time filing.';
$canonical    = 'https://www.legalkhata.com/in/income-tax-return-filing.php';
$hreflang_in  = $canonical;
$hreflang_au  = 'https://www.legalkhata.com/au/';
$hreflang_def = $canonical;
$breadcrumb   = [['label'=>'Home','url'=>'/in/'], ['label'=>'Income Tax Return Filing','url'=>'#']];
$schema_json  = '<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","serviceType":"Income Tax Return Filing",
"provider":{"@type":"ProfessionalService","name":"Legal Khata","areaServed":"IN"},
"areaServed":{"@type":"Country","name":"India"}}
</script>';
include '../includes/header.php';
?>
<section class="hero ledger-lines">
  <div class="wrap">
    <div>
      <div class="eyebrow">Taxation</div>
      <h1>Income Tax Return Filing</h1>
      <p class="lede">We prepare and file your ITR with a human reviewing every entry — the right ITR
      form, maximised eligible deductions, and a filing you can defend if questioned.</p>
      <div class="hero-actions">
        <a href="/in/contact.php" class="btn btn-brass">File My ITR</a>
        <a href="/in/gst-registration.php" class="btn btn-outline">Also need GST?</a>
      </div>
    </div>
    <div class="ledger-card">
      <div class="row"><span>Salaried individuals</span><span>Same week</span></div>
      <div class="row"><span>Freelancers/proprietors</span><span>2–4 days</span></div>
      <div class="row"><span>Companies/LLPs</span><span>5–7 days</span></div>
      <div class="row"><span>Old notices/rectification</span><span>Handled</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap two-col">
    <div>
      <h2>Who we file for</h2>
      <ul class="check-list">
        <li>Salaried individuals with Form 16</li>
        <li>Freelancers and consultants (presumptive or regular)</li>
        <li>Proprietorships and partnership firms</li>
        <li>Private Limited Companies and LLPs</li>
        <li>Individuals with capital gains (shares, property, mutual funds)</li>
      </ul>
    </div>
    <div>
      <h2>What we check before filing</h2>
      <ul class="check-list">
        <li>Form 26AS / AIS reconciliation against your records</li>
        <li>All eligible deductions and exemptions claimed</li>
        <li>Correct ITR form selected for your income type</li>
        <li>Advance tax and TDS credit properly matched</li>
      </ul>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="cta-banner">
      <div><h2>Don't leave your ITR to the last date.</h2><p>Free consultation — tell us your income type.</p></div>
      <a href="/in/contact.php" class="btn btn-brass">Book Free Consultation</a>
    </div>
  </div>
</section>
<?php include '../includes/footer.php'; ?>
