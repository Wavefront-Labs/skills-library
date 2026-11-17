---
id: computing-software.systems-network-administration.varnish-cache.vary-and-request-normalization
name: vary-and-request-normalization
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vary-header, normalize-host, querysort, cache-variants]
level: practitioner
status: docs-checked
description: "Raise hit rate by normalising requests: Vary-based variants, one canonical Host, std.querysort, and tracking-parameter removal."
sources:
  - https://www.varnish.org/docs/users-guide/increasing-your-hitrate/
  - https://www.varnish.org/docs/tutorials/configuring-varnish-wordpress/
  - https://www.varnish.org/docs/reference/vmod_std/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vary and request normalization

A `Vary: Accept-Language` response makes Varnish store one variant per distinct request header value, and the values must match exactly: a missing space or a different case creates another copy. Normalise the headers a backend varies on, for example map `Accept-Language` to a few known values (the guide shows `en`, `de`, `fr` and removes the header otherwise). `Vary: User-Agent` is a pitfall: every browser and patch level has a different value, so normalise it or hit rate suffers badly. Varnish returns a 503 when it cannot parse `Vary`, or when a listed client header exceeds 65k characters.

Collapse equivalent hosts (the Varnish guide's example, shown here with a placeholder domain):

```vcl
if (req.http.host ~ "(?i)^(www\.)?example\.com") {
    set req.http.host = "example.com";
}
```

Other normalisations from the WordPress guide:

```vcl
import std;
sub vcl_recv {
    set req.url = regsub(req.url, "\?$", "");              # empty query string
    set req.http.Host = regsub(req.http.Host, ":[0-9]+", ""); # port in Host
    set req.url = std.querysort(req.url);                    # stable parameter order
    unset req.http.proxy;                                    # httpoxy
}
```

Remove tracking parameters (such as `gclid`, `fbclid`, `utm_*`) with `regsuball` on `req.url` when the URL matches them, then strip a trailing `?`, `|` or `&` with `regsub`; the WordPress guide lists many parameter names in one alternation.

## Checked
2026-11-08: Read in full the Varnish "Achieving a high hitrate" page. Read only the `vcl_recv` normalisation block of the WordPress guide and the `std.querysort` entry of the vmod_std reference; the rest of those two pages was not read. Confirmed: Vary variants must match exactly, Accept-Language and User-Agent normalisation, Vary parse-error 503 and 65k limit, host collapsing, empty query string, port removal, `std.querysort`, `unset req.http.proxy` (httpoxy), tracking-parameter removal. Removed: `Vary: *` never cached, the `vary_notice` parameter with its default of 10, and the `http_gzip_support`/Accept-Encoding claim (none appear on the cited pages). The first example now escapes the dots in the host regex (the guide's version leaves them unescaped).
Method: documentation only; no commands were run.
