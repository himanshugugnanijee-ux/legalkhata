<?php
/*
  Expected variables set by the calling page BEFORE including this file:

  $locale        = 'in' or 'au'
  $page_title    = string, full <title> text
  $meta_desc     = string, meta description (150-160 chars)
  $canonical     = full canonical URL for this page
  $hreflang_in   = full URL of the India version of this page
  $hreflang_au   = full URL of the Australia version of this page
  $hreflang_def  = full URL to use as x-default (usually same as root domain page)
  $breadcrumb    = optional array of ['label' => 'Home', 'url' => '/'] entries
  $schema_json   = optional raw JSON-LD string(s) for page-specific schema
*/
$locale       = isset($locale) ? $locale : 'in';
$page_title   = isset($page_title) ? $page_title : 'Legal Khata';
$meta_desc    = isset($meta_desc) ? $meta_desc : '';
$canonical    = isset($canonical) ? $canonical : '';
$hreflang_in  = isset($hreflang_in) ? $hreflang_in : 'https://www.legalkhata.com/in/';
$hreflang_au  = isset($hreflang_au) ? $hreflang_au : 'https://www.legalkhata.com/au/';
$hreflang_def = isset($hreflang_def) ? $hreflang_def : 'https://www.legalkhata.com/';
$root         = ($locale === 'au') ? '/au' : '/in';
?><!DOCTYPE html>
<html lang="<?php echo $locale === 'au' ? 'en-AU' : 'en-IN'; ?>">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title><?php echo $page_title; ?></title>
<meta name="description" content="<?php echo $meta_desc; ?>">
<?php if ($canonical): ?><link rel="canonical" href="<?php echo $canonical; ?>"><?php endif; ?>

<link rel="alternate" href="<?php echo $hreflang_in; ?>" hreflang="en-in">
<link rel="alternate" href="<?php echo $hreflang_au; ?>" hreflang="en-au">
<link rel="alternate" href="<?php echo $hreflang_def; ?>" hreflang="x-default">

<meta property="og:type" content="website">
<meta property="og:title" content="<?php echo $page_title; ?>">
<meta property="og:description" content="<?php echo $meta_desc; ?>">
<?php if ($canonical): ?><meta property="og:url" content="<?php echo $canonical; ?>"><?php endif; ?>
<meta name="twitter:card" content="summary_large_image">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">

<?php if (!empty($schema_json)) { echo $schema_json; } ?>
</head>
<body>

<div class="topbar">
  <div class="wrap">
    <div class="topbar-links">
      <a href="tel:+917048915155">+91 70489 15155</a>
      <a href="mailto:infolegalkhata@gmail.com">infolegalkhata@gmail.com</a>
    </div>
    <div class="topbar-links">
      <a href="https://www.facebook.com/legalkhata" aria-label="Facebook">Facebook</a>
      <a href="https://www.instagram.com/legalkhata/" aria-label="Instagram">Instagram</a>
      <div class="locale-switch">
        <label for="locale-select" style="position:absolute;left:-9999px;">Choose your country</label>
        <select id="locale-select">
          <option value="/in/" <?php echo $locale === 'in' ? 'selected' : ''; ?>>🇮🇳 India</option>
          <option value="/au/" <?php echo $locale === 'au' ? 'selected' : ''; ?>>🇦🇺 Australia</option>
        </select>
      </div>
    </div>
  </div>
</div>

<header class="site-header">
  <div class="wrap nav-row">
    <a href="<?php echo $root; ?>/" class="brand">
      <span class="mark">LK</span>
      <span>Legal Khata<br><small><?php echo $locale === 'au' ? 'BOOKKEEPING · AUSTRALIA' : 'REGISTRATIONS & TAX · INDIA'; ?></small></span>
    </a>

    <nav class="main-nav" aria-label="Primary">
      <?php if ($locale === 'au'): ?>
      <ul>
        <li><a href="/au/bookkeeping-services.php">Bookkeeping</a></li>
        <li><a href="/au/bas-lodgement.php">BAS Lodgement</a></li>
        <li><a href="/au/payroll-services.php">Payroll</a></li>
        <li><a href="/au/xero-bookkeeping.php">Xero Bookkeeping</a></li>
        <li><a href="/au/outsourced-bookkeeping-for-accountants.php">For Accounting Firms</a></li>
        <li><a href="/au/about.php">About</a></li>
      </ul>
      <?php else: ?>
      <ul>
        <li><a href="/in/private-limited-company-registration.php">Company Registration</a></li>
        <li><a href="/in/gst-registration.php">GST Registration</a></li>
        <li><a href="/in/income-tax-return-filing.php">Income Tax</a></li>
        <li><a href="/in/bookkeeping-accounting.php">Bookkeeping</a></li>
        <li><a href="/in/msme-udyam-registration.php">MSME</a></li>
        <li><a href="/in/about.php">About</a></li>
      </ul>
      <?php endif; ?>
    </nav>

    <div class="nav-cta">
      <a href="<?php echo $root; ?>/contact.php" class="btn btn-outline">Contact</a>
      <a href="<?php echo $root; ?>/contact.php" class="btn btn-brass">Free Consultation</a>
      <button class="menu-toggle" aria-label="Toggle menu" aria-expanded="false">☰</button>
    </div>
  </div>
</header>

<?php if (!empty($breadcrumb)): ?>
<div class="wrap crumb">
  <?php foreach ($breadcrumb as $i => $b): ?>
    <?php echo $i > 0 ? ' / ' : ''; ?><a href="<?php echo $b['url']; ?>"><?php echo $b['label']; ?></a>
  <?php endforeach; ?>
</div>
<?php endif; ?>
