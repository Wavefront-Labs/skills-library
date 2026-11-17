---
id: computing-software.networking-hardware-and-wireless.envoy.header-to-metadata-filter
name: header-to-metadata-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, header-to-metadata, request-rules, metadata-namespace, envoylb, subset-routing, dynamic-metadata]
level: practitioner
status: docs-checked
description: "Copy request headers into dynamic metadata with the header_to_metadata filter to steer subset load balancing or later filters."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/header_to_metadata_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# header to metadata filter
The header_to_metadata filter reads headers (or cookies) and writes them into dynamic metadata, typically under the `envoy.lb` namespace so subset load balancing can route on it, with `on_header_present` and `on_header_missing` actions. The docs' example:

```yaml
http_filters:
- name: envoy.filters.http.header_to_metadata
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.header_to_metadata.v3.Config
    request_rules:
    - header: x-version
      on_header_present:
        metadata_namespace: envoy.lb
        key: version
        type: STRING
      on_header_missing:
        metadata_namespace: envoy.lb
        key: default
        value: "true"
        type: STRING
      remove: false
```
Pair it with a cluster `lb_subset_config` selector on `version` and a `default_subset`. `remove: false` keeps the header on the forwarded request. Further examples cover cookies, regex substitution and route-level config.

Gotchas: the filter must sit before the router; metadata written under another namespace does not affect load balancing unless the route `metadata_match` reads it. Verify with `GET /clusters` per-host stats and `%DYNAMIC_METADATA(envoy.lb)%` in the access log.

## Checked

2026-11-03. Confirmed against: header_to_metadata filter page and proto (request_rules, on_header_present, on_header_missing, remove) and the substitution formatter page. Removed or corrected: the claim about subset fallback behaviour.

Method: documentation only; no commands were run.
