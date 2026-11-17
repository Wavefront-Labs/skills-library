---
id: computing-software.cloud-infrastructure-engineering.nginx.try-files-fallback
name: try-files-fallback
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, try-files, spa, fallback]
level: practitioner
status: docs-checked
description: "try_files for static-then-app fallback, single page app routing and named-location handoff, including the last-argument rule."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`try_files file ... uri;` or `try_files file ... =code;` (contexts `server`, `location`) checks files in order and uses the first one found, processing in the current context. File paths are built from `root` and `alias`; a trailing slash (`$uri/`) tests for a directory. If no file is found, the last parameter is used: an internal redirect to that URI, a named location, or a status code (`=404`).

```nginx
location / {
    root /srv/app/dist;
    try_files $uri $uri/ /index.html;
}
location /api/ { try_files $uri @backend; }
location @backend { proxy_pass http://app; }
location /assets/ { try_files $uri =404; }
```

- The `/index.html` fallback answers every path that is not a file, so a mistyped asset URL returns the app page; give asset directories their own location ending in `=404`, as the last block does.
- A named location as last argument hands the request to the application (the docs' Mongrel and Drupal examples work this way); the docs' Mongrel example also lists a maintenance page first: `try_files /system/maintenance.html $uri $uri/index.html $uri.html @mongrel;`.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_core_module page (try_files section): syntax, contexts, ordering, directory test, last-parameter forms, root/alias path construction, named location examples.
Removed as unconfirmed: the autoindex/redirect warning on `$uri/`, the claim about query strings and `$is_args$args`, the comment that `if (!-f ...)` is fragile, and the curl verify step.
Method: documentation only; no commands were run.
