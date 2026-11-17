---
id: computing-software.systems-network-administration.linux.acme-sh-certificates-with-http-01-webroot
name: acme-sh-certificates-with-http-01-webroot
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, acme-sh, http-01, acme, lets-encrypt, dns-01, zerossl]
level: practitioner
status: docs-checked
description: "Issue and renew TLS certificates with acme.sh: HTTP-01 webroot and standalone, DNS-01 API mode, install-cert with reload hooks, CA selection, and renewal checks."
sources:
  - https://github.com/acmesh-official/acme.sh
  - https://github.com/acmesh-official/acme.sh/wiki
  - https://github.com/acmesh-official/acme.sh/wiki/Server
  - https://letsencrypt.org/docs/rate-limits/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ACME with acme.sh

acme.sh is a POSIX shell ACME client: no Python, runs as a normal user, installs its own cron job.

## Install
```bash
curl https://get.acme.sh | sh -s email=admin@example.com      # into ~/.acme.sh, adds a daily cron
# open a new shell afterwards so the acme.sh alias takes effect
acme.sh --set-default-ca --server letsencrypt                 # default CA is ZeroSSL since acme.sh v3.0
```

## HTTP-01 with an existing web server (webroot)
The CA fetches `http://<domain>/.well-known/acme-challenge/<token>` on **port 80**.
```bash
acme.sh --issue -d example.com -d www.example.com -w /var/www/html
```
nginx serving the challenge even when everything else redirects to HTTPS:
```nginx
location ^~ /.well-known/acme-challenge/ { root /var/www/html; default_type text/plain; }
location / { return 301 https://$host$request_uri; }
```
Other modes: `--standalone` (acme.sh binds port 80 itself, which must be free; socat is in the install prerequisites), `--nginx` (configures nginx temporarily and restores the original config), `--apache` (writes nothing to the web root). Neither web server mode changes your site config, so you still configure the certificate paths yourself.

## DNS-01 (wildcards, hosts without inbound 80)
```bash
export CF_Token=xxxx CF_Zone_ID=yyyy        # CF_Account_ID instead of CF_Zone_ID covers all zones of an account
acme.sh --issue --dns dns_cf -d example.com -d '*.example.com'
```
Environment variables used when issuing are saved in `~/.acme.sh/account.conf` for renewals; scope API tokens to the one zone. Use `--challenge-alias` to delegate `_acme-challenge` to a separate zone if the main DNS provider has no API.

## Install the certificate (never point servers at ~/.acme.sh directly)
```bash
acme.sh --install-cert -d example.com \
  --key-file /etc/ssl/private/example.com.key \
  --fullchain-file /etc/ssl/certs/example.com.fullchain.pem \
  --reloadcmd "systemctl reload nginx"
```
The install paths and reload command are remembered and rerun on each renewal.

## Options worth knowing
- `--keylength ec-256` (the default, ECDSA P-256) vs `--keylength 2048` (or 3072/4096) for RSA-only clients; `ec-384` also exists. ECC certs need `--ecc` on `--renew`/`--force` calls.
- `--server letsencrypt_test` for staging while testing; Let's Encrypt allows up to 5 certificates per exact same set of identifiers every 7 days.
- `--preferred-chain "<chain name>"` selects an alternate chain when the CA offers several (`--preferred-chain` takes the chain name or a part of it, per the wiki).

## Renewal
```bash
acme.sh --list                 # domains, created and renew dates
acme.sh --cron --home ~/.acme.sh   # what cron runs; renews every 30 days by default (earlier when the CA's ARI says so)
acme.sh --renew -d example.com --force
crontab -l | grep acme
```
Failures usually: port 80 blocked by firewall/CDN, an AAAA record pointing to a host without the challenge file, or a stale DNS API token.

## Verify
- [ ] `openssl s_client -connect example.com:443 -servername example.com </dev/null | openssl x509 -noout -dates -issuer` shows the new cert.
- [ ] A forced renew triggers the reload command and the service picks up the cert.

## Checked

Checked 2026-10-26 against acmesh-official/acme.sh (README, last commit 2026-10-16), its wiki repository (Server, Change-default-CA-to-ZeroSSL, Preferred-Chain, dnsapi, DNS-alias-mode, Install-preparations) and the Let's Encrypt rate limit and challenge type pages (letsencrypt/website, rate limits page last modified 2026-08-05). Confirmed: install command, ZeroSSL default since v3.0, --set-default-ca, letsencrypt_test, webroot, standalone, nginx and apache modes, Cloudflare variables, account.conf persistence, install-cert options, keylength values and ec-256 default, ARI, --challenge-alias, 5 certificates per exact set of identifiers per 7 days, HTTP-01 on port 80 only. Corrected: renewal happens every 30 days by default, not 60. Removed: the invented acme.sh.env sourcing step.

Method: documentation only; no commands were run.
