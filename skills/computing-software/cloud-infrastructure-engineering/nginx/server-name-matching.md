---
id: computing-software.cloud-infrastructure-engineering.nginx.server-name-matching
name: server-name-matching
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, server-name, virtual-host, default-server]
level: practitioner
status: docs-checked
description: "How nginx selects a server block by Host header: exact, leading wildcard, trailing wildcard, regex, then default_server, plus hash table errors."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html", "https://nginx.org/en/docs/http/server_names.html", "https://nginx.org/en/docs/http/request_processing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

nginx tests the `Host` header against `server_name` values. Search order, stopping at the first hit:
1. the exact name;
2. the longest wildcard starting with an asterisk, e.g. `*.example.com`;
3. the longest wildcard ending with an asterisk, e.g. `mail.*`;
4. the first matching regular expression, in file order (written with a leading `~`).

If nothing matches, or `Host` is missing, the request goes to the default server of that listen port. That is the first server defined for the port unless `default_server` is set on `listen`.

```nginx
server { listen 80; server_name example.com .example.org; }   # .example.org = example.org and *.example.org
server { listen 80 default_server; server_name _; return 444; }
```

- The default server is a property of the `listen` port, not of `server_name`.
- The default `server_name` is the empty string, which matches requests without a `Host` header. `return 444` closes the connection.
- `_` is not special: it is an invalid name that never matches a real one.
- Regex names can have captures (`~^(www\.)?(.+)$`, use `$2`) and named captures (`(?<domain>.+)`, use `$domain`).
- Error "could not build the server_names_hash, you should increase server_names_hash_bucket_size: 32": set a larger `server_names_hash_bucket_size` (the page's example uses 64) in `http`. If the message names both `server_names_hash_max_size` and the bucket size, first raise `server_names_hash_max_size` to near the number of names.

## Checked
Date: 2026-11-03.
Confirmed in the core module, server_names and "How nginx processes a request" pages: priority order, default_server rules, empty default name, 444, `_` explanation, captures, hash error text and remedy.
Removed as unconfirmed: "64 or 128" bucket sizes, the SNI wording in the intro, the exposed-internal-vhost remark and the curl verify step.
Method: documentation only; no commands were run.
