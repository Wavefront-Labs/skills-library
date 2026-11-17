---
id: computing-software.cloud-infrastructure-engineering.nginx.proxy-pass-uri-handling
name: proxy-pass-uri-handling
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, proxy-pass, reverse-proxy, uri]
level: practitioner
status: docs-checked
description: "proxy_pass semantics: with and without a URI part, regex and named locations, rewrite break and variables, with examples of what the upstream sees."
sources: ["https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Whether `proxy_pass` carries a URI changes what the backend receives.

```nginx
location /api/ { proxy_pass http://app:8080;      }  # /api/x -> /api/x  (no URI: request URI passed as sent)
location /api/ { proxy_pass http://app:8080/;     }  # /api/x -> /x       (matched prefix replaced)
location /api/ { proxy_pass http://app:8080/v2/;  }  # /api/x -> /v2/x
```

- With a URI on `proxy_pass`, the part of the normalized request URI that matches the location is replaced by it.
- Without a URI, the request URI is passed in the form the client sent (or the full normalized changed URI when it was rewritten).
- The part to replace cannot be determined in a regular-expression location or a named location; there `proxy_pass` must have no URI.
- After `rewrite ... break;` in the same location, the URI on `proxy_pass` is ignored and the full changed URI is sent.
- With variables in `proxy_pass`, a URI given in the directive is passed as is, replacing the original request URI (example: `proxy_pass http://127.0.0.1$request_uri;`). If the address is a domain name, it is searched among the defined server groups first, then resolved with a `resolver`.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_proxy_module page (proxy_pass section): every bullet above and the three mappings.
Removed as unconfirmed: the claim that trailing-slash mismatches are the most common cause of 404s, and the tcpdump/echo verify step.
Method: documentation only; no commands were run.
