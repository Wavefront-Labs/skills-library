---
id: computing-software.cloud-infrastructure-engineering.contour.contour-cors-policy
name: contour-cors-policy
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [corspolicy, cors, alloworigin, allowmethods, maxage, allowcredentials, allowprivatenetwork, preflight]
level: practitioner
status: docs-checked
description: "HTTPProxy corsPolicy on a virtual host: allowOrigin exact or regex, methods, headers, exposeHeaders, maxAge, allowCredentials and allowPrivateNetwork."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/cors.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy CORS policy

`corsPolicy` is set on `spec.virtualhost` and applies to every route of that host.

```yaml
spec:
  virtualhost:
    fqdn: www.example.com
    corsPolicy:
      allowCredentials: true
      allowPrivateNetwork: true
      allowOrigin:
      - https://client.example.com
      - http[s]?:\/\/some-site-[a-z0-9]+\.example\.com
      allowMethods: [GET, POST, OPTIONS]
      allowHeaders: [authorization, cache-control]
      exposeHeaders: [Content-Length, Content-Range]
      maxAge: "10m"
```

- Controls `Access-Control-Allow-Origin`, `-Methods`, `-Headers`, `-Expose-Headers`, `-Max-Age`, `-Allow-Private-Network` and `-Allow-Credentials`.
- `allowOrigin`: `"*"` for any origin, exact origins, or regular expressions. Patterns must be valid regex; globs such as `*.foo.com` are not accepted or may match wrongly.
- `maxAge` is a Go duration (units ns, us or µs, ms, s, m, h); only positive values; `0` disables preflight caching so every cross-origin request needs an `OPTIONS` check.
- `allowHeaders` are passed to the upstream; `exposeHeaders` become readable to the cross-origin client.

## Checked

2026-11-08. Read the Contour main-branch config page cors.md in full. Confirmed: corsPolicy on the virtualhost applies to all routes, the listed response headers, the `allowOrigin` spelling (the draft had `alloworigin`, fixed), `"*"`, exact and regex origins, the glob warning, the Go duration format with its units, positive-only values and `0` disabling the cache, and the allowHeaders/exposeHeaders roles. Removed the unsourced remark about `allowCredentials` combined with `"*"` origins.

Method: documentation only; no commands were run.
