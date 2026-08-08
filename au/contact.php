<?php
$locale       = 'au';
$page_title   = 'Contact Legal Khata | Bookkeeping Services, Australia';
$meta_desc    = 'Get in touch with Legal Khata for outsourced bookkeeping, BAS support and payroll services in Australia. Request a free consultation and fixed monthly quote.';
$canonical    = 'https://www.legalkhata.com/au/contact.php';
$hreflang_in  = 'https://www.legalkhata.com/in/contact.php';
$hreflang_au  = $canonical;
$hreflang_def = $canonical;
$breadcrumb   = [['label'=>'Home','url'=>'/au/'], ['label'=>'Contact','url'=>'#']];
$schema_json  = '<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService","name":"Legal Khata",
"telephone":"+91-70489-15155","email":"infolegalkhata@gmail.com",
"areaServed":{"@type":"Country","name":"Australia"}}
</script>';
include '../includes/header.php';
?>
<section class="hero ledger-lines">
  <div class="wrap" style="grid-template-columns:1fr;">
    <div>
      <div class="eyebrow">Contact</div>
      <h1>Get a fixed monthly bookkeeping quote</h1>
      <p class="lede">Tell us about your business and current software setup — we'll reply within 24 hours with a fixed monthly quote.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap two-col">
    <div>
      <!-- NOTE: this form currently has no backend handler. Point action="" at your
           mail-processing script (PHPMailer, a form service, etc.) before going live. -->
      <form method="post" action="/au/contact-handler.php">
        <div class="form-grid">
          <div class="field"><label for="name">Full name</label><input id="name" name="name" type="text" required></div>
          <div class="field"><label for="phone">Phone number</label><input id="phone" name="phone" type="tel" required></div>
        </div>
        <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" required></div>
        <div class="field"><label for="business">Business name</label><input id="business" name="business" type="text"></div>
        <div class="field"><label for="software">Accounting software you use</label>
          <select id="software" name="software">
            <option>Xero</option>
            <option>MYOB</option>
            <option>QuickBooks Online</option>
            <option>None yet / Spreadsheets</option>
            <option>Other</option>
          </select>
        </div>
        <div class="field"><label for="type">I am a...</label>
          <select id="type" name="type">
            <option>Small business owner</option>
            <option>Accounting / CPA firm</option>
          </select>
        </div>
        <div class="field"><label for="message">Anything else we should know?</label><textarea id="message" name="message" rows="4"></textarea></div>
        <button type="submit" class="btn btn-brass">Request Free Consultation</button>
      </form>
    </div>
    <div>
      <h2>Direct contact</h2>
      <p><strong>Phone:</strong> <a href="tel:+917048915155">+91 70489 15155</a><br>
      <strong>Email:</strong> <a href="mailto:infolegalkhata@gmail.com">infolegalkhata@gmail.com</a></p>
      <p><a href="https://api.whatsapp.com/send/?phone=917048915155&text&app_absent=0">Message us on WhatsApp →</a></p>
    </div>
  </div>
</section>
<?php include '../includes/footer.php'; ?>
