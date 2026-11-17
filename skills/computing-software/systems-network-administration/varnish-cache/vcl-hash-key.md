---
id: computing-software.systems-network-administration.varnish-cache.vcl-hash-key
name: vcl-hash-key
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vcl-hash, hash-data, cache-key, cache-variants]
level: practitioner
status: docs-checked
description: "Customise the cache key in vcl_hash with hash_data: default URL plus Host or server IP, no case folding, and why returning lookup yourself drops the built-in parts."
sources:
  - https://www.varnish.org/docs/users-guide/vcl-hashing/
  - https://www.varnish.org/docs/tutorials/varnish-builtin-vcl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vcl hash key

The cache key is built in `vcl_hash` with `hash_data()`. By default an object is identified by the request URL and the Host header, or the server IP if there is no Host header (unlikely, per the built-in VCL tutorial):

```vcl
sub vcl_hash {
    hash_data(req.url);
    if (req.http.host) { hash_data(req.http.host); }
    else { hash_data(server.ip); }
    return (lookup);
}
```

After the hash is composed, `return (lookup)` does the cache lookup: a hit goes to `vcl_hit`, a miss to `vcl_miss`.

Varnish does not lowercase the hostname or URL, so "Varnish.org/" and "varnish.org/" would in theory be different entries, though browsers tend to lowercase hostnames.

Adding inputs, e.g. serving pages by country: set a header in `vcl_recv` (the guide uses a geoip VMOD lookup on `client.ip`) and hash it:

```vcl
sub vcl_hash {
    hash_data(req.http.X-Country-Code);
}
```

Without a `return` here, the built-in VCL still adds the URL and Host (or server IP). If you add `return (lookup);` yourself, only the country code matters and Varnish returns seemingly random objects, ignoring the URL (though always with the right country code). Do not return unless you replicate everything.

The URL contains no scheme, so by default there is no HTTPS awareness (see the redirect-loop skill for varying on X-Forwarded-Proto).

## Checked

Method: 2026-11-08 docs-only read of the hashing guide; the vcl_hash, vcl_purge and return(lookup) parts of the built-in VCL tutorial were checked by search rather than read in full. Removed the earlier claim that a purge request must hash like the cached GET (neither page says so); other claims match.
