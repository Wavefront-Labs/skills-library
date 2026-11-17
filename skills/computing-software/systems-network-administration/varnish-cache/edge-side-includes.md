---
id: computing-software.systems-network-administration.varnish-cache.edge-side-includes
name: edge-side-includes
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [esi, do-esi, esi-include, esi-fragments]
level: practitioner
status: docs-checked
description: "Assemble pages from separately cached fragments with ESI: esi:include, esi:remove, <!--esi -->, beresp.do_esi, and fragment failure handling."
sources:
  - https://www.varnish.org/docs/users-guide/esi/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# edge side includes

Varnish implements a subset: `esi:include`, `esi:remove` and `<!--esi ... -->`. Variable and cookie substitution is not implemented, and ESI inside HTML comments is not processed.

Enable it for the parent only:

```vcl
sub vcl_backend_response {
    if (bereq.url == "/test.html") {
        set beresp.do_esi = true;
        set beresp.ttl = 24h;
    } elseif (bereq.url == "/cgi-bin/date.cgi") {
        set beresp.ttl = 1m;
    }
}
```

Fragments have their own TTLs. Set `do_esi` on a fragment only if it contains includes itself. `max_esi_depth` defaults to 5.

Parent markup:

```html
<esi:include src="/cgi-bin/date.cgi"/>
```

Use `esi:remove` for content to show only when ESI is not processed, and `<!--esi ... -->` for content to show only when it is.

Failure: fragments must return status 200 or 204 or their delivery fails; failure does not abort the parent by default. Synthetic fragments from `vcl_synth` or `vcl_backend_error` must set status 200.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: nothing needed removing.

Method: documentation only; no commands were run.
