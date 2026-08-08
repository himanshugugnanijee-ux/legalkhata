<?php
$locale       = 'au';
$page_title   = 'BAS Lodgement Support Australia | Legal Khata';
$meta_desc    = 'BAS-ready bookkeeping and reconciliation ahead of every quarterly lodgement. We prepare the figures — your BAS agent or accountant lodges with confidence.';
$canonical    = 'https://www.legalkhata.com/au/bas-lodgement.php';
$hreflang_in  = 'https://www.legalkhata.com/in/gst-registration.php';
$hreflang_au  = $canonical;
$hreflang_def = $canonical;
$breadcrumb   = [['label'=>'Home','url'=>'/au/'], ['label'=>'BAS Lodgement','url'=>'#']];
$schema_json  = '<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","serviceType":"BAS Preparation Support",
"provider":{"@type":"ProfessionalService","name":"Legal Khata","areaServed":"AU"},
"areaServed":{"@type":"Country","name":"Australia"}}
</script>';
include '../includes/header.php';
?>
<section class="hero ledger-lines">
  <div class="wrap">
    <div>
      <div class="eyebrow">Compliance</div>
      <h1>BAS Lodgement Support</h1>
      <p class="lede">Business Activity Statements are only as accurate as the books behind them.
      We reconcile your accounts and prepare BAS-ready figures every quarter, so lodgement is
      fast and your BAS agent or accountant isn't chasing missing data.</p>
      <div class="hero-actions">
        <a href="/au/contact.php" class="btn btn-brass">Get BAS-Ready</a>
        <a href="/au/bookkeeping-services.php" class="btn btn-outline">See Full Bookkeeping Service</a>
      </div>
    </div>
    <div class="ledger-card">
      <div class="row"><span>GST reconciliation</span><span>Every quarter</span></div>
      <div class="row"><span>PAYG withholding check</span><span>Included</span></div>
      <div class="row"><span>Turnaround before due date</span><span>2 weeks buffer</span></div>
      <div class="row"><span>Lodgement itself</span><span>By your registered BAS agent/accountant</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap two-col">
    <div>
      <h2>What we prepare</h2>
      <ul class="check-list">
        <li>GST collected and GST paid, fully reconciled</li>
        <li>PAYG withholding figures from your payroll</li>
        <li>PAYG instalments where applicable</li>
        <li>Reconciled bank and credit card transactions for the period</li>
        <li>A clean summary handed to your BAS agent or accountant</li>
      </ul>
    </div>
    <div>
      <h2>Important note</h2>
      <p>Legal Khata prepares your books and figures to BAS-ready standard. Lodgement itself is
      completed by your registered BAS agent or accountant — if you don't already have one, we
      can point you toward one we work with regularly.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="cta-banner">
      <div><h2>Never scramble at BAS time again.</h2><p>Free consultation, fixed monthly pricing.</p></div>
      <a href="/au/contact.php" class="btn btn-brass">Book Free Consultation</a>
    </div>
  </div>
</section>
<?php include '../includes/footer.php'; ?>
