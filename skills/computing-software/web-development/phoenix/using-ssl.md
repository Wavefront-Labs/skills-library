---
id: computing-software.web-development.phoenix.using-ssl
name: using-ssl
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, https, forcessl, hsts, ssl, tls, endpoint, mix-phx-gen-cert]
level: advanced
status: docs-checked
description: "Serve Phoenix over HTTPS: https endpoint config, dev self-signed certs, force_ssl behind proxies, and HSTS pitfalls on localhost."
sources:
  - https://hexdocs.pm/phoenix/using_ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: serve requests over SSL, redirect HTTP to HTTPS, and use HSTS safely.

## HTTPS config
You need a key file and a certificate (PEM) file from a certificate authority; pass their paths via environment variables. In `config/runtime.exs`:
```elixir
config :hello, HelloWeb.Endpoint,
  http: [port: String.to_integer(System.get_env("PORT"))],
  url: [host: "example.com"],
  cache_static_manifest: "priv/static/cache_manifest.json",
  https: [
    port: 443,
    cipher_suite: :strong,
    otp_app: :hello,
    keyfile: System.get_env("SOME_APP_SSL_KEY_PATH"),
    certfile: System.get_env("SOME_APP_SSL_CERT_PATH"),
    # OPTIONAL Key for intermediate certificates:
    cacertfile: System.get_env("INTERMEDIATE_CERTFILE_PATH")
  ]
```
With `otp_app:`, relative paths resolve from the app root (e.g. `priv/our_keyfile.key`). Without it use absolute paths, e.g. `Path.expand("../../../some/path/to/ssl/key.pem", __DIR__)`. The `https:` options go to the Plug adapter (typically Bandit), which uses `Plug.SSL`; see `Plug.SSL.configure/1`.

## Dev
`mix phx.gen.cert` generates a self-signed certificate (needs Erlang/OTP 20 or later). In `config/dev.exs`:
```elixir
https: [
  port: 4001,
  cipher_suite: :strong,
  keyfile: "priv/cert/selfsigned_key.pem",
  certfile: "priv/cert/selfsigned.pem"
]
```
It can replace `http` or run on a different port beside it.

## Force SSL
`:force_ssl` redirects HTTP to HTTPS (options forwarded to `Plug.SSL`; by default it sets the strict-transport-security header):
```elixir
config :my_app, MyAppWeb.Endpoint,
  force_ssl: [rewrite_on: [:x_forwarded_proto]]
```
Redirects use the `:host` from `:url`. `rewrite_on` names the proxy/load-balancer header indicating the original scheme. To redirect to the current request's host, set `host: nil` and, behind a proxy, `x_forwarded_host` and `x_forwarded_port`:
```elixir
force_ssl: [rewrite_on: [:x_forwarded_proto, :x_forwarded_host, :x_forwarded_port], host: nil]
```
Requests from localhost are not redirected; for probes from "127.0.0.1" or an internal IP, use `exclude: ["localhost", "127.0.0.1"]`.

Gotcha: `force_ssl` is compile-time config, so set it in `prod.exs`; it will not work from `runtime.exs`.

## HSTS
`force_ssl: [hsts: true]` adds the `Strict-Transport-Security` header with a max-age. Browsers keep the policy until it expires, and assume traffic on any port other than 80 is encrypted. Recommended in production, but hitting `https://localhost:4000` with HSTS can break other local HTTP servers/proxies. To recover: Chrome, DevTools open, hold the reload icon, "Empty Cache and Hard Reload"; Safari, clear cache, remove the entry from `~/Library/Cookies/HSTS.plist` (or delete it), restart. Or set `:expires` on `force_ssl` to `0` to expire the entry and disable HSTS.

## Checked

2026-11-08. Read the Phoenix guide Using SSL in full. Confirmed the https endpoint options, otp_app path rule, mix phx.gen.cert (Erlang/OTP 20 or later), force_ssl and rewrite_on options, the compile-time prod.exs note, and the HSTS section including the Chrome and Safari reset steps and expires: 0. Nothing removed.

Method: documentation only; no commands were run.
