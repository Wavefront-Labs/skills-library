---
id: computing-software.networking-hardware-and-wireless.envoy.rbac-http-filter
name: rbac-http-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, rbac, role-based-access-control, policies, permissions, principals, shadow-mode, rbac-access-denied]
level: practitioner
status: docs-checked
description: "Authorise requests inside Envoy with the RBAC filter using ALLOW or DENY policies, shadow mode and per-route overrides."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/rbac_filter.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/security/rbac_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rbac http filter
RBAC authorises in-process from policies in the filter config, unlike ext_authz. It can run as a network filter (unauthorised connections are closed) or an HTTP filter (403), or both. A policy is a list of permissions (what: method, path, port) and principals (who: for example the URI SAN of the downstream client certificate or an IP). Rules are either an ALLOW/DENY policy list or the matching API.

```yaml
http_filters:
- name: envoy.filters.http.rbac
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.rbac.v3.RBAC
    rules:
      action: ALLOW
      policies:
        admin-only:
          permissions: [ { url_path: { path: { prefix: /admin } } } ]
          principals: [ { authenticated: { principal_name: { exact: spiffe://example.com/ops } } } ]
```
Shadow mode (`shadow_rules`) evaluates policies without enforcing and records stats and dynamic metadata, so roll out new rules there first. Overriding or disabling per virtual host, route or weighted cluster uses `RBACPerRoute`.

Denied requests set `RESPONSE_CODE_DETAILS` to `rbac_access_denied_matched_policy[policy_name]` (`none` if no policy matched), which separates an Envoy deny from an upstream 403. Stats live under `http.<stat_prefix>.rbac.`.

Gotchas: path-based policies need `normalize_path` and `merge_slashes` on the HCM or encoded paths slip through. An ALLOW list with no matching policy denies everything. Verify with the response code details in the access log.

## Checked

2026-11-03. Confirmed against: rbac_filter.rst (config and arch overview) and the RBAC protos (policies, shadow_rules, RBACPerRoute, response code details). Removed or corrected: nothing.

Method: documentation only; no commands were run.
