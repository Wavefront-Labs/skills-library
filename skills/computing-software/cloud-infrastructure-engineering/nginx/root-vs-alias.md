---
id: computing-software.cloud-infrastructure-engineering.nginx.root-vs-alias
name: root-vs-alias
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, root-alias, root, alias, static-files]
level: practitioner
status: docs-checked
description: "Difference between root and alias in nginx, when to prefer root, and alias inside regex locations."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`root` appends the request URI to its path; `alias` replaces the matched location part with its path.

```nginx
location /i/ { root  /data/w3; }         # /i/top.gif -> /data/w3/i/top.gif
location /i/ { alias /data/w3/images/; } # /i/top.gif -> /data/w3/images/top.gif
```

- When the location matches the last part of the `alias` value (`location /images/ { alias /data/w3/images/; }`), the docs say to use `root` instead (`root /data/w3;`).
- `root` defaults to `html`.
- In a location defined by a regular expression, `alias` gives the complete file path and should normally refer to the captures:

```nginx
location ~ ^/users/(.+\.(?:gif|jpe?g|png))$ {
    alias /data/w3/images/$1;
}
```

- The `alias` path can contain variables except `$document_root` and `$realpath_root`.
- `try_files` builds each file path from `root` and `alias`.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_core_module page: root/alias examples and semantics, use-root advice, regex alias, variable exceptions, root default, try_files path construction.
Removed as unconfirmed: the `/files../secret` traversal walkthrough and trailing-slash rules, the alias plus try_files quirks note, and the curl/error-log verify step. Check slash consistency between `location` and `alias` yourself when editing.
Method: documentation only; no commands were run.
