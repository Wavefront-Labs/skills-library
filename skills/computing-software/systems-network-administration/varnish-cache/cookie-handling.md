---
id: computing-software.systems-network-administration.varnish-cache.cookie-handling
name: cookie-handling
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [cookies, vmod-cookie, strip-cookies, set-cookie]
level: practitioner
status: docs-checked
description: "Make cookied traffic cacheable: drop client cookies by URL, keep only named cookies with vmod_cookie or regsub, and unset unwanted backend Set-Cookie headers."
sources:
  - https://www.varnish.org/docs/users-guide/increasing-your-hitrate/
  - https://www.varnish.org/docs/reference/vmod_cookie/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cookie handling

By default Varnish does not cache an object from the backend with a `Set-Cookie` header (a hit-for-miss object is created), and a client `Cookie` header makes it bypass the cache. This can be overly conservative: for example Google Analytics cookies are used by client-side JavaScript and are of no interest to the server. An `Authorization` header also makes Varnish pass the request; unset it if that is not wanted.

Client cookies: ignore them everywhere except a special area.

```vcl
if (!(req.url ~ "^/admin/")) { unset req.http.Cookie; }
```

Keep only chosen cookies with vmod_cookie (parse into internal storage, filter, write back):

```vcl
import cookie;
sub vcl_recv {
    if (req.http.cookie) {
        cookie.parse(req.http.cookie);
        # delete chosen ones with cookie.delete("cookie2"), or keep a few:
        cookie.keep("SESSIONID,PHPSESSID");
        set req.http.cookie = cookie.get_string();
        # if empty, unset so the builtin VCL can consider it for caching
        if (req.http.cookie == "") { unset req.http.cookie; }
    }
}
```

Other functions: `filter` (delete a comma-separated list), `keep_re` / `filter_re` (regex), `get`, `get_re`, `isset`, `set`, `clean`, `format_date`. `get` returns NULL for a missing cookie (an empty string when assigned to a header); the module docs say `isset` is often a better presence check. Parsed state lives only for the current request or backend request; pass values to the backend request in fake bereq headers.

Without the VMOD the page uses regular expressions, for example dropping `has_js` and underscore-prefixed cookies, then a leading `;`:

```vcl
set req.http.Cookie = regsuball(req.http.Cookie, "(^|;\s*)(_[_a-z]+|has_js)=[^;]*", "");
set req.http.Cookie = regsub(req.http.Cookie, "^;\s*", "");
```

Cookies from the backend: if it sets unwanted cookies, unset the `Set-Cookie` header (`unset beresp.http.Set-Cookie` in `vcl_backend_response`).

## Checked

Method: 2026-11-08, read the increasing-your-hitrate page and the vmod_cookie reference in full (docs only, nothing run). Added the Authorization note, NULL-versus-isset guidance, state lifetime and the page's regsuball example; function list now matches the reference. Core snippets were unchanged.
