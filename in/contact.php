<?php
$locale       = 'in';
$page_title   = 'Contact Legal Khata | Company Registration & Tax Consultants, India';
$meta_desc    = 'Get in touch with Legal Khata for company registration, GST, income tax and bookkeeping services in India. Call +91 70489 15155 or request a free consultation.';
$canonical    = 'https://www.legalkhata.com/in/contact.php';
$hreflang_in  = $canonical;
$hreflang_au  = 'https://www.legalkhata.com/au/contact.php';
$hreflang_def = $canonical;
$breadcrumb   = [['label'=>'Home','url'=>'/in/'], ['label'=>'Contact','url'=>'#']];
$schema_json  = '<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService","name":"Legal Khata",
"telephone":"+91-70489-15155","email":"infolegalkhata@gmail.com",
"address":{"@type":"PostalAddress","addressLocality":"Rohini, Delhi","addressCountry":"IN"}}
</script>';
include '../includes/header.php';
?>
<section class="hero ledger-lines">
  <div class="wrap" style="grid-template-columns:1fr;">
    <div>
      <div class="eyebrow">Contact</div>
      <h1>Tell us what you need registered or filed</h1>
      <p class="lede">Free first consultation. We'll tell you exactly what documents are needed and what it will cost, before you commit to anything.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap two-col">
    <div>
      <!-- NOTE: this form currently has no backend handler. Point action="" at your
           mail-processing script (PHPMailer, a form service, etc.) before going live. -->
      <form method="post" action="/in/contact-handler.php">
        <div class="form-grid">
          <div class="field"><label for="name">Full name</label><input id="name" name="name" type="text" required></div>
          <div class="field"><label for="phone">Phone number</label><input id="phone" name="phone" type="tel" required></div>
        </div>
        <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" required></div>
        <div class="field"><label for="service">What do you need help with?</label>
          <select id="service" name="service">
            <option>Private Limited Company Registration</option>
            <option>LLP Registration</option>
            <option>GST Registration</option>
            <option>Income Tax Return Filing</option>
            <option>MSME / Udyam Registration</option>
            <option>Bookkeeping &amp; Accounting</option>
            <option>Other</option>
          </select>
        </div>
        <div class="field"><label for="message">Message</label><textarea id="message" name="message" rows="4"></textarea></div>
        <button type="submit" class="btn btn-brass">Request Free Consultation</button>
      </form>
    </div>
    <div>
      <h2>Direct contact</h2>
      <p><strong>Phone:</strong> <a href="tel:+917048915155">+91 70489 15155</a><br>
      <strong>Email:</strong> <a href="mailto:infolegalkhata@gmail.com">infolegalkhata@gmail.com</a><br>
      <strong>Office:</strong> Rohini, Sector 6, Delhi</p>
      <p><a href="https://api.whatsapp.com/send/?phone=917048915155&text&app_absent=0">Message us on WhatsApp →</a></p>
    </div>
  </div>
</section>
<?php include '../includes/footer.php'; ?>
