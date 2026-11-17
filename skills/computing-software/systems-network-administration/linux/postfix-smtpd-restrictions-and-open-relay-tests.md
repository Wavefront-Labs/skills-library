---
id: computing-software.systems-network-administration.linux.postfix-smtpd-restrictions-and-open-relay-tests
name: postfix-smtpd-restrictions-and-open-relay-tests
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, smtpd-recipient-restrictions, open-relay, postfix, smtpd-relay-restrictions, postscreen, rbl]
level: practitioner
status: docs-checked
description: "Lock down Postfix with smtpd_relay_restrictions and smtpd_recipient_restrictions, RBLs and postscreen, then prove the server is not an open relay."
sources:
  - https://www.postfix.org/SMTPD_ACCESS_README.html
  - https://www.postfix.org/postconf.5.html#smtpd_relay_restrictions
  - https://www.postfix.org/POSTSCREEN_README.html
  - https://github.com/jetmore/swaks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Postfix smtpd restrictions and open relay tests

## The two lists
Since Postfix 2.10, relay control sits in `smtpd_relay_restrictions` and spam policy in `smtpd_recipient_restrictions`. Both are evaluated at `RCPT TO`; the first `permit`/`reject` wins within each list.
```
# main.cf
mynetworks = 127.0.0.0/8 [::1]/128 10.0.0.0/16
smtpd_relay_restrictions =
    permit_mynetworks,
    permit_sasl_authenticated,
    defer_unauth_destination
smtpd_recipient_restrictions =
    reject_non_fqdn_recipient,
    reject_unknown_recipient_domain,
    reject_unauth_pipelining,
    permit_mynetworks,
    permit_sasl_authenticated,
    reject_rbl_client zen.spamhaus.org=127.0.0.[2..11],
    reject_rhsbl_sender dbl.spamhaus.org=127.0.1.[2..99],
    check_policy_service unix:private/policyd-spf
smtpd_helo_required = yes
smtpd_helo_restrictions = permit_mynetworks, reject_invalid_helo_hostname, reject_non_fqdn_helo_hostname
smtpd_sender_restrictions = reject_non_fqdn_sender, reject_unknown_sender_domain
disable_vrfy_command = yes
```
- `defer_unauth_destination` (temporary 4xx) is the safe default while testing; switch to `reject_unauth_destination` once sure.
- Never put `permit` before the relay check in either list; one stray `permit` makes an open relay.
- `mynetworks` too wide (e.g. a whole cloud VPC shared with others) is a classic relay hole. `mynetworks_style` defaults to `host` (trust only the local machine) from Postfix 3.0 and `subnet` before; an explicit `mynetworks` overrides it.
- Check the DNSBL operator's current usage terms before querying its public mirrors from a busy server.

## postscreen (before smtpd)
```
# master.cf: replace "smtp inet ... smtpd" with
smtp      inet  n - n - 1 postscreen
smtpd     pass  - - n - - smtpd
dnsblog   unix  - - n - 0 dnsblog
tlsproxy  unix  - - n - 0 tlsproxy
# main.cf
postscreen_greet_action = enforce
postscreen_dnsbl_sites = zen.spamhaus.org*3 bl.spamcop.net*1
postscreen_dnsbl_threshold = 3
postscreen_dnsbl_action = enforce
```

## Prove it is not an open relay
```bash
postconf -n | grep -E 'relay|recipient|mynetworks'
# from an outside host:
swaks --server mx.example.com --from a@outside.test --to b@another.test
# expect: rejected at RCPT TO with a temporary (4xx) code under defer_unauth_destination, or a permanent (5xx) code under reject_unauth_destination
swaks --server mx.example.com --to user@example.com      # local delivery still accepted
swaks --server mx.example.com:587 --tls --auth LOGIN --auth-user alice --to b@another.test   # authenticated relay works
```
Run the test from a host outside your own networks, since `mynetworks` hosts are trusted. `postmap -q 1.2.3.4 cidr:/etc/postfix/client_access` tests lookup tables.

## Verify
- [ ] Unauthenticated external `RCPT TO` a foreign domain is rejected (4xx or 5xx); the mail log shows a `reject:` or `NOQUEUE` line for it.
- [ ] `postfix check` clean and `postconf -n` shows no `permit` before relay checks.

## Checked
Checked 2026-10-27 against the Postfix documentation (current source tree, Postfix 3.11) and the swaks manual.
- `smtpd_relay_restrictions` exists since Postfix 2.10 with default `permit_mynetworks, permit_sasl_authenticated, defer_unauth_destination`; `defer_unauth_destination` gives a non-permanent code (postconf.5).
- `reject_rbl_client`/`reject_rhsbl_sender` accept `=d.d.d.d` patterns with `[a..b]` ranges (Postfix 2.8 and later); `reject_unauth_pipelining`, `reject_unknown_*_domain` and `reject_non_fqdn_*` exist (postconf.5).
- `mynetworks_style` defaults to `host` from Postfix 3.0 (postconf.5).
- postscreen master.cf lines use chroot `n`, and `postscreen_dnsbl_sites` weights use `site*N` (POSTSCREEN_README).
- swaks options `--server host[:port]`, `--auth`, `--auth-user` and `--tls` exist (swaks manual).
- Removed unconfirmed claims: literal 454 reply text, Spamhaus public-mirror behaviour, third-party online relay checker.
Method: documentation only; no commands were run.
