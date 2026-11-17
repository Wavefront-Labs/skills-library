---
id: computing-software.systems-network-administration.varnish-cache.bypass-cache-pass-and-pipe
name: bypass-cache-pass-and-pipe
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [return-pass, return-pipe, bypass-cache, websocket-pipe]
level: practitioner
status: docs-checked
description: "Bypass the cache for specific URLs with return(pass), and reserve return(pipe) for non-HTTP uses such as WebSocket upgrades."
sources:
  - https://www.varnish.org/docs/tutorials/bypass-cache-urls/
  - https://www.varnish.org/docs/reference/vcl-step/
  - https://www.varnish.org/docs/tutorials/varnish-builtin-vcl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# bypass cache pass and pipe

Bypass the cache with `return (pass)` in `vcl_recv` when the request information tells you the response is not cacheable, typically by URL:

```vcl
vcl 4.1;
sub vcl_recv {
    if (req.url ~ "^/admin($|/.*)") { return (pass); }
}
```

`pass` switches to pass mode: the request does not use the cache and its response is not put into it. Control goes to `vcl_pass`, whose `return (fetch)` starts the backend request. Subsequent requests on the same client connection are handled normally.

`pipe` switches to pipe mode (`vcl_pipe`). Varnish degrades into a simple TCP proxy shuffling bytes both ways until either end closes the connection; no other VCL subroutine is called after `vcl_pipe`. All notion of HTTP is lost, so use pipe only when the request cannot be identified as HTTP, such as a WebSocket established by a `Connection: Upgrade` header:

```vcl
sub vcl_recv {
    if (req.http.upgrade == "websocket") { return (pipe); }
}
```

The built-in VCL notes that piping means you cannot manipulate the transaction later and your logs are blind to the backend response, so prefer pass for HTTP requests. By default `Connection: close` is set on all piped requests to stop connection reuse sending later requests to the wrong backend; `unset bereq.http.connection` in `vcl_pipe` undoes it.

Built-in `vcl_recv` pipes request methods outside GET, HEAD, PUT, POST, TRACE, OPTIONS, DELETE and PATCH, passes other non-GET/HEAD methods, and passes any request with an Authorization or Cookie header.

## Checked

Method: 2026-11-08, read the bypass-cache-urls tutorial, the vcl-step reference and the built-in VCL tutorial in full (docs only, nothing run). Dropped the pipe_timeout (60s) claim and the BAN/PURGE aside, which none of the pages state. Added the pipe/pass semantics from vcl-step and the built-in VCL's Connection: close, method lists and logging caveat.
