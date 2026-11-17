---
id: computing-software.cybersecurity-defensive.nessus.web-app-scanning
name: web-app-scanning
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-templates, web-app-scanning, dast, web-application-tests, tenable-was, authenticated-web-scan]
level: practitioner
status: draft
description: "Scan web applications with Nessus web app tests or Tenable Web App Scanning: crawl scope, authentication, safe settings for production and result triage."
sources: ["https://docs.tenable.com/web-app-scanning/Content/Welcome.htm", "https://docs.tenable.com/nessus/Content/SettingsAssessment.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web application scanning

**Goal:** find web-layer flaws (injection, XSS, misconfiguration, outdated components)
on your own applications without breaking them.

## Pick the tool
- **Nessus Web Application Tests** (Advanced scan > Assessment > Web Applications, or the
  *Web Application Tests* template): basic crawling and generic CGI tests; adequate for
  simple sites and finding default content/outdated servers.
- **Tenable Web App Scanning (WAS)** in Tenable Vulnerability Management: modern crawler
  (JavaScript, SPAs), OWASP Top 10 coverage, API scanning from OpenAPI specs. Prefer it for
  real applications. OWASP ZAP is the free alternative.

## Nessus settings
- Scan web applications: on. *Maximum run time* (minutes) to bound crawl.
- *Use a custom User-Agent*; *start crawling from* `/` plus key paths; exclude logout and
  destructive URLs with the *excluded pages (regex)*: `/logout|/delete|/admin/reset`.
- Generic tests (XSS, SQL injection, command injection): enable on test environments; on
  production enable only with owner agreement because they submit forms.
- HTTP authentication: Credentials > HTTP (basic/NTLM/form-based or cookie import).

## WAS essentials
- Scope: target URL plus allowed domains; set *crawl depth* and max pages.
- Authentication: login form recorder (Selenium script), cookie, API key or bearer token;
  set a logged-in check pattern so the scanner knows when the session expires.
- Scan templates: *Overview* (passive, safe for production), *Scan* (full active),
  *API* (from OpenAPI), *Config audit*.
- Rate limits: requests per second to protect fragile apps.

## Triage
Confirm each finding by reproducing the request (WAS shows request/response). Typical false
positives: reflected input that is safely encoded, timing-based SQLi on slow pages.
Route confirmed findings to the app team with the request evidence.

## Gotchas
- Scanning with an admin account can create, change or delete data; use a dedicated test
  account with realistic but limited rights.
- WAFs block scanners; allowlist the scanner IP for the scan window or results show nothing.
- Forms that send email or SMS will spam users; exclude them.

## Verify
Scan an intentionally vulnerable app (OWASP Juice Shop, DVWA) in a lab with the same
settings and confirm known issues are detected.
