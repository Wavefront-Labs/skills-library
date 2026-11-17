---
id: computing-software.cybersecurity-defensive.application-security.security-misconfiguration-review
name: security-misconfiguration-review
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [owasp-top-10, security-misconfiguration, a05, verbose-errors, default-accounts, debug-mode, hardening-review]
level: practitioner
status: draft
description: "Review a web application for OWASP A05 security misconfiguration: debug modes, default accounts, verbose errors, exposed admin and actuator endpoints, headers and cloud storage."
sources: ["OWASP Top 10 2021 - A05 Security Misconfiguration", "OWASP Web Security Testing Guide - Configuration and Deployment Management Testing", "OWASP Secure Headers Project"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security misconfiguration review (OWASP A05)

**Goal:** find configuration that turns a secure codebase into an exposed deployment, and make it repeatable.

## Checklist per environment
1. **Debug/dev features off:** Django `DEBUG=False`, Flask debugger off (Werkzeug console is RCE), Laravel `APP_DEBUG=false`, ASP.NET `customErrors`/`DeveloperExceptionPage` not in production, Rails `consider_all_requests_local=false`.
2. **Error handling:** generic error pages; no stack traces, SQL errors or framework versions in responses.
3. **Admin and management endpoints:** Spring Boot actuator (`/actuator/env`, `/heapdump`) only `health` exposed publicly; `/server-status`, `/phpinfo.php`, `/.git/`, `/.env`, Swagger UI, GraphQL introspection in production.
4. **Default accounts and samples:** CMS/admin consoles, Tomcat manager, sample apps, default DB users removed or changed.
5. **Headers:** CSP, HSTS, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `frame-ancestors`; remove `Server`/`X-Powered-By` version banners.
6. **Directory listing** disabled; unnecessary HTTP methods (TRACE, PUT, DELETE on static) disabled.
7. **Cloud storage and services:** buckets not public, CORS not wildcard with credentials, metadata service protected (IMDSv2).
8. **Dependencies and platform** patched; unused features/modules removed.
9. **XML parsers** with external entities disabled (XXE was folded into A05 in 2021).

## Quick probes
```
for p in .git/HEAD .env actuator/env server-status phpinfo.php swagger-ui.html graphql; do
  printf "%s " $p; curl -s -o /dev/null -w "%{http_code}\n" https://target.example/$p; done
```
Nuclei templates (`misconfiguration/`, `exposures/`) automate the same at scale.

## Make it stick
- Encode settings in IaC and app config with environment-specific overlays; production overlay reviewed by security.
- Scan continuously (ZAP baseline, nuclei) and on every deploy.

## Verify
- [ ] Forced error returns a generic page in production.
- [ ] None of the probe paths return 200 with content.
