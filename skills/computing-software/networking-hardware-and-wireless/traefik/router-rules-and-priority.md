---
id: computing-software.networking-hardware-and-wireless.traefik.router-rules-and-priority
name: router-rules-and-priority
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, rule, router, priority, host, pathprefix, matchers]
level: practitioner
status: docs-checked
description: "Write Traefik v3 router rules with Host, PathPrefix, Header and ClientIP matchers and predict which router wins by rule length or explicit priority."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/routing/rules-and-priority.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/routing/router.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# router rules and priority
Matchers available: Header, HeaderRegexp, Host, HostRegexp, Method, Path, PathPrefix, PathRegexp, Query, QueryRegexp and ClientIP. Values go in backticks or escaped double quotes. Combine with `&&`, `||`, `!` and parentheses. Regexes use Go syntax.

```yaml
http:
  routers:
    api:
      rule: "Host(`example.com`) && PathPrefix(`/api`)"
      priority: 100
      service: api-svc
```
Priority: by default a router's priority equals the length of its rule string, so the longest rule wins. The docs example: `HostRegexp([a-z]+\.traefik\.com)` has length 34 and `Host(foobar.traefik.com)` has 26, so the regex router wins unless you set `priority`. `priority: 0` means the default. Negative values are allowed; the maximum is MaxInt64 minus 1000. Ties across providers are decided by `providers.precedence`.

Gotchas: the stars of a double wildcard host do not count toward length, so the reference gives priorities of 23, 21 and 20 for foo.example.com, *.example.com and **.example.com. The `*` and `**` host wildcards need the v3 rule syntax, which is the default. The per-router `ruleSyntax` option inherits its default from the install option `core.defaultRuleSyntax`.

## Checked
2026-11-03. Confirmed against the Traefik HTTP rules and priority reference page and router page: matcher list, quoting, Go regexp syntax, priority equals rule length (34 versus 26 example), `priority: 0`, negative values, the maximum (MaxInt64 minus 1000), cross-provider ties and the wildcard length rule. Removed: the claim that `ruleSyntax` is deprecated, the single-quote remark and the dashboard and curl Verify step.
Method: documentation only; no commands were run.


