---
id: computing-software.cybersecurity-defensive.authelia.access-control-rule-order-and-bypass
name: access-control-rule-order-and-bypass
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, access-control, rule-matching, ordering, bypass, subject-rules, first-match]
level: advanced
status: docs-checked
description: "Avoid Authelia rule ordering mistakes: first full match wins, bypass rules go early, subject rules force authentication."
sources:
  - https://www.authelia.com/configuration/security/access-control/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two concepts explain nearly every surprising access control result.

Concept 1: sequential order. The first rule in the list whose criteria all match is applied. A broad early rule hides later specific ones. The documentation's example is a bypass rule for `/api` on `example.com` and every subdomain, followed by a `two_factor` rule for `app.example.com`. A request to `https://app.example.com/api` hits the first rule, so the second never applies.

Concept 2: subject criteria require authentication. A rule that depends on the user cannot be evaluated for an anonymous visitor. This covers the `subject` criterion and any `domain_regex` that uses the `User` or `Group` named groups. Such rules must not use `bypass`.

In addition, if every other criterion of a subject-based rule matches and no earlier rule matched, the user is immediately forwarded for authentication so Authelia can learn who they are and decide.

Consequences:

- Put bypass rules near the top, but check them against everything that follows them.
- If you have an identical pair, one bypass and one subject-based, the bypass rule generally goes first.

Check: the docs point to the `authelia access-control check-policy` command to evaluate whether your rules match a given request, and why not.

## Checked
2026-11-08. Read in full: the Access Control configuration page. Confirmed Rule Matching Concepts 1 and 2, the `/api` bypass example, subject-reliant criteria and the identical-pair advice. Removed: the one-factor wording (page says only forwarded for authentication), the `*`/`~` output markers and the `--username`/`--groups` flags (not on the page).
Method: documentation only; no commands were run.
