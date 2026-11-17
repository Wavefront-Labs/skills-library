---
id: computing-software.cybersecurity-defensive.authelia.access-control-regex-and-named-groups
name: access-control-regex-and-named-groups
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, access-control, domain-regex, regular-expressions, named-groups, case-insensitive]
level: advanced
status: docs-checked
description: "Write safe Authelia domain_regex and resources patterns, with User and Group named groups, escaping and case sensitivity."
sources:
  - https://www.authelia.com/configuration/security/access-control/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`domain_regex` and `resources` use Go regular expressions. Test them on Regex 101 with the Golang flavour selected.

```yaml
access_control:
  rules:
    - domain_regex:
        - '^user-(?P<User>\w+)\.example\.com$'
        - '^group-(?P<Group>\w+)\.example\.com$'
      policy: 'two_factor'
```

With the named groups `User` and `Group`, the request matches only when the captured text equals the signed-in username or one of their groups. In the documentation's example, user `john` in groups `example` and `example1` matches `user-john`, `group-example` and `group-example1` hosts, but not `user-fred` or `group-admin`.

Practical rules:

- The docs' examples anchor patterns with `^` and `$`; escape `.`, `*`, `+` and `?` when you mean the literal character, and test rules before deploying.
- Authelia treats regexes as case-insensitive in the appropriate places by prefixing `(?i)`, unlike the Go default. The `resources` path itself is matched case-sensitively as HTTP specifies, so check the proxy and the application also treat paths that way.
- For an API prefix, end with `([/?].*)?$`, as in `^/api([/?].*)?$`. A bare `.*` can match unintended paths.
- A rule using named groups depends on the subject, so it needs authentication and cannot use `bypass`.

Check: the docs point to the `authelia access-control check-policy` command to evaluate whether your rules match a given request, and why not.

## Checked
2026-11-08. Read in full: the Access Control configuration page. Confirmed the named-group example, Named Regex Groups table, the `(?i)` default and `(?-i)` override, resources case sensitivity and the `([/?].*)?$` advice. Reworded the anchoring bullet (page examples anchor, but it is not a stated rule) and removed the near-miss test procedure.
Method: documentation only; no commands were run.
