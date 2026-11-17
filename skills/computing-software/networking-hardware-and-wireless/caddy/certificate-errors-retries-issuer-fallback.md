---
id: computing-software.networking-hardware-and-wireless.caddy.certificate-errors-retries-issuer-fallback
name: certificate-errors-retries-issuer-fallback
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [acme-errors, retries, issuer-fallback, zerossl, lets-encrypt, backoff, rate-limits, automatic-https]
level: advanced
status: docs-checked
description: "What Caddy does when certificate issuance fails: background retries, challenge switching, Let's Encrypt to ZeroSSL fallback, backoff schedule and rate limiting."
sources:
  - https://caddyserver.com/docs/automatic-https
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: interpret certificate failures and avoid making them worse.

Certificate management runs in the background, so startup is not blocked and sites run before all certificates exist. On an error Caddy: (1) retries once after a brief pause in case it was a fluke; (2) switches to the next enabled challenge type; (3) after all challenges, tries the next configured issuer; (4) after all issuers, backs off exponentially, with a maximum of 1 day between attempts, for up to 30 days. During retries with Let's Encrypt it uses their staging environment to avoid rate-limit trouble.

Default issuers are Let's Encrypt and ZeroSSL; if one fails, the other is tried. You can customise issuers globally or for specific names.

Internal rate limiting is currently 10 attempts per ACME account per 10 seconds, so a config with a million names is worked through gradually. In-flight tasks, including ACME transactions, are aborted when the config changes, so batch config changes and avoid constant reloads, otherwise certificates may never finish.

Testing: switch the ACME endpoint to a staging URL, because production rate limits can block you for up to a week. For Let's Encrypt staging use `https://acme-staging-v02.api.letsencrypt.org/directory`.

Storage: Caddy tests that storage is writable with enough capacity before ACME transactions; instances sharing storage coordinate as a cluster. With default storage, `$HOME` must be writable and persistent; `--environ` prints environment variables at startup for troubleshooting.

## Checked

2026-11-03: read automatic-https against this skill. Confirmed: retry order, 1 day maximum between attempts for up to 30 days, staging use during Let's Encrypt retries, default issuers, 10 attempts per 10 seconds, staging URL, storage notes.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
