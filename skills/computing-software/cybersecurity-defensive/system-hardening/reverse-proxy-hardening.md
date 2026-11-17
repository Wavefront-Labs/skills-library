---
id: computing-software.cybersecurity-defensive.system-hardening.reverse-proxy-hardening
name: reverse-proxy-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [reverse-proxy-hardening, nginx, haproxy, envoy, x-forwarded-for, request-smuggling, web-server-hardening]
level: practitioner
status: docs-checked
description: "Harden reverse proxies (nginx, HAProxy, Envoy): trusted forwarded headers, request smuggling defences, header hygiene, size and rate limits, TLS, and admin interfaces."
sources: ["https://nginx.org/en/docs/http/ngx_http_realip_module.html", "https://portswigger.net/web-security/request-smuggling", "https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/", "https://www.envoyproxy.io/docs/envoy/latest/configuration/best_practices/edge", "https://www.envoyproxy.io/docs/envoy/latest/operations/admin", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html", "https://nginx.org/en/docs/http/ngx_http_core_module.html", "https://nginx.org/en/docs/http/ngx_http_limit_req_module.html", "https://nginx.org/en/docs/http/ngx_http_stub_status_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reverse proxy hardening

The reverse proxy is the trust boundary between the internet and your apps. Mistakes here (trusting client
headers, parsing differences) undermine every control behind it.

## Forwarded headers: set, do not trust
- At the edge proxy, **overwrite** `X-Forwarded-For`, `X-Real-IP`, `X-Forwarded-Proto`, `X-Forwarded-Host`
  rather than appending client-supplied values:
  nginx `proxy_set_header X-Forwarded-For $remote_addr;` at the outermost proxy (use
  `$proxy_add_x_forwarded_for` only on inner hops), HAProxy `option forwardfor` (with `http-request del-header
  X-Forwarded-For` first at the edge).
- Inner proxies and apps trust these headers only from known proxy IPs: nginx `set_real_ip_from 10.0.0.0/8;
  real_ip_header X-Forwarded-For; real_ip_recursive on;`. Otherwise IP allowlists and rate limits are bypassable.
- Strip internal headers from client requests (e.g. `X-User-Id`, `X-Internal-Auth`) so clients cannot inject
  identity headers that backends trust.

## Request smuggling and parsing
- Keep proxies and backends patched; prefer HTTP/2 or HTTP/1.1 with keep-alive end to end where both sides
  handle it correctly, or normalise.
- Reject ambiguous requests: both `Content-Length` and `Transfer-Encoding`, duplicate CL headers, obfuscated TE
  (check what your proxy version rejects by default and test it; Envoy's edge guidance sets `headers_with_underscores_action: REJECT_REQUEST`).
- Do not downgrade HTTP/2 to HTTP/1.1 to backends without validation (HTTP/2 downgrade smuggling, see the PortSwigger request smuggling page).

## Header hygiene
- Hide upstream identity: nginx `server_tokens off; proxy_hide_header X-Powered-By;`.
- Add security headers centrally (HSTS, X-Content-Type-Options, frame-ancestors via CSP) where apps do not.
- Normalise or reject path tricks: decide how encoded slashes and double slashes are handled; route matching
  differences between proxy and backend cause ACL bypasses. Envoy's edge guidance enables `normalize_path` and
  `merge_slashes` and sets `path_with_escaped_slashes_action`.

## Limits
`client_max_body_size`, header size limits, timeouts (`client_body_timeout`, `proxy_read_timeout`), connection
and request rate limits (`limit_req_zone`), slowloris protection; HAProxy `timeout http-request`, stick tables.

## TLS
TLS 1.2/1.3 only, modern ciphers, HSTS; re-encrypt to backends across untrusted networks with
certificate verification (`proxy_ssl_verify on`).

## Admin and status endpoints
nginx `stub_status`, HAProxy stats page, Envoy admin interface (its endpoints include `POST /quitquitquit`;
the Envoy docs' example binds it to port 9901): bind to localhost or a management network and restrict access.

## Verify
A request with a forged `X-Forwarded-For: 127.0.0.1` is logged with the real client IP at the app; a request
with both CL and TE is rejected; admin/status endpoints are unreachable externally.

## Checked
2026-10-31. Confirmed: nginx `set_real_ip_from`, `real_ip_header`, `real_ip_recursive`, `$proxy_add_x_forwarded_for` (appends `$remote_addr`), `proxy_set_header`, `proxy_hide_header`, `proxy_read_timeout`, `proxy_ssl_verify`, `client_max_body_size`, `client_body_timeout`, `server_tokens`, `limit_req_zone`, `stub_status`; HAProxy `option forwardfor`, `http-request del-header`, `timeout http-request`, stick tables; Envoy edge best practices (`use_remote_address`, `normalize_path`, `merge_slashes`, underscore header rejection, admin restriction) and admin `POST /quitquitquit`; PortSwigger on Content-Length versus Transfer-Encoding disagreement, obfuscated TE and HTTP downgrading. Removed: Traefik, the TLS grade check, specific path-bypass examples, and an unsourced claim about default rejection.
Method: documentation only; no commands were run.
