---
id: computing-software.web-development.wordpress.email-deliverability-smtp-and-wp-mail
name: email-deliverability-smtp-and-wp-mail
category: computing-software
field: web-development
product: wordpress
tags: [wp-mail-smtp, wp-mail, email-deliverability, spf-dkim-dmarc, wordpress]
level: practitioner
status: docs-checked
description: "Making WordPress email deliverable: why PHP mail() fails, sending via SMTP or provider APIs, phpmailer_init configuration, SPF, DKIM and DMARC, from-address rules and logging."
sources:
  - https://developer.wordpress.org/reference/functions/wp_mail/
  - https://developer.wordpress.org/reference/hooks/phpmailer_init/
  - https://support.google.com/a/answer/81126
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Email deliverability (SMTP / wp_mail)

## 1. The problem
`wp_mail()` uses PHPMailer with PHP `mail()` by default: messages come from the web server, often with a `wordpress@host` sender, no DKIM, and an IP with poor reputation. Gmail's sender requirements, in force since 1 February 2024, expect authenticated mail (SPF, DKIM, and DMARC for senders over 5,000 messages a day, with From-domain alignment); unauthenticated messages may be marked as spam or rejected.

## 2. Send through a real provider
Options: a transactional email service via SMTP or HTTP API, or your organisation's mail server, using an SMTP plugin or this code:
```php
add_action( 'phpmailer_init', function ( PHPMailer\PHPMailer\PHPMailer $mailer ) {
    $mailer->isSMTP();
    $mailer->Host       = 'smtp.provider.example';
    $mailer->Port       = 587;
    $mailer->SMTPSecure = 'tls';
    $mailer->SMTPAuth   = true;
    $mailer->Username   = ACME_SMTP_USER;      // define in wp-config.php or env, never in the database unencrypted
    $mailer->Password   = ACME_SMTP_PASS;
} );
add_filter( 'wp_mail_from', fn() => 'no-reply@example.com' );
add_filter( 'wp_mail_from_name', fn() => 'Example Store' );
```
- Use a From address on **your** domain that the provider is authorised to send for.

## 3. DNS authentication
```
example.com.                TXT "v=spf1 include:spf.provider.example ~all"
selector._domainkey.example.com.  TXT "k=rsa; p=..."          # provider-supplied DKIM key
_dmarc.example.com.         TXT "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
```
- DKIM signing by the provider with alignment to the From domain.
- Start DMARC at `p=none` (Google accepts a policy of none), read the DMARC reports, then tighten the policy.

## 4. Operations
- Log sent mail and failures (plugin email logs or provider dashboards); hook `wp_mail_failed` to log errors.
- Keep transactional mail separate from marketing mail.

## 5. Development
Route mail to a local catcher on staging, or short-circuit `wp_mail` with the `pre_wp_mail` filter, so test sites don't email real customers.

## Verify
- [ ] Test email shows SPF, DKIM and DMARC pass and is not marked as spam; From uses your domain; failures logged; staging cannot email real users.

## Checked
2026-11-01. Confirmed against the wp_mail() reference (PHPMailer, wp_mail_from, wp_mail_from_name, wp_mail_failed, pre_wp_mail), the phpmailer_init hook page and Google's email sender guidelines (2024 requirements, 5,000/day threshold, alignment, DMARC policy none allowed). Removed: Yahoo claim, vendor names and SMTP host, SPF lookup limit, port-blocking claim, mail-tester and Mailpit.
Method: documentation only; no commands were run.
