---
id: computing-software.cybersecurity-defensive.authelia.access-control-resources-and-methods
name: access-control-resources-and-methods
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, access-control, resources, methods, path-matching, api-bypass]
level: practitioner
status: docs-checked
description: "Scope Authelia rules by URL path with resources regexes and by HTTP verb with methods, including the recommended API prefix pattern."
sources:
  - https://www.authelia.com/configuration/security/access-control/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two criteria narrow a rule below the hostname.

`resources` is a list of regular expressions matched against the path and query of the request. Any one match makes the criterion match.

```yaml
access_control:
  rules:
    - domain: 'app.example.com'
      policy: 'bypass'
      resources:
        - '^/api([/?].*)?$'
      methods:
        - 'GET'
        - 'HEAD'
```

`methods` lists HTTP verbs the rule applies to. Because all criteria must match, this rule bypasses only GET and HEAD requests to `/api`, `/api/...` or `/api?...` on that host.

Guidance from the documentation:

- Use the `([/?].*)?$` suffix after the prefix so the trailing slash and the query string are both matched; the docs warn that a bare `.*` can allow unintended paths.
- The path is case-sensitive, matching the HTTP specification. Verify your proxy and app also treat paths case-sensitively, otherwise `/API` could reach the app without matching your rule.
- Regexes must be escaped properly; the docs suggest Regex 101 with the Golang option for debugging.
- Authelia cannot preserve request data when redirecting, so non-GET/HEAD methods can lose form data; use `methods` mainly for CORS preflight (`OPTIONS`) bypass or where security essentially needs it.
- Unmatched requests fall through to later rules or the default policy, so put a more specific bypass above broader rules.

The docs recommend `resources` for basic needs and describe `query` as the advanced option for matching query argument keys.

Check: the docs point to the `authelia access-control check-policy` command to evaluate whether your rules match a given request, and why not.

## Checked
2026-11-08. Read in full: the Access Control configuration page. Confirmed `resources` and `methods` behaviour, the `/api` bypass example, case sensitivity advice and the methods caveat. Removed: the single-quote YAML claim, the `/apixyz` example, the advice to prefer `query` (page recommends `resources` for basic needs) and the check-policy flags.
Method: documentation only; no commands were run.
