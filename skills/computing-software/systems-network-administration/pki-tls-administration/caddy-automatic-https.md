---
id: computing-software.systems-network-administration.pki-tls-administration.caddy-automatic-https
name: caddy-automatic-https
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [caddy-automatic-https, pki-caddy, caddy, acme, on-demand-tls, local-ca, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Caddy automatic HTTPS: what activates it, ACME challenge requirements, local CA trust, on-demand TLS restrictions, retry behaviour and storage."
sources:
  - https://caddyserver.com/docs/automatic-https
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Caddy automatic HTTPS
Goal: zero-touch TLS for a site.
- Caddy serves public DNS names with certificates from a public ACME CA (Let's Encrypt and ZeroSSL by default), keeps them renewed and redirects HTTP (port 80) to HTTPS (port 443). IP addresses and local names (localhost, .local, .internal, .home.arpa) get certificates from Caddy's own local CA.
- Public-name requirements: A/AAAA records point to the server, ports 80 and 443 are open externally and bindable by Caddy, the data directory is writeable and persistent (the default storage needs a writeable, persistent `$HOME`), and the domain appears in the config.
- Activation needs a hostname or IP in the config (for example a Caddyfile site address). It is prevented by disabling it, giving no hostnames, listening only on the HTTP port, an `http://` site address prefix, or manually loading certificates (unless `ignore_loaded_certificates`).
- Challenges: HTTP (port 80) and TLS-ALPN (port 443) are on by default and one is picked at random, then learned by success. The DNS challenge needs no open ports but needs DNS provider credentials (provider support is by plugin); once enabled, the other challenges are off by default. A CNAME can delegate `_acme-challenge` to another zone.
- Wildcards: only a single left-most `*` label qualifies (`*.example.com`). Let's Encrypt requires the DNS challenge for wildcards.
- Local CA: root and intermediate are stored under `pki/authorities/local` in the data directory. Caddy tries to install the root into the system trust store on first use and may prompt for a password; `caddy trust` retries as a privileged user and `caddy untrust` removes it. Auto-install is not guaranteed, for example in containers or unprivileged services; clients that do not trust the root show errors.
- On-demand TLS gets a certificate during the first handshake for an unknown SNI name. It must be enabled and restricted: the primary restriction is an `ask` endpoint (global `on_demand_tls` option in the Caddyfile) that Caddy queries before obtaining a certificate. Restrictions are global, not per site.
- Errors: on failure Caddy retries once, then tries the next challenge type, then the next issuer, then backs off exponentially (at most 1 day between attempts, for up to 30 days). Internal rate limit is 10 attempts per ACME account per 10 seconds.
- Testing: point at the Let's Encrypt staging endpoint `https://acme-staging-v02.api.letsencrypt.org/directory`; production rate limits can block HTTPS for up to a week.
- Instances sharing the same storage coordinate certificate management as a cluster.
Gotcha: on-demand TLS without an `ask` restriction lets any hostname pointed at the server trigger issuance.
Verify:
- [ ] Logs show certificates obtained for each qualifying hostname.
- [ ] `curl -vI https://<hostname>` shows a publicly trusted certificate (or the local CA once its root is trusted).

## Checked
Confirmed 2026-11-08 against the Caddy Automatic HTTPS page. Removed (not on the page): the sample Caddyfile with a Cloudflare DNS block and `email` global option, `$XDG_DATA_HOME` path, OCSP stapling, `tls internal`, `xcaddy` builds and `caddy validate`.
Method: docs-only read of cited pages, 2026-11-08
