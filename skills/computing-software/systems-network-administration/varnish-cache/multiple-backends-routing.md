---
id: computing-software.systems-network-administration.varnish-cache.multiple-backends-routing
name: multiple-backends-routing
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [multiple-backends, backend-hint, req-backend-hint, unused-backend]
level: practitioner
status: docs-checked
description: "Send requests to different backends by URL or Host with req.backend_hint, and avoid the compile error for unused backends."
sources:
  - https://www.varnish.org/docs/tutorials/multiple-backends/
  - https://www.varnish.org/docs/users-guide/vcl-backends/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# multiple backends routing

Define several backends and choose one by conditionally assigning `req.backend_hint` in `vcl_recv`. Here every cache miss goes to `default` except images:

```vcl
vcl 4.1;
backend default { .host = "backend.example.com"; .port = "80"; }
backend image   { .host = "image.example.com";   .port = "80"; }

sub vcl_recv {
    if (req.url ~ "\.(png|jpg|svg)$") {
        set req.backend_hint = image;
    }
}
```

The choice can use arbitrary request data: a URL prefix (`req.url ~ "^/java/"`), the User-Agent (the users guide suggests `req.http.User-agent ~ /mobile/` for mobile devices), or `req.http.host` for virtual hosts, which are never declared explicitly. Without an explicit selection Varnish uses the backend named `default`; if none is named default, the first backend in the VCL.

Host regexes are loose: `req.http.host ~ "foo.com"` matches foo.com, www.foo.com, zoop.foo.com and any host ending in foo.com. For a tighter match use `==`, for example `req.http.host == "foo.com" || req.http.host == "www.foo.com"`.

Unused backends: every defined backend must be used or VCL compilation fails:

```
Unused backend image, defined:
Running VCC-compiler failed, exited with 2
VCL compilation failed
```

Fix by removing the backend or assigning it in VCL. Backends can also be declared `none` (`backend default none;`); all none backends compare equal and a none backend is false in a boolean context. Directors typically return it when no backend is healthy.

Routing by content only offloads the primary backend; the distribution is not predictable. For real load balancing use `vmod_directors` (see the round-robin example below), optionally with health probes.

```vcl
import directors;
sub vcl_init {
    new vdir = directors.round_robin();
    vdir.add_backend(backend1);
    vdir.add_backend(backend2);
}
sub vcl_recv { set req.backend_hint = vdir.backend(); }
```

## Checked

Method: 2026-11-08, read the multiple-backends tutorial and the backend servers users-guide page in full (docs only, nothing run). Dropped the unsupported `unused image;` fix and the VCL-labels pointer. Added the none backend, default-backend rule from the users guide, the exact-match advice and the directors example.
