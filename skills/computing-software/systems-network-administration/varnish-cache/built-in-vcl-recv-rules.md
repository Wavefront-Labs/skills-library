---
id: computing-software.systems-network-administration.varnish-cache.built-in-vcl-recv-rules
name: built-in-vcl-recv-rules
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [builtin-vcl, vcl-recv, uncacheable-methods, cookie-bypass]
level: practitioner
status: docs-checked
description: "Know what the built-in vcl_recv does: PRI 405, Host required, unknown methods, only GET and HEAD cached, and Authorization or Cookie forcing a pass."
sources:
  - https://www.varnish.org/docs/tutorials/varnish-builtin-vcl/
  - https://www.varnish.org/docs/users-guide/vcl-built-in-code/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# built in vcl recv rules

Your VCL runs first, then the built-in code is appended. Skipping it with an early `return` removes the safe defaults. Print it with `varnishd -x builtin`.

Built-in `vcl_recv`:
1. Method `PRI` returns `synth(405)`.
2. A top-level HTTP/1.1 request without `Host` returns `synth(400)`.
3. A method other than GET, HEAD, PUT, POST, TRACE, OPTIONS, DELETE, PATCH was piped. As of Varnish 8.0 unknown methods get a synthetic 501 instead; re-enable pipe in `sub vcl_req_method { if (req.method == "CUSTOM") { return (pipe); } }`.
4. A method other than GET or HEAD returns `pass`.
5. `Authorization` or `Cookie` present returns `pass`; this lives in the `vcl_req_cookie` sub.
6. Otherwise `return (hash)`.

`vcl_pipe` sets `Connection: close` on piped requests. `vcl_pass` and `vcl_miss` return `fetch`. `vcl_purge` returns `synth(200, "Purged")`. `vcl_deliver` returns `deliver`.

To cache despite cookies, override just that sub:

```vcl
sub vcl_req_cookie { return; }
```

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: nothing needed removing.

Method: documentation only; no commands were run.
