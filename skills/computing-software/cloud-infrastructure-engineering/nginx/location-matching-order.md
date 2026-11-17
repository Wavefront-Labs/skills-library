---
id: computing-software.cloud-infrastructure-engineering.nginx.location-matching-order
name: location-matching-order
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, location-matching, location, regex, prefix]
level: practitioner
status: docs-checked
description: "How nginx picks a location block: exact match, longest prefix, ^~, regular expressions in file order, then predicate locations."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`location [ = | ~ | ~* | ^~ ] uri { ... }`, `location $variable { ... }` (predicate, 1.31.5) and `location @name { ... }` (contexts `server`, `location`). Matching runs against the normalized URI: `%XX` decoded, `.` and `..` resolved, adjacent slashes merged.

Search order:

1. Prefix locations are checked and the one with the longest matching prefix is selected and remembered.
2. If that prefix has `^~`, regular expressions and predicate locations are skipped.
3. Otherwise regular expressions (`~` case-sensitive, `~*` case-insensitive) are checked in order of appearance in the file; the first match wins.
4. If none matches, predicate locations are checked in order of appearance.
5. If none matches, the remembered prefix location is used.

An `=` modifier defines an exact match; if found, the search ends (and such a location cannot contain nested locations).

Documented example:

```nginx
location = /            { }   # A
location /              { }   # B
location /documents/    { }   # C
location ^~ /images/    { }   # D
location ~* \.(gif|jpg|jpeg)$ { }   # E
location $arg_pred      { }   # F
```

`/` matches A, `/index.html` matches B, `/documents/document.html` matches C, `/images/1.gif` matches D, `/documents/1.jpg` matches E, and `/documents/index.html?pred=1` matches F.

- A predicate location matches when its variable is not empty and not `0`.
- `@name` locations are not used for normal matching, only for redirection, and cannot be nested.
- For a prefix location ending in `/` that is handled by `proxy_pass`, `fastcgi_pass`, `uwsgi_pass`, `scgi_pass`, `memcached_pass` or `grpc_pass`, a request for the same URI without the trailing slash gets a `301` to the URI with the slash. Define `location = /user { ... }` to avoid that.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_core_module` page (`location` section and its example). Removed: the invented example blocks, the "regex hijacks /api/" scenario, and the add_header/curl Verify step. The predicate location version (1.31.5) is stated from the page.
Method: documentation only; no commands were run.
