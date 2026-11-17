---
id: computing-software.cloud-infrastructure-engineering.azure.application-gateway-http-to-https-and-redirect-configurations
name: application-gateway-http-to-https-and-redirect-configurations
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, application-gateway, http-to-https-redirect, redirect-configuration, url-path-map, 301-redirect]
level: practitioner
status: docs-checked
description: "Configure Application Gateway redirects: HTTP to HTTPS listener redirects, external URL and path-based redirects, status codes, and keeping path/query strings."
sources: ["https://learn.microsoft.com/azure/application-gateway/redirect-overview", "https://learn.microsoft.com/azure/application-gateway/redirect-http-to-https-cli", "https://learn.microsoft.com/cli/azure/network/application-gateway/redirect-config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application Gateway redirects

**Goal:** every HTTP request lands on HTTPS (and legacy URLs on new ones) with the right status code and no lost paths.

## HTTP to HTTPS
```bash
az network application-gateway frontend-port create -g rg --gateway-name agw-prod -n port-80 --port 80
az network application-gateway http-listener create -g rg --gateway-name agw-prod -n lst-www-http \
  --frontend-port port-80 --host-name www.contoso.com
az network application-gateway redirect-config create -g rg --gateway-name agw-prod -n redir-www-https \
  --type Permanent --target-listener lst-www-https --include-path true --include-query-string true
az network application-gateway rule create -g rg --gateway-name agw-prod -n rule-www-http \
  --http-listener lst-www-http --redirect-config redir-www-https --rule-type Basic --priority 200
```
The redirect configuration object names either a target listener or an external site, with options to append the path and query string.

## Types
| `--type` | Code | Use |
|---|---|---|
| Permanent | 301 | HTTP->HTTPS (Learn recommends 301 for this), permanent URL moves |
| Found | 302 | Temporary moves; client keeps using the original URL |
| SeeOther | 303 | Redirects the client to a different resource named in `Location` |
| Temporary | 307 | Temporary; the client must not change the request method |

## Redirect to an external site or another path
```bash
az network application-gateway redirect-config create -g rg --gateway-name agw-prod -n redir-blog \
  --type Found --target-url "https://blog.contoso.com" --include-path false --include-query-string true
```
Path-based: in a URL path map, a path rule (e.g. `/old/*`) can reference a redirect configuration instead of a backend.

## Gotchas
- Use 302 while validating a new redirect, then switch to 301.
- `--target-listener` and `--target-url` are alternatives; `--include-path` and `--include-query-string` control what is appended.

## Verify
- [ ] `curl -I http://www.contoso.com/a?b=1` returns 301 with `Location: https://www.contoso.com/a?b=1`.

## Checked
2026-10-28. Confirmed in Learn redirect-overview and the `az network application-gateway redirect-config` reference: redirect to a listener
or external site, path-based redirection, 301/302/303/307 meanings, `--type` values (Found, Permanent, SeeOther, Temporary),
`--include-path`, `--include-query-string`. check_commands found all commands valid. Removed: the v2 rule priority sentence,
browser caching of 301, listener-versus-URL semantics, the HSTS tip and the Front Door advice.
Method: documentation only; no commands were run.
