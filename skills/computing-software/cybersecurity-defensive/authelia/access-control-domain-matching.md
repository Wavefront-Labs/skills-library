---
id: computing-software.cybersecurity-defensive.authelia.access-control-domain-matching
name: access-control-domain-matching
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, access-control, domain, wildcard, session-domain, rule-criteria]
level: practitioner
status: docs-checked
description: "Match hosts in Authelia access control with domain lists and wildcards, keeping rule domains under the session cookie domain."
sources:
  - https://www.authelia.com/configuration/security/access-control/
  - https://www.authelia.com/reference/cli/authelia/authelia_access-control_check-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `domain` criterion accepts a string or a list. A list matches when any entry matches. If you also set `domain_regex`, the rule matches when either criterion does. One of the two is required.

```yaml
access_control:
  rules:
    - domain:
        - 'apple.example.com'
        - '*.example.com'
      policy: 'bypass'
```

Details:

- A leading `*.` matches any subdomain, so `*.example.com` matches `abc.example.com`. Quote any value starting with `*`, or YAML will misparse it.
- The older `{user}.` and `{group}.` wildcards are deprecated. They are translated into equivalent `domain_regex` rules and remain functional, but the docs strongly recommend migrating to `domain_regex`. They only match hostname characters (letters, digits, hyphen), so a username containing an underscore will not match.
- Domains must be the session cookie `domain` or a subdomain of it. Browsers only let a site write cookies for a domain it belongs to, so Authelia cannot protect hosts outside the cookie domain.

Check: run `authelia access-control check-policy --url https://abc.example.com` and confirm the intended rule is flagged.

## Checked

2026-11-08. Confirmed against the access control configuration page (domain and domain_regex criteria, the `*.` wildcard and quoting, the deprecated `{user}.` and `{group}.` wildcards and their hostname-character limit, the session domain requirement) and the check-policy CLI reference (--url). Removed: the unread session introduction source and an unsourced troubleshooting tip.

Method: documentation only; no commands were run.
