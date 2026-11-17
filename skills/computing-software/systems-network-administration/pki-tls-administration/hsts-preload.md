---
id: computing-software.systems-network-administration.pki-tls-administration.hsts-preload
name: hsts-preload
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [hsts-preload, pki-http-hardening, hsts, rfc6797, preload, strict-transport-security, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Deploy Strict-Transport-Security with a staged max-age rollout, includeSubDomains, and the hstspreload.org submission requirements."
sources:
  - https://www.rfc-editor.org/rfc/rfc6797
  - https://hstspreload.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HSTS and preload
Goal: browsers use HTTPS only for your domain.
```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```
Set it with your web server's response-header directive, on HTTPS responses only.

Rollout (hstspreload.org deployment recommendations):
1. Examine all subdomains and nested subdomains and make sure they work over HTTPS, including internal ones that are not publicly accessible.
2. Send the header on all HTTPS responses and ramp up max-age in stages: `max-age=300; includeSubDomains` (5 minutes), then `max-age=604800; includeSubDomains` (1 week), then `max-age=2592000; includeSubDomains` (1 month).
3. At each stage check for broken pages and monitor site metrics, fix problems, and wait the full max-age of that stage before moving on (wait a month in the last stage).

Preload list requirements (hstspreload.org, "Submission Requirements"):
- Serve a valid certificate.
- If you listen on port 80, redirect from HTTP to HTTPS on the same host.
- Serve all subdomains over HTTPS (including `www` if a DNS record for it exists); preloading applies to all subdomains, including internal ones.
- Serve the HSTS header on the base domain for HTTPS requests with max-age of at least 31536000 seconds (1 year), `includeSubDomains` and `preload`.
- If the HTTPS site serves an additional redirect, that redirect must itself carry the HSTS header.
- A site sending `preload` is treated as requesting inclusion; submit it through the form on hstspreload.org.

Things to know:
- hstspreload.org states that HSTS is recommended but preloading is not recommended, because its benefit over HSTS is minimal: Chrome and Safari already auto-upgrade HTTP navigations, so preload only helps when those upgrades fail under an active attacker.
- Preloading should be opt-in: do not emit `preload` by default from configuration generators.
- Removal is slow: domains can be removed, but it takes months for the change to reach users with a Chrome update, with no guarantee for other browsers. Removing `preload` from the header makes the site immediately eligible for the removal form.
- You must keep satisfying the requirements; sites may be removed automatically in future for failing to.
- RFC 6797 section 7.2: an HSTS host MUST NOT include the header in responses over non-secure transport.
- RFC 6797 section 12.1 ("No User Recourse"): a site issuing an HSTS policy opts in to connection termination on any certificate warning or error, with no click-through.
Gotcha: because of that no-click-through behaviour, a lapsed certificate on an HSTS site hard-fails, so certificate-expiry monitoring is mandatory.

Verify:
- [ ] `curl -sI https://example.com` shows the Strict-Transport-Security header.
- [ ] The hstspreload.org check passes before submission.

## Checked
Checked against the full text of hstspreload.org (deployment recommendations, submission requirements, removal, opt-in guidance) and RFC 6797 (sections 7.2, 12.1).
Removed: the nginx and Apache directive lines (not in cited pages), the 1 day and 2 year rollout stages (the site lists 5 minutes, 1 week, 1 month), and the "valid certificate hard-fail" wording now cites RFC 6797 section 12.1.
Method: docs-only read of cited pages, 2026-11-08
