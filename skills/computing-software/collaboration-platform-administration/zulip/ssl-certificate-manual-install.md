---
id: computing-software.collaboration-platform-administration.zulip.ssl-certificate-manual-install
name: ssl-certificate-manual-install
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [ssl-certificates, certificate-chain, zulip-combined-chain]
level: practitioner
status: docs-checked
description: "Install your own TLS certificate for Zulip at the documented key and combined-chain paths, include intermediates, and test the chain with SSL Labs or curl."
sources: ["https://zulip.readthedocs.io/en/latest/production/ssl-certificates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manual SSL certificate install

Zulip serves HTTPS only, so every server needs a certificate. If you already have one, place or symlink the files at:

- `/etc/ssl/private/zulip.key` for the private key
- `/etc/ssl/certs/zulip.combined-chain.crt` for the certificate

The certificate file must contain your certificate plus the full chain, including any intermediate certificates from your CA. A missing intermediate may work in some browsers but fail in others and in the Zulip mobile and desktop apps. Desktop apps can be configured with a custom CA to trust an internal authority.

Testing: opening the site in a browser is not enough, since some browsers tolerate errors others reject. Instead:

- If the server is public, use the SSL Labs tester and look for "Chain issues". Any listed means intermediates are missing.
- Or run `curl -SsI https://zulip.example.com` from another machine. Confirm on the same machine that `curl -SsI https://incomplete-chain.badssl.com` produces an error, because curl on some systems, including Macs, accepts incomplete chains and would give a false pass.

If you need wildcard certificates, have an existing certificate workflow, or the server is not on the public Internet, manual install is the route (Certbot automation is aimed at public servers).

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/ssl-certificates.html (zulip.readthedocs.io, latest). Removed: the nginx reload step (documented only for self-signed certificates) and the closing internal-versus-commercial CA line.

Method: documentation only; no commands were run.
