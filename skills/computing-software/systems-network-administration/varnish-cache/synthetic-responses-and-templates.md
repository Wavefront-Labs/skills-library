---
id: computing-software.systems-network-administration.varnish-cache.synthetic-responses-and-templates
name: synthetic-responses-and-templates
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [synthetic-response, vcl-synth, guru-meditation, template-file]
level: practitioner
status: docs-checked
description: "Generate responses in VCL with synth, override the vcl_synth and vcl_backend_error output templates, and load the template from a file with std.fileread."
sources:
  - https://www.varnish.org/docs/tutorials/vcl-synthetic-output-template-file/
  - https://www.varnish.org/docs/reference/vcl-step/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# synthetic responses and templates

Synthetic responses are not from the origin. `return (synth(status, reason))` (client side) goes to `vcl_synth` with `resp.status` and `resp.reason` preset. `vcl_backend_error` is called automatically when the backend fetch fails or `max_retries` is exceeded; it uses `beresp.*` and `bereq.xid` because `resp` is not available in the backend context.

The built-in templates set `Content-Type: text/html; charset=utf-8` and `Retry-After: 5`, and print the status and reason, a "Guru Meditation" heading and the XID (`req.xid`, or `bereq.xid` in the backend version), then end with `return (deliver)`.

Override with your own body (any content type: HTML, XML, JSON, plain text):

```vcl
sub vcl_synth {
    set resp.http.Content-Type = "text/plain; charset=utf-8";
    set resp.body = resp.reason + "(" + resp.status + ")";
    return (deliver);
}
sub vcl_backend_error {
    set beresp.http.Content-Type = "text/plain; charset=utf-8";
    set beresp.body = beresp.reason + "(" + beresp.status + ")";
    return (deliver);
}
```

Always `return (deliver)`; otherwise the built-in output is appended to yours. In `vcl_synth`, `return (deliver)` delivers directly without calling `vcl_deliver`. The reference page says a synthetic body may also be built with `synthetic()`.

Template from a file: `std.fileread()` (std VMOD) returns the file as a string; inject the reason with `regsuball()` on a placeholder:

```vcl
import std;
sub vcl_synth {
    set resp.http.Content-Type = "text/html; charset=utf-8";
    set resp.http.Retry-After = "5";
    set resp.body = regsuball(std.fileread("/etc/varnish/synth.html"), "<<REASON>>", resp.reason);
    return (deliver);
}
```

Use `beresp.reason` and `beresp.*` in the `vcl_backend_error` twin. The HTML file contains the `<<REASON>>` placeholder. Several template files can be loaded for different kinds of output.

Caching: a `vcl_synth` object never enters the cache, but a `vcl_backend_error` object delivered with `beresp.uncacheable == false` becomes a cached synthetic object, so keep private information out of it or set `beresp.uncacheable = true` there.

## Checked

Method: 2026-11-08 docs-only read of both cited pages. Removed unsupported earlier claims: "synthetic(STRING) is identical to setting resp.body", "synthetic ESI fragments need status 200" and the advice to escape user input. Added the return(deliver) warning and the caching caution.
