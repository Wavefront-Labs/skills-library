---
id: computing-software.systems-network-administration.varnish-cache.ban-expressions
name: ban-expressions
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [ban, ban-expression, ban-list, regex-invalidation]
level: practitioner
status: docs-checked
description: "Invalidate groups of objects with bans: expression syntax and fields, varnishadm ban and ban.list, the VCL ban function, std.ban_error and shell quoting."
sources:
  - https://www.varnish.org/docs/tutorials/ban/
  - https://www.varnish.org/docs/users-guide/purging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ban expressions

A ban is expression-based invalidation. Adding a ban puts its expression on the ban list; objects are evaluated against it when hit, before delivery, and a banned object is marked expired so fresh content is fetched. A ban works only on objects already cached and does not stop new content entering. An object is only checked against bans newer than the last one it saw.

Format: `<field> <operator> <arg> [&& <field> <oper> <arg> ...]`. Fields: `req.url`, `req.http.*`, `obj.status`, `obj.http.*`. Operators: `==`, `!=`, `~`, `!~`. Only logical AND is available; for OR add several bans. Arguments are not delimited by double quotes or long-string braces.

Examples from the tutorial: `req.url == / && req.http.host == example.com` (ban equivalent of a purge), `obj.status == 404`, `obj.http.Content-Type ~ ^image/`, `req.url ~ ^/products(/.+|$) && req.http.host == example.com`.

```bash
varnishadm ban obj.status == 404
varnishadm ban "obj.http.Content-Type ~ ^image/"
varnishadm ban req.http.host == example.com '&&' req.url '~' '\\.png$'
varnishadm ban.list
```

Shell characters can break unquoted expressions (the tutorial shows error code 106, "expected conditional"), so quote them. In the users-guide example the backslash is doubled because the Varnish CLI requires it.

From VCL, the page shows `std.ban()` returning a boolean, with `std.ban_error()` for the failure message:

```vcl
import std;
sub vcl_recv {
    if (req.method == "BAN") {
        # check an ACL first
        if (std.ban("req.http.host == " + req.http.host + " && req.url == " + req.url)) {
            return (synth(200, "Ban added"));
        } else {
            return (synth(400, std.ban_error()));
        }
    }
}
```

The VCL must explicitly handle the BAN method; otherwise the built-in VCL pipes it to the backend, and a backend 200 is no confirmation.

Ban list: `varnishadm ban.list` shows timestamp, a count of referencing objects and a flag (C = completed; the users guide also mentions G = Gone). There is always one entry, even on a fresh start. Bans are not immediate removals; they are added and evaluated lazily or by the ban lurker. `req.*` bans are only evaluated by request threads; `obj.*` bans can also be processed by the lurker (see ban-lurker-friendly-bans). `ban_any_variant` limits how many possibly non-matching variants are tested against the ban list during lookup.

## Checked

Method: 2026-11-08, read both cited Varnish pages in full (docs only, nothing run). Corrected the shell-quoting example and the "std.ban_error" claim wording to what the users guide shows; added ban-list semantics and the pipe warning; the field and operator lists were unchanged.
