---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.nginx-config-snippets
name: nginx-config-snippets
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, nginx-config, configuration-snippet, config-yaml, nginx-conf]
level: advanced
status: docs-checked
description: "Inject custom NGINX directives into APISIX via nginx_config snippet keys in config.yaml (main, http, http_server, http_admin, http_end, stream) and avoid indentation errors."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/customize-nginx-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NGINX configuration snippets

Overrides live under `nginx_config` in `conf/config.yaml`. Defaults are in `conf/config.default.example`; the generated file is `conf/nginx.conf`, created by `./bin/apisix start`.

Snippet keys and the page's examples:
- `main_configuration_snippet`: adds `daemon on;`.
- `http_configuration_snippet`: adds a `server` block on port 45651 with a `/ysec_status` location, plus `chunked_transfer_encoding on;`.
- `http_server_configuration_snippet`: `set $my "var";`.
- `http_admin_configuration_snippet`: a `log_format admin` entry.
- `http_end_configuration_snippet`: `server_names_hash_bucket_size 128;`.
- `stream_configuration_snippet`: `tcp_nodelay off;`.

Indent the sub-entries correctly under `nginx_config`; wrong indentation can stop `./bin/apisix start` from generating `conf/nginx.conf`.

## Checked

2026-11-04: read the Customize Nginx Configuration page; the nginx_config location, config.default.example, conf/nginx.conf generation, all six snippet keys with their example contents and the indentation warning match. Removed a meta line about what the page does not cover.

Method: documentation only; no commands were run.
