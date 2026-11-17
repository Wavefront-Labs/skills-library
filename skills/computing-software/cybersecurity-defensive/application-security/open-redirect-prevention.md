---
id: computing-software.cybersecurity-defensive.application-security.open-redirect-prevention
name: open-redirect-prevention
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [input-validation, open-redirect, unvalidated-redirects, returnurl, oauth-redirect, url-parsing, cwe-601]
level: practitioner
status: docs-checked
description: "Prevent open redirects in login return URLs, OAuth flows and link trackers: avoid user-supplied URLs, map IDs server-side, allowlist parsed URL components."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html", "https://cwe.mitre.org/data/definitions/601.html", "https://datatracker.ietf.org/doc/html/rfc9700"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Open redirect prevention

A redirect that takes its destination from untrusted input lets an attacker build a link on your trusted
domain that sends users to a malicious site (phishing). Forwards built from user input can also reach
functions the user is not authorised for.

## Options, strongest first
1. **Avoid redirects and forwards**, or do not let the destination come from user input.
2. **Short name, ID or token mapped server-side** to a full target URL: highest protection against URL
   tampering. Watch for enumeration (a user cycling IDs to list all targets).
3. **If user input cannot be avoided**: the value must be valid, appropriate for the application and
   authorised for the user.
4. **Local return URLs**: use a framework helper that rejects non-local destinations (OWASP names ASP.NET Core
   `LocalRedirect` or `IsLocalUrl`).
5. **External destinations**: use a maintained URL parser compatible with the redirect API and browser
   interpretation; compare parsed scheme, canonical host and effective port against an explicit allowlist;
   constrain the path if only certain endpoints are allowed; reject userinfo and ambiguous input; redirect to
   the validated URL, not a transformed copy. Do not use raw prefix or suffix matching.
6. Optionally send users through an interstitial page that shows the destination and asks them to confirm.

## OAuth/OIDC
RFC 9700 (OAuth 2.0 security best current practice) is the reference for redirect URI handling by
authorization servers; read its redirect URI sections rather than relying on summaries.

## Forwards
Check that the user is authorised for the target of any server-side forward built from input.

## Verify
Tests with hostile destination values (other hosts, userinfo in the URL, lookalike hostnames) resolve to a safe
default or are rejected; DAST open-redirect checks pass on login, logout and SSO endpoints.

## Checked
2026-11-01. Confirmed against the OWASP Unvalidated Redirects and Forwards Cheat Sheet (prevention list,
parsed-component allowlist, userinfo, no prefix/suffix matching, enumeration warning, interstitial page) and
that RFC 9700 and CWE-601 pages exist. Removed: the Python snippet, framework helpers other than
ASP.NET Core `IsLocalUrl`/`LocalRedirect`, the bypass payload list, the client-side `javascript:` note and the
OAuth exact-matching detail (not re-read in the RFC this batch).
Method: documentation only; no commands were run.
