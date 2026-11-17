---
id: computing-software.systems-network-administration.varnish-cache.device-detection
name: device-detection
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [device-detection, user-agent, x-ua-device, vary-header]
level: practitioner
status: docs-checked
description: "Serve device-specific content: classify User-Agent into X-UA-Device, then Vary, route to another backend or redirect, keeping one cached object per URL per device class."
sources:
  - https://www.varnish.org/docs/users-guide/devicedetection/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# device detection

Device detection picks content from the User-Agent, for example size-reduced files for mobile clients or a video codec the client understands. Strategies: redirect to another URL, use a different backend, or change the backend request so the backend sends tailored content. The guide assumes `req.http.X-UA-Device` is present and unique per client class. It can be as simple as a regex test on `req.http.User-Agent` (e.g. `(?i)iphone` setting `mobile-iphone`). A basic community regex set lives in the varnishcache/varnish-devicedetect repository on GitHub; include `devicedetect.vcl` and call it.

Same URL, different content, requires:

1. Detect the client.
2. Signal the class to the backend (set or change a header, or change the backend request URL).
3. Add any missing `Vary` header to the backend response so Varnish's own Vary handling applies.
4. Alter what clients see so caches outside your control do not serve wrong content.

Throughout, keep one cached object per URL per device class.

Example 1, header to backend: Varnish copies `req.http.X-UA-Device` into the backend request. In `vcl_backend_response`, if `bereq.http.X-UA-Device` is set, set `Vary` to `X-UA-Device` when absent, or append `, X-UA-Device` when it is not already listed (remove `Vary: User-Agent` if your backend sets it). In `vcl_deliver`, rewrite the outgoing Vary with `regsub(resp.http.Vary, "X-UA-Device", "User-Agent")` so downstream caches vary on the real header. Optionally copy the class into `beresp.http.X-UA-Device`; the page says to comment that out if you do not want the client to see your classification.

Example 2, normalize User-Agent: in `vcl_miss` and `vcl_pass`, set `req.http.User-Agent = req.http.X-UA-Device` so the backend sees e.g. `mobile-android`. Only suitable if the backend does not need the original header (the page cites CGI scripts with few headers). Same Vary handling as above.

Example 3, query parameter: as a last resort append `devicetype=<class>` to the URL for GET requests in `vcl_miss` and `vcl_pass` (after `vcl_hash`, so all variants can be purged in one go without banning). The client does not see it. Strip `[?&]devicetype=.*$` from the Location header on 301/302/303 backend responses.

Different backend: set `req.backend_hint` when `req.http.X-UA-Device` matches `^mobile` or `^tablet`, and `hash_data(req.http.X-UA-Device)` in `vcl_hash`.

Redirect: `return(synth(750, "Moved Temporarily"))` in `vcl_recv` for those classes; in `vcl_synth` set the Location header to an m. host plus `req.url`, set status 302 and deliver. (The page uses `obj.*` in `vcl_synth`; in Varnish 4 and later the synthetic object is `resp.*`, which is outside what the page states.)

## Checked

Method: 2026-11-08 docs-only read of the cited guide. Rewrote the thin earlier summary to cover all examples on the page. The removed claim that Vary is the only step was replaced by the four listed steps. The page's example `if` in the first snippet lacks a closing parenthesis; do not copy it verbatim.
