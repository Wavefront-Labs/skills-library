---
id: computing-software.email-administration.dovecot.postfix-dovecot-sasl-submission-auth
name: postfix-dovecot-sasl-submission-auth
category: computing-software
field: email-administration
product: dovecot
tags: [postfix-sasl, smtpd-sasl, submission-port, permit-sasl-authenticated, login-maps, auth-over-tcp]
level: practitioner
status: docs-checked
description: "Use Dovecot as the authentication backend for Postfix SMTP AUTH, with a dedicated submission port, TLS and optional TCP auth."
sources:
  - https://doc.dovecot.org/main/howto/sasl/postfix.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since version 2.3, Postfix supports SMTP AUTH through Dovecot SASL. If you need GSSAPI, oauth2 or external (certificate based) authentication, use the Dovecot submission service instead. For Postfix installed from a binary package, check Dovecot SASL support with `postconf -a`.

Configuration has two halves. In Dovecot, expose the auth service on a socket Postfix can reach and set the mechanisms:

```
service auth {
  unix_listener /var/spool/postfix/private/auth {
    mode = 0660
    user = postfix
    group = postfix
  }
}
auth_mechanisms = plain login
```

The page notes that Outlook and Windows Mail work only with the LOGIN mechanism, not PLAIN, and that the user and group assume the default Postfix user and group. In Postfix `main.cf`:

```
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
smtpd_relay_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination
```

`smtpd_sasl_path` can be absolute or relative to `$queue_directory`. On Debian and Ubuntu, Postfix runs chrooted by default, so leave it relative. With Postfix before 2.10, use `smtpd_recipient_restrictions` instead of `smtpd_relay_restrictions`.

Use a dedicated submission port (TCP 587) for mail clients. In `master.cf` you can override global parameters for that entry, and you will not run into internet mail rejection when the Dovecot auth mechanism is unavailable (port 25 is unaffected). The page's example accepts TLS-encrypted sessions only and adds sanity checks, including verifying alias ownership via login maps and domain name and recipient plausibility:

```
submission inet n - n - - smtpd
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_sasl_type=dovecot
  -o smtpd_sasl_path=private/auth
  -o smtpd_sasl_security_options=noanonymous
  -o smtpd_sasl_local_domain=$myhostname
  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
  -o smtpd_sender_login_maps=hash:/etc/postfix/virtual
  -o smtpd_sender_restrictions=reject_sender_login_mismatch
  -o smtpd_recipient_restrictions=reject_non_fqdn_recipient,reject_unknown_recipient_domain,permit_sasl_authenticated,reject
```

If Postfix and Dovecot run on separate servers, authenticate over TCP. In Dovecot add an `inet_listener` inside `service auth`:

```
service auth {
  inet_listener auth {
    port = 12345
  }
}
```

and point Postfix at it with `smtpd_sasl_path = inet:dovecot.example.com:12345` and `smtpd_sasl_type = dovecot`. The page gives no encryption guidance for this link; credentials cross it, so protect it with your own network controls.

## Checked
2026-11-09. Read the whole Dovecot page "Postfix and Dovecot SASL" (doc.dovecot.org/main/howto/sasl/postfix.html) and compared every setting, version and port against it. Removed the claims about related Exim and chasquid pages, a general SASL admin page and a page caution about unencrypted TCP, none of which are on the page.

Method: documentation only; no commands were run.
