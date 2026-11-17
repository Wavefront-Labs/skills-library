---
id: computing-software.cloud-infrastructure-engineering.contour.contour-global-rate-limit-descriptors
name: contour-global-rate-limit-descriptors
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [rate-limiting, global-rate-limit, descriptors, ratelimitservice, extensionservice, generickey, remoteaddress, requestheader]
level: advanced
status: docs-checked
description: "HTTPProxy global rate limit policy: rateLimitService config, ExtensionService, descriptor entry types genericKey, remoteAddress, requestHeader, requestHeaderValueMatch."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/rate-limiting.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy global rate limiting descriptors

Global limiting queries an external RLS (any RateLimitService gRPC implementation, e.g. envoyproxy/ratelimit) per request. Policies define descriptors, not limits; the RLS decides.

1. Register the RLS as an ExtensionService (`projectcontour.io/v1alpha1`, `protocol: h2`, port 8081 in the example).
2. Reference it in the config file:

```yaml
rateLimitService:
  extensionService: projectcontour/ratelimit
  domain: contour
  failOpen: true
```
(`domain` is passed to the RLS on every request; `failOpen` lets requests proceed when the RLS fails to respond with a valid decision within the timeout defined on the extension service.)

3. Add `rateLimitPolicy.global.descriptors` on a virtual host or route:

```yaml
rateLimitPolicy:
  global:
    descriptors:
    - entries:
      - remoteAddress: {}
      - genericKey: {key: vhost, value: local.projectcontour.io}
    - entries:
      - requestHeader: {headerName: My-Header, descriptorKey: my-header-value}
```

Entry types:
- `genericKey`: static pair; `key` defaults to `generic_key`.
- `remoteAddress`: key `remote_address`, value is the trusted client IP from x-forwarded-for.
- `requestHeader`: value copied from a header; entry skipped if the header is absent.
- `requestHeaderValueMatch`: key `header_match`, static `value`, generated only when `headers` match (`present`, `notpresent`, `contains`, `notcontains`, `exact`, `notexact`); `expectMatch` defaults true.

If any entry in a descriptor cannot be generated, the whole descriptor is dropped. All generable descriptors in the policy are sent to the RLS.

## Checked

2026-11-08. Read the Contour main-branch config page rate-limiting.md in full (the local rate limiting sections are out of scope for this skill). Confirmed: global limiting queries an external RLS over gRPC, any RateLimitService implementation works, the ExtensionService example (h2, port 8081), the `rateLimitService` config keys, descriptor-only policies on virtual hosts and routes, and the four entry types with their keys, defaults and operators. Removed the unsourced `failOpen` default and the `enableXRateLimitHeaders` and `enableResourceExhaustedCode` options.

Method: documentation only; no commands were run.
