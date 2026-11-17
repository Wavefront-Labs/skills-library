---
id: computing-software.systems-network-administration.varnish-cache.xkey-tag-purging
name: xkey-tag-purging
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [xkey, surrogate-keys, soft-purge, tag-based-purge]
level: advanced
status: docs-checked
description: "Purge groups of objects by tag with vmod_xkey: keys from an xkey response header, xkey.purge and xkey.softpurge, a PURGE handler, and the Varnish Enterprise ykey variant."
sources:
  - https://www.varnish.org/docs/tutorials/cache-invalidation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# xkey tag purging

vmod_xkey adds tags (secondary keys) to cached objects, allowing fast purging of every object matching a tag. The origin lists keys in an `xkey` response header, space separated; values are arbitrary and can identify or segment objects:

```
HTTP/1.1 200 OK
Server: Apache
xkey: 8155054 166412 234323
```

A hard purge removes matching objects from the cache immediately. A soft purge expires them but keeps them for their configured grace (stale delivery while the next fetch runs) and keep (conditional fetches).

```vcl
vcl 4.1;
import xkey;
acl purgers { "203.0.113.0"/24; }

sub vcl_recv {
    if (req.method == "PURGE") {
        if (client.ip !~ purgers) { return (synth(403, "Forbidden")); }
        if (req.http.xkey) {
            set req.http.n-gone = xkey.purge(req.http.xkey);
            # or: set req.http.n-gone = xkey.softpurge(req.http.xkey)
            return (synth(200, "Invalidated " + req.http.n-gone + " objects"));
        } else {
            return (purge);
        }
    }
}
```

Request: `curl -X PURGE -H "xkey: purging_key" "http://example.com/"` purges every object matching that key.

Where each method works (from the page's table): plain purge targets one object with its Vary variants (VCL yes, CLI no); ban targets regex patterns (VCL and CLI); xkey and ykey target keys (VCL only, not CLI). Broadcaster and Controller (commercial Varnish Software products) support all four. A plain purge requires the same hash as the cached object, has no regex, and evicts regardless of backend availability.

Ykey: the page describes vmod_ykey (it mistakenly writes xkey in that sentence) as the Varnish Enterprise, commercial equivalent, with a configurable header name, arbitrary keys defined in VCL, a choice of key separator, namespaces, and persistence of key data with the MSE stevedore. Keys are added in `vcl_backend_response` with `ykey.add_header(beresp.http.Ykey)` and `ykey.add_key("IMAGE")`; purge with `ykey.purge_header(req.http.Ykey-Purge)` (add `soft=true` for soft purge).

## Checked

Method: 2026-11-08 docs-only read of the cache-invalidation tutorial. Replaced the earlier "VCL supports purge, ban, xkey and ykey; CLI bans only" shorthand with the page's table. Dropped the earlier example's "localhost" ACL entry, which came from the purge example, not the xkey one. The page's ykey example references an ACL name that does not match its declaration; check yours.
