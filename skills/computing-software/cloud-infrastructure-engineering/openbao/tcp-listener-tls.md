---
id: computing-software.cloud-infrastructure-engineering.openbao.tcp-listener-tls
name: tcp-listener-tls
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, listener, tcp, tls, client-certificate]
level: practitioner
status: docs-checked
description: "Configure the OpenBao TCP listener: addresses, TLS files and versions, auto-reload, client certs, PROXY protocol and X-Forwarded-For."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/configuration/listener/tcp.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP listener and TLS

## Addresses

- `address` default `127.0.0.1:8200`
- `cluster_address` default `127.0.0.1:8201` (one port above `address`)

## TLS (on by default)

- `tls_disable` false; `tls_cert_file` and `tls_key_file` required when TLS is on. Both reload on SIGHUP (changing the path while running does not).
- `tls_auto_reload` false; `tls_auto_reload_interval` `30s`, minimum 5s.
- `tls_min_version` `tls12`, `tls_max_version` `tls13`.
- `tls_cipher_suites` applies only to TLS 1.2 and earlier.
- `tls_require_and_verify_client_cert` with `tls_client_ca_file`; it is mutually exclusive with `tls_disable_client_certs`.

## Behind proxies

- `proxy_protocol_behavior`: `use_always`, `allow_authorized`, `deny_unauthorized` (v1), with `proxy_protocol_authorized_addrs` (cannot be empty, not needed for `use_always`).
- `x_forwarded_for_authorized_addrs` (CIDRs) to enable; `x_forwarded_for_hop_skips` 0; `x_forwarded_for_reject_not_authorized` and `x_forwarded_for_reject_not_present` default true.

## Gotchas

- `tls_prefer_server_cipher_suites` is deprecated and does nothing.
- Since v2.5.0 `disable_unauthed_rekey_endpoints` defaults to true; since v2.5.3 `disable_unauthed_generate_root_endpoints` does.
- A public server using ACME without `tls_acme_domains` lets others trigger certificate requests against your quota.

## Checked

2026-11-04. Read the OpenBao TCP listener page in full. Confirmed: address defaults, TLS parameters and defaults, SIGHUP and auto-reload behaviour, cipher suite note, client certificate options and their mutual exclusion, PROXY protocol values, X-Forwarded-For options and defaults, the deprecated `tls_prefer_server_cipher_suites` and the v2.5.0 and v2.5.3 defaults and the ACME warning. Removed: nothing.
Method: documentation only; no commands were run.
