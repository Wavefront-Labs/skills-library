---
id: computing-software.networking-hardware-and-wireless.envoy.edge-proxy-best-practices
name: edge-proxy-best-practices
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, edge-proxy, best-practices, buffer-limits, normalize-path, merge-slashes, headers-with-underscores-action, hardening]
level: practitioner
status: docs-checked
description: "Harden Envoy as an edge proxy: admin lockdown, overload manager, 32 KiB buffers, HTTP/2 limits, timeouts and path normalisation."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/best_practices/edge.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# edge proxy best practices
Envoy defaults suit the service mesh case; an edge proxy must tighten several. For TCP proxies: restrict the admin endpoint, configure the overload manager, and set listener and cluster per-connection buffer limits to 32 KiB. For HTTP additionally:
- `use_remote_address: true` so client-supplied headers are not trusted (see header sanitizing);
- connection and stream timeouts;
- HTTP/2 and HTTP/3 max concurrent streams to 100, HTTP/2 initial stream window 64 KiB and initial connection window 1 MiB;
- `headers_with_underscores_action: REJECT_REQUEST` so upstreams that treat `_` and `-` alike are not tricked;
- listener connection limits and global downstream connection limits.

If you use RBAC or path-based routing, also set `normalize_path` and `merge_slashes`, and choose `path_with_escaped_slashes_action`:

```yaml
normalize_path: true
merge_slashes: true
path_with_escaped_slashes_action: UNESCAPE_AND_REDIRECT
```
Use `REJECT_REQUEST` when clients are RFC 3986 normalised (gRPC), `UNESCAPE_AND_REDIRECT` for browsers (forces a re-issued request), and `KEEP_UNCHANGED` only for servers that need encoded slashes.

`UNESCAPE_AND_FORWARD` suits servers known to treat escaped and unescaped slashes equivalently, but can raise the path confusion risk if intermediaries do path-based access control.

Gotcha: without normalisation, parties that use different path representations (path confusion) can dodge a prefix RBAC or route match.

## Checked

2026-11-03. Confirmed against: edge.rst best-practices page (all listed settings, 32 KiB, 100 streams, 64 KiB, 1 MiB, path action recommendations). Removed or corrected: the curl --path-as-is verify step and the specific example paths.

Method: documentation only; no commands were run.
