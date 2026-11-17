---
id: computing-software.systems-network-administration.linux.postfix-dovecot-mail-relay
name: postfix-dovecot-mail-relay
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, postfix, dovecot, mail-relay, smtp, smarthost, satellite, sasl, relayhost, main-cf, postconf, postqueue, mailq, imap, lmtp, maildir, spf, dkim, dmarc, opendkim, tls-smtp, null-client, system-mail, cron-mail, lpic-2, email, sysadmin, aliases]
level: practitioner
status: docs-checked
description: "Make Linux hosts send mail reliably: Postfix as a null client / authenticated smarthost relay, queue management, TLS and SASL, DKIM signing, and a minimal Dovecot IMAP/LMTP setup for a small domain."
sources:
  - https://www.postfix.org/BASIC_CONFIGURATION_README.html
  - https://www.postfix.org/SASL_README.html
  - https://www.postfix.org/postconf.5.html
  - https://doc.dovecot.org/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Postfix and Dovecot — relay system mail correctly, host a small mailbox domain if you must

**Goal:** cron/app/alert mail from every host reaches a mailbox via a relay with
authentication and TLS; the queue is observable; optionally one host receives mail for
a domain with IMAP access.

## 1. Null client / satellite (every server should be this)
```bash
# install postfix, a SASL client plugin package that provides PLAIN/LOGIN, and a mail(1) command, using your distro's package names
postconf -e 'myhostname = web01.example.com' \
           'myorigin = $mydomain' \
           'inet_interfaces = loopback-only' \
           'mydestination =' \
           'relayhost = [smtp.example.com]:587' \
           'smtp_tls_security_level = encrypt' \
           'smtp_sasl_auth_enable = yes' \
           'smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd' \
           'smtp_sasl_security_options = noanonymous' \
           'smtp_tls_CAfile = <path to the system CA bundle>' \
           'sender_canonical_maps = hash:/etc/postfix/sender_canonical'
# hash: tables need a Postfix built with hash support; use the type that `postconf -m` lists (the Postfix SASL README uses lmdb:)
echo '[smtp.example.com]:587 relayuser@example.com:<PASSWORD>' > /etc/postfix/sasl_passwd
chmod 600 /etc/postfix/sasl_passwd && postmap /etc/postfix/sasl_passwd
echo 'root alerts@example.com' > /etc/postfix/sender_canonical && postmap /etc/postfix/sender_canonical
echo 'root: ops@example.com' >> /etc/aliases && newaliases
systemctl enable --now postfix
echo test | mail -s "test from $(hostname)" root
```
- Brackets in `relayhost` skip MX lookup; `:587` = submission (STARTTLS); `:465` (SUBMISSIONS) needs
  `smtp_tls_wrappermode = yes`, which requires `smtp_tls_security_level = encrypt` or stronger.
- `mydestination =` (empty) means "deliver nothing locally, relay all" — otherwise
  `root@localhost` stays in `/var/mail/root` on each box. `/etc/aliases` + `newaliases`
  still redirects root's mail.
- `sender_canonical_maps` rewrites `root@web01` into a sender your relay accepts (many relays reject
  unknown senders). `smtp_generic_maps` does address rewriting in the SMTP client for mail sent to the internet.
- `smtp_tls_security_level = encrypt` fails rather than falling back to plaintext. The parameter's
  default is empty before Postfix 3.11 and `may` (opportunistic TLS) from 3.11, so set it explicitly.

## 2. Queue and logs
```bash
postqueue -p          # or mailq; shows queue ID, size, sender, reason
postqueue -f          # flush (retry everything now)
postsuper -d ALL deferred      # delete deferred mail; -d <ID> for one
postcat -q <ID>       # read a queued message
journalctl -u postfix -f  # or /var/log/maillog, /var/log/mail.log: look for status=sent/bounced/deferred and the SMTP reply
postconf -n           # non-default settings; postconf -d for defaults
postfix check         # check the installation for problems
```
Deferred with `SASL authentication failed` → wrong credentials or `postmap` not re-run;
a relay rejection (access denied) → the relay doesn't allow your IP/user; `certificate verification failed`
→ `smtp_tls_CAfile`/system CA bundle out of date.

