---
id: computing-software.systems-network-administration.pki-tls-administration.certbot-issue-renew
name: certbot-issue-renew
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [certbot-issue-renew, pki-certbot, certbot, letsencrypt, webroot, standalone, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Issue and renew certificates with certbot using nginx, apache, webroot, standalone and DNS plugins, and test renewal with a dry run."
sources:
  - https://eff-certbot.readthedocs.io/en/stable/using.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# certbot issue and renew
Goal: automatic issuance on a Linux server.
```
certbot --nginx -d example.com -d www.example.com
certbot certonly --webroot -w /var/www/html -d example.com
certbot certonly --standalone --preferred-challenges http -d example.com
certbot renew --dry-run
```
- Certificates are saved under `/etc/letsencrypt/live/<name>/`; point services at `fullchain.pem` and `privkey.pem` there.
- DNS plugins such as `certbot-dns-cloudflare` exist; use the plugin's own documentation for its flags.
- Renewal config: `/etc/letsencrypt/renewal/<name>.conf` (editing it by hand is discouraged; test with `certbot renew --dry-run`). Your installation method may have pre-installed a timer: look for `certbot renew` in crontab or `systemctl list-timers`.
- Staging: add `--staging` while testing; `--dry-run` uses staging.
- Key type: since certbot 2.0.0 the default is ECDSA secp256r1; `--key-type`, `--elliptic-curve` and `--rsa-key-size` change it.
Gotcha: `--standalone` must bind to port 80 for validation, so a running web server on that port makes renewal fail; stop it with `--pre-hook` and `--post-hook`, or use the webroot or nginx plugin.
Verify:
- [ ] `certbot renew --dry-run` succeeds.
- [ ] `certbot certificates` lists the certificates you have from certbot.

## Checked
2026-11-03. Confirmed on the certbot User Guide and command-line reference: `--nginx`, `certonly --webroot -w`, `--standalone` binding port 80, `--preferred-challenges`, `renew --dry-run`, `certificates`, `--staging`, `--key-type`, `--elliptic-curve` and the 2.0.0 ECDSA default, paths under `/etc/letsencrypt/live` and `renewal/CERTNAME.conf`, timer lookup via crontab or systemd timers, the certbot-dns-cloudflare plugin name. Removed: the Cloudflare credentials flag and wildcard example (flag not on the fetched pages), the symlink wording, and the snap/distro timer claim.
Method: documentation only; no commands were run.
