---
id: computing-software.digital-privacy-hygiene.password-hygiene.well-known-change-password-url
name: well-known-change-password-url
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, change-password-url, password-rotation, breach-response]
level: practitioner
status: draft
description: "Use the well-known change-password URL to jump straight to a site's password change page, check whether a site supports it, and set it up for your own site."
sources:
  - "https://w3c.github.io/webappsec-change-password-url/"
  - "https://developer.apple.com/documentation/security/password_autofill"
  - "https://web.dev/articles/change-password-url"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Well-known change-password URL

**Goal:** rotate breached or reused passwords quickly by going straight to each site's change-password page.

## The standard
W3C WebAppSec proposal: `https://example.com/.well-known/change-password` redirects to the site's real
change-password page. Safari, Chrome and some password managers use it for "Change password" buttons in their
breach/reuse alerts.

## Use it
- In your password manager's or browser's compromised-password report, click "Change password" where offered.
- Manually: type `https://site.example/.well-known/change-password` in the address bar.

## Check support
```
curl -sI https://github.com/.well-known/change-password | grep -i -E '^(HTTP|location)'
```
A 302/303 with a `Location:` to a settings page = supported. 404 = not supported; find the page manually.

## For your own website
Configure a redirect, e.g. nginx:
```
location = /.well-known/change-password { return 302 /account/password; }
```

## Gotchas
- Some sites redirect to a login page first; you'll land on change-password after logging in.
- Don't use the URL from a link in an email; type it, so you're on the real domain.
