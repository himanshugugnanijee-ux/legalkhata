<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h4>Legal Khata</h4>
        <p style="color:#B9C4B4;font-size:.9rem;max-width:32ch;">
          A technology-driven registration, tax and bookkeeping practice serving clients
          in India and Australia.
        </p>
      </div>

      <?php if ($locale === 'au'): ?>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="/au/bookkeeping-services.php">Bookkeeping Services</a></li>
          <li><a href="/au/bas-lodgement.php">BAS Lodgement</a></li>
          <li><a href="/au/payroll-services.php">Payroll Services</a></li>
          <li><a href="/au/xero-bookkeeping.php">Xero Bookkeeping</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/au/about.php">About Us</a></li>
          <li><a href="/au/outsourced-bookkeeping-for-accountants.php">For Accounting Firms</a></li>
          <li><a href="/au/contact.php">Contact</a></li>
          <li><a href="/in/">India Services</a></li>
        </ul>
      </div>
      <?php else: ?>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="/in/private-limited-company-registration.php">Company Registration</a></li>
          <li><a href="/in/gst-registration.php">GST Registration</a></li>
          <li><a href="/in/income-tax-return-filing.php">Income Tax Return</a></li>
          <li><a href="/in/bookkeeping-accounting.php">Bookkeeping &amp; Accounting</a></li>
          <li><a href="/in/msme-udyam-registration.php">MSME / Udyam Registration</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/in/about.php">About Us</a></li>
          <li><a href="/in/contact.php">Contact</a></li>
          <li><a href="/au/">Australia Services</a></li>
        </ul>
      </div>
      <?php endif; ?>
    </div>

    <div class="footer-bottom">
      <span>&copy; <?php echo date('Y'); ?> Legal Khata. All rights reserved.</span>
      <span>Rohini, Delhi, India · Serving clients across India &amp; Australia</span>
    </div>
  </div>
</footer>

<script src="/assets/js/main.js"></script>
</body>
</html>
