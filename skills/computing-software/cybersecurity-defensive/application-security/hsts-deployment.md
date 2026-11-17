---
id: computing-software.cybersecurity-defensive.application-security.hsts-deployment
name: hsts-deployment
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [security-headers, hsts, strict-transport-security, hsts-preload, tls, includesubdomains]
level: practitioner
status: docs-checked
description: "Deploy HTTP Strict Transport Security safely: ramp max-age, audit subdomains before includeSubDomains, then consider the preload list knowing removal is slow."
sources: ["https://www.rfc-editor.org/rfc/rfc6797.txt", "https://hstspreload.org/", "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HSTS deployment

**Goal:** browsers only ever connect over HTTPS to your domain, defeating SSL-stripping.

## Header
`Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
(63072000 s is 2 years, the OWASP example.) A host MUST NOT send the header over non-secure transport (RFC 6797
section 7.2). Redirect HTTP to HTTPS on the same host.

## Ramp
hstspreload.org suggests, with `includeSubDomains` from the start:
1. Examine all subdomains and nested subdomains, including internal ones that are not publicly reachable, and make
   sure each works over HTTPS. Internal-only hosts under the same domain (printers, intranet with a private CA)
   break once `includeSubDomains` is enforced.
2. Send the header on all HTTPS responses and ramp `max-age` in stages: `max-age=300; includeSubDomains` (5
   minutes), `max-age=604800; includeSubDomains` (1 week), `max-age=2592000; includeSubDomains` (1 month).
3. At each stage check for broken pages and watch site metrics, fix problems, and wait the full `max-age` of the
   stage before moving on. Then move to a long value such as 63072000.
4. If you want a gentler start, OWASP also shows `max-age=86400; includeSubDomains` as a short value for early rollout.
   Without `includeSubDomains` the policy does not cover subdomains, and cookies set from subdomains remain a risk.
5. Preload (optional): the site must serve a valid certificate; redirect HTTP to HTTPS on the same host if
   listening on port 80; serve all subdomains over HTTPS (including `www` if a DNS record exists); and serve the
   HSTS header on the base domain with `max-age` of at least 31536000 (1 year), `includeSubDomains` and `preload`.
   An additional HTTPS redirect must also carry the header. Submit via the form at hstspreload.org.

Add the header with your server's response-header directive (set it for every response, including errors).

## Gotchas
- Preload is hard to undo: removal takes months to reach users with a Chrome update and nothing is guaranteed for
  other browsers. hstspreload.org itself says preloading is not recommended in general (HSTS is), because
  browsers already upgrade HTTP navigations; preloading only helps against an active attacker on first visit.
  Do not add `preload` by default in templates or advice.
- `max-age=0` makes the browser stop treating the host as a known HSTS host, including `includeSubDomains`.
- HSTS does not protect the first visit unless the domain is preloaded.
- Removing the `preload` directive makes the site immediately eligible for the removal form.

## Verify
- [ ] Response headers on the apex and `www` show the header over HTTPS.
- [ ] hstspreload.org status check shows the expected state.
- [ ] All subdomains pass a TLS check before `includeSubDomains` goes live.

## Checked
2026-10-31. Confirmed against hstspreload.org (ramp values, submission requirements, preload caveats, removal),
RFC 6797 (no header over non-secure transport, `max-age=0` semantics) and the OWASP HSTS Cheat Sheet (63072000 as
2 years, 86400 example, subdomain cookie note). Removed unconfirmed: NGINX, Apache and IIS snippets and the IIS
version, the "301" redirect type, the `add_header` location-block gotcha, the CT-log inventory tip.
Method: documentation only; no commands were run.
