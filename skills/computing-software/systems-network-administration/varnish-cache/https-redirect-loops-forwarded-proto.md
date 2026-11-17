---
id: computing-software.systems-network-administration.varnish-cache.https-redirect-loops-forwarded-proto
name: https-redirect-loops-forwarded-proto
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [x-forwarded-proto, redirect-loop, tls-offload, vary-forwarded-proto]
level: advanced
status: docs-checked
description: "Avoid HTTP-to-HTTPS redirect loops behind a TLS proxy: set X-Forwarded-Proto and make it a cache variation via Vary, since Varnish has no scheme awareness by default."
sources:
  - https://www.varnish.org/docs/tutorials/avoid-http-to-https-redirect-loops-varnish/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# https redirect loops forwarded proto

With a TLS terminator in front and plain HTTP to the origin, the origin sees only HTTP and keeps redirecting to HTTPS. Varnish caches the 301 (cacheable by default), so the browser loops. The tutorial recommends native TLS (Varnish 9; Varnish Enterprise has had it for years) instead of a TLS proxy such as Hitch.

1. Tell the origin the scheme with `X-Forwarded-Proto: https`. If a pure TLS proxy cannot set it, set it in VCL by listener port (here a proxy on 443 forwarding to 8443):

```vcl
import std;
sub vcl_recv {
    if (!req.http.X-Forwarded-Proto) {
        if (std.port(server.ip) == 8443) { set req.http.X-Forwarded-Proto = "https"; }
        else { set req.http.X-Forwarded-Proto = "http"; }
    }
}
```

Proxy-side directives from the page: HAProxy `http-request set-header X-Forwarded-Proto https`; Apache `RequestHeader set`; Nginx `proxy_set_header X-Forwarded-Proto https;`.

2. The hash is built from URL and Host, with no scheme, so only one version is cached. If HTTP is requested first the redirect is cached and the loop persists; if HTTPS is cached first, plain HTTP clients get HTTPS references (mixed content). Fix by returning `Vary: X-Forwarded-Proto`, from the application or in VCL:

```vcl
sub vcl_backend_response {
    if (beresp.http.Vary) { set beresp.http.Vary = beresp.http.Vary + ", X-Forwarded-Proto"; }
    else { set beresp.http.Vary = "X-Forwarded-Proto"; }
}
```

Result: separate HTTP and HTTPS cache variations.

With native TLS: add `.ssl = 1;` to the backend (port 443) to reach an HTTPS origin, and redirect plain HTTP in VCL (`return (synth(301))` with a location header copied in `vcl_synth`). If the origin is plain HTTP you still need X-Forwarded-Proto and the Vary; detect TLS by port 443 or with `tls.is_tls()` from the tls VMOD.

## Checked

Method: 2026-11-08 docs-only read of the cited tutorial. Removed the earlier `hash_data(req.http.X-Forwarded-Proto)` alternative, which the page does not state. Added the page's native TLS and tls.is_tls() notes. Other claims match.
