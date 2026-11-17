---
id: computing-software.cybersecurity-defensive.authelia.access-control-default-policy-and-rules
name: access-control-default-policy-and-rules
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, access-control, default-policy, rules, bypass, one-factor, two-factor, deny]
level: practitioner
status: docs-checked
description: "Structure Authelia access_control with a deny default, ordered rules, and the four policies deny, bypass, one_factor and two_factor."
sources:
  - https://www.authelia.com/configuration/security/access-control/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`access_control` decides, per request seen by the proxy, which policy applies.

```yaml
access_control:
  default_policy: 'deny'
  rules:
    - domain: 'private.example.com'
      policy: 'one_factor'
      subject:
        - ['group:admins']
```

`default_policy` applies when no rule matches. The documentation recommends `deny`, and advises that sites you do not want to protect at all should not be configured in the proxy to call Authelia in the first place, for performance reasons.

A rule matches only when every criterion in it matches. Criteria are `domain`, `domain_regex`, `resources`, `subject`, `networks`, `methods` and `query`. The policy of the first matching rule applies.

Policies:

- `deny` refuses access. Use it to block an API that has no authentication of its own.
- `bypass` skips all authentication. It cannot be combined with a `subject` restriction, because the subject is unknown below one-factor.
- `one_factor` needs username and password. A user who also did 2FA passes it.
- `two_factor` needs a second factor and is the highest level.

This section does not apply to OpenID Connect 1.0 (see the Authelia FAQ).

Check: the docs point to the `authelia access-control check-policy` command to evaluate whether your rules match a given request, and why not.

## Checked
2026-11-08. Read in full: the Access Control configuration page. Confirmed `default_policy`, rule matching, the criteria list, the four policies and the OpenID Connect note. Removed: the "saves a round trip" claim (page says performance), the OpenID authorization-policy claim and the first-full-match marking of check-policy output.
Method: documentation only; no commands were run.
