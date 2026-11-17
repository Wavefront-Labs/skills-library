---
id: computing-software.qa-testing-engineering.test-automation.security-headers-and-tls-checks
name: security-headers-and-tls-checks
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [security-headers, tls-testing, testssl, hsts, content-security-policy, security-testing]
level: practitioner
status: docs-checked
description: "Check HTTP security headers and TLS configuration: HSTS, CSP, frame and content-type options, cookie flags, protocol versions, ciphers and certificates with testssl.sh."
sources:
  - https://owasp.org/www-project-secure-headers/
  - https://github.com/testssl/testssl.sh
  - https://owasp.org/www-project-web-security-testing-guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security headers and TLS configuration checks

**Goal:** confirm the deployed site sends the protective response headers and offers only strong TLS, and keep it that way with an automated check.

## Headers to expect

| Header | Typical good value |
|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` (add `preload` only deliberately) |
| `Content-Security-Policy` | restrictive `default-src 'self'`, no `unsafe-inline` scripts, `frame-ancestors 'none'` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` or stricter |
| `Permissions-Policy` | disable unused features (`camera=()`, `geolocation=()`) |
| `X-Frame-Options` | `DENY` (legacy; CSP `frame-ancestors` supersedes) |

Also check CORS: the wildcard `Access-Control-Allow-Origin: *` cannot be used with credentials (browsers reject it), so an API that needs cookies must name its origins.

```bash
curl -sI https://app.example | grep -iE 'strict-transport|content-security|x-content-type|referrer-policy|permissions-policy|x-frame'
```

Check error pages, redirects, static assets and API responses too; headers often only exist on the main HTML route.

## TLS
```bash
testssl.sh https://app.example
```
testssl.sh checks the supported protocols, ciphers and some cryptographic flaws on any TLS port (see its README and `--help` for options). Review the output for deprecated protocol versions and weak ciphers, the certificate chain and expiry, and any flagged vulnerabilities.

## Automate
Add a CI or synthetic-monitor test asserting the header set on key routes and alerting well before certificate expiry.

## Verify
The header check passes on HTML, API, error and asset responses, and testssl.sh reports no unaccepted findings.

## Checked

2026-11-02. Header values checked against MDN reference pages for Strict-Transport-Security (max-age, includeSubDomains, preload), Content-Security-Policy (default-src 'self', unsafe-inline, frame-ancestors 'none', similar to X-Frame-Options: deny), X-Content-Type-Options (nosniff), Referrer-Policy (strict-origin-when-cross-origin), Permissions-Policy (geolocation=()), X-Frame-Options and Access-Control-Allow-Origin (wildcard with credentials is an error). testssl.sh README confirms it checks protocols, ciphers and some cryptographic flaws on any TLS port. Removed because no fetched page states them: the Server/X-Powered-By banner advice, the --severity flag and Docker image invocation, the specific protocol, cipher and vulnerability list, OCSP stapling, the 30-day expiry figure and the SSL Labs sentence. The OWASP Secure Headers page is a script shell and was not readable.

Method: documentation only; no commands were run.
