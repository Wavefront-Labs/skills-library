---
id: computing-software.systems-network-administration.varnish-cache.vcl-labels-and-separate-vcls
name: vcl-labels-and-separate-vcls
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vcl-label, return-vcl, virtual-hosts, multiple-vcl]
level: advanced
status: docs-checked
description: "Split vhosts into separate VCL files, point vcl.label names at them, branch from the active VCL with return(vcl(label)), and update one without reloading the top level."
sources:
  - https://www.varnish.org/docs/users-guide/vcl-separate/
  - https://www.varnish.org/docs/reference/varnish-cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vcl labels and separate vcls

From Varnish 5.0, separate VCL files can serve separate vhosts or any distinct subset of requests. Each is a normal VCL file, as if it ran that domain alone. These are varnishadm CLI commands:

```
vcl.load vo_1 /path/vo.vcl
vcl.load vc_1 /path/vc.vcl
vcl.label l_vo vo_1
vcl.label l_vc vc_1
```

Top-level VCL branching on Host (it must have a backend even if unused):

```vcl
import std;
backend default { .host = "127.0.0.1"; }
sub vcl_recv {
    set req.http.host = std.tolower(req.http.host);
    if (req.http.host ~ "\.?varnish\.org$")       { return (vcl(l_vo)); }
    if (req.http.host ~ "\.?varnish-cache\.org$") { return (vcl(l_vc)); }
    return (synth(302, "http://varnish-cache.org"));
}
sub vcl_synth {
    if (resp.status == 301 || resp.status == 302) {
        set resp.http.location = resp.reason;
        set resp.reason = "Moved";
        return (deliver);
    }
}
```

Then `vcl.load top_1 /path/top.vcl` and `vcl.use top_1`. To update a site, load a new file and move its label: `vcl.load vo_2 ...` then `vcl.label l_vo vo_2`. To change the top level, load a new one and `vcl.use` it as usual.

Rules:

- All requests start in the active VCL (the one from `vcl.use`).
- Only labels may be used in `return(vcl(name))`; otherwise the top level would need reloading whenever a separate VCL changed.
- You can switch VCLs only from the active VCL; trying from a separate one gives a 503.
- You cannot remove (`vcl.discard`) a label if any VCL contains `return(vcl(that_label))`, nor a VCL that has a label attached.
- The VCL step reference adds that `return(vcl(label))` is valid only while `req.restarts` is zero and only from the active VCL, and that it rolls the request back as if `std.rollback(req)` ran.
- The page calls this a new feature that may change, tested as testcase c00077.

## Checked

Method: 2026-11-08 docs-only read of the separate-VCL guide; the rest of the CLI reference was not read in full. The `req.restarts` rule comes from the VCL steps page (read), not the cited CLI page; the earlier wording attributing it to the guide is corrected here. Other claims match.