## 3. Receiving mail for a domain (Postfix + Dovecot, single host)
DNS first: an `MX` record for the domain, `A`/`AAAA` for `mail`, **PTR** for the IP matching
`myhostname`, plus SPF and DMARC TXT records (RFC 7208, RFC 7489).
```bash
postconf -e 'inet_interfaces = all' 'mydestination = $myhostname' \
  'virtual_mailbox_domains = example.com' 'virtual_transport = lmtp:unix:private/dovecot-lmtp' \
  'smtpd_tls_cert_file = /etc/letsencrypt/live/mail.example.com/fullchain.pem' \
  'smtpd_tls_key_file = /etc/letsencrypt/live/mail.example.com/privkey.pem' \
  'smtpd_tls_security_level = may' 'smtpd_sasl_type = dovecot' 'smtpd_sasl_path = private/auth' \
  'smtpd_sasl_auth_enable = yes' \
  'smtpd_recipient_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination, reject_unknown_reverse_client_hostname, reject_rbl_client zen.spamhaus.org' \
  'message_size_limit = 52428800'
# master.cf: uncomment the "submission" service (587) with smtpd_tls_security_level=encrypt and smtpd_sasl_auth_enable=yes
```
Dovecot 2.4 syntax (2.4 renamed settings; on 2.3 the equivalents are `mail_location`, `ssl_cert` and `ssl_key`, see the 2.3-to-2.4 upgrade page):
```
protocols { lmtp = yes }
mail_driver = maildir
mail_path = /var/mail/vhosts/%{user|domain}/%{user|username}
ssl_server_cert_file = /etc/letsencrypt/live/mail.example.com/fullchain.pem
ssl_server_key_file  = /etc/letsencrypt/live/mail.example.com/privkey.pem
passdb passwd-file { passwd_file_path = /etc/dovecot/users }   # user:{SCHEME}password lines
service auth { unix_listener /var/spool/postfix/private/auth { mode = 0660 user = postfix group = postfix } }
```
The Postfix SASL README gives the same `service auth` listener (for Dovecot 2.x) together with
`auth_mechanisms = plain login`. For LMTP, add a `unix_listener` under `service lmtp` at the path
Postfix's `virtual_transport` points to (relative to the Postfix queue directory). Choose `mail_uid`/`mail_gid`
and the password scheme from the Dovecot documentation for your version; check the result with `doveconf -n`.
Open the SMTP, submission and IMAPS ports you use in the firewall. DKIM signing is done by a milter
(`smtpd_milters` points Postfix at it); follow your milter's documentation. Check
deliverability with an external test before trusting the setup.

## 4. Decision
Run a real mail domain yourself only if you own reverse DNS, can keep the IP reputation
clean, and someone will tend the queue and blocklists. Otherwise: every host is a null
client, the relay is a hosted provider, and inbound is hosted too.

## Verify
- [ ] `mail -s test root` on a host arrives in the ops mailbox within a minute; `postqueue -p` is empty.
- [ ] `journalctl -u postfix` shows `status=sent` with `TLS` and `SASL` noted; `postconf -n` has no warnings on `postfix check`.
- [ ] (Receiving) `openssl s_client -starttls smtp -connect mail.example.com:587` shows your cert; `doveadm auth test` succeeds; SPF/DKIM/DMARC all pass on an external test.

## Checked
Checked 2026-10-27 against the Postfix documentation (current source tree, which documents Postfix 3.11) and the Dovecot 2.4 documentation source (github.com/dovecot/documentation).
- `smtp_tls_security_level` default is empty before Postfix 3.11 and `may` from 3.11; `smtp_tls_wrappermode` needs `encrypt` or stronger (postconf.5).
- `smtpd_sasl_type` defaults to cyrus, so `dovecot` is set explicitly; the Dovecot `service auth` unix listener and `auth_mechanisms = plain login` are in the SASL README.
- Dovecot 2.4 setting names `mail_driver`, `mail_path`, `ssl_server_cert_file`, `ssl_server_key_file`, `passdb passwd-file { passwd_file_path }` and `%{user|domain}` variables are in the Dovecot docs and the 2.3-to-2.4 upgrade page.
- `smtp_generic_maps`, `postsuper -d ALL deferred`, `postqueue -f` and `postconf -m` are in the Postfix manuals.
- Removed unconfirmed claims: package names, CA bundle path, provider port-25 blocking, vendor sender rules, SPF/DMARC literals, OpenDKIM port and `doveadm pw` scheme example.
Method: documentation only; no commands were run.
