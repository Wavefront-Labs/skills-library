---
id: computing-software.systems-network-administration.pki-tls-administration.certbot-deploy-hooks
name: certbot-deploy-hooks
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [certbot-deploy-hooks, pki-certbot, certbot, deploy-hook, pre-hook, post-hook, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Run pre, post and deploy hooks to reload services, copy certificates and handle multi-service deployments on renewal."
sources:
  - https://eff-certbot.readthedocs.io/en/stable/using.html#renewing-certificates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# certbot hooks and reloads
Goal: renewed certificates actually reach the running service.
- `--deploy-hook` runs once for each successfully issued certificate, including renewals; `--pre-hook` and `--post-hook` run before and after each renewal attempt, only when a certificate is due.
- Put persistent scripts in `/etc/letsencrypt/renewal-hooks/{pre,post,deploy}/`; executable files there run, in alphabetical order. Since certbot 3.2.0 they run for any subcommand, not only `renew`.
```
#!/bin/sh
# /etc/letsencrypt/renewal-hooks/deploy/reload.sh
set -e
nginx -t && systemctl reload nginx
```
- In a deploy hook `$RENEWED_LINEAGE` is the live subdirectory of the certificate; use it to copy into HAProxy bundles: `cat $RENEWED_LINEAGE/fullchain.pem $RENEWED_LINEAGE/privkey.pem > /etc/haproxy/certs/site.pem`. From certbot 2.7.0 post-renewal hooks also get `RENEWED_DOMAINS` and `FAILED_DOMAINS`.
- A failing hook is printed to stderr and renewal still goes ahead; certbot exits non-zero only when a renewal attempt fails. Monitor hook output separately.
- Reload, do not restart, to avoid dropped connections.
Gotcha: hooks from the command line, config file or renewal config run after the directory hooks, except that an executable already in the matching hook directory is not run twice; `--no-directory-hooks` turns directory hooks off. Options given to `certbot renew` are saved for that certificate; check `/etc/letsencrypt/renewal/*.conf`.
Verify:
- [ ] `certbot renew --dry-run --run-deploy-hooks` runs the deploy hooks during a test run (`--force-renewal` renews everything and can hit rate limits).
- [ ] Hook logs show success.

## Checked
2026-11-03. Confirmed on the certbot User Guide and command-line reference: hook semantics for `--pre-hook`, `--post-hook` and `--deploy-hook`, the `renewal-hooks/{pre,deploy,post}` directories, alphabetical order and the 3.2.0 change, `--no-directory-hooks`, `$RENEWED_LINEAGE`, `RENEWED_DOMAINS` and `FAILED_DOMAINS` from 2.7.0, failing-hook and exit-status behaviour, `--run-deploy-hooks`, `--force-renewal` rate-limit warning. Removed: the advice to exit non-zero to alert the timer (the page says a failing hook does not change the exit code directly).
Method: documentation only; no commands were run.
