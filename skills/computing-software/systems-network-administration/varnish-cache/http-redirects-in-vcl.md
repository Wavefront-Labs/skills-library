---
id: computing-software.systems-network-administration.varnish-cache.http-redirects-in-vcl
name: http-redirects-in-vcl
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [redirect, synth-301, http-to-https, location-header]
level: practitioner
status: docs-checked
description: "Issue 301/302 redirects from Varnish with synth and vcl_synth, including HTTP to HTTPS, internal path moves and external targets."
sources:
  - https://www.varnish.org/docs/tutorials/redirect/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# http redirects in vcl

Return a synthetic response from a client-side sub and set `Location` in `vcl_synth`.

HTTP to HTTPS:

```vcl
vcl 4.1;
import std;
sub vcl_recv {
    unset req.http.location;
    if (std.port(server.ip) != 443) {
        set req.http.location = "https://" + req.http.host + req.url;
        return (synth(301));
    }
}
sub vcl_synth {
    if (resp.status == 301 || resp.status == 302 ||
        resp.status == 303 || resp.status == 307) {
        if (!req.http.location) {
            std.log("location not specified");
            set resp.status = 503;
            return (deliver);
        }
        set resp.http.location = req.http.location;
        return (deliver);
    }
}
```

Internal move: `return (synth(301, "/another-page"))` and in `vcl_synth` copy `resp.reason` into `resp.http.location`, then set `resp.reason = "Moved"`.

External: pass the full URL as the reason the same way, for example `return (synth(301, "https://external.example.com/"))` for `/external`.

The page notes that origin webservers usually handle redirects with rewrite rules, but Varnish can do it too. Its HTTP-to-HTTPS example tests `std.port(server.ip) != 443`; the page's examples also define a `backend default` and omit `import std;`, which that example needs for `std.port` and `std.log`.

## Checked

Method: 2026-11-08, read the redirect tutorial in full (docs only, nothing run). Dropped the unsupported "listener port" gloss, added the external example, the rewrite-rules note and the missing import caveat. Code is otherwise the page's.
