---
id: computing-software.software-engineering.erlang.ssl-tls
name: ssl-tls
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-networking, ssl-tls]
level: advanced
status: draft
description: "Erlang ssl: verify_peer with CA certs, SNI, hostname check, TLS versions and server certificate options."
sources:
  - https://www.erlang.org/doc/apps/kernel/
  - https://www.erlang.org/doc/apps/ssl/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ssl client and server
**Goal:** make TLS connections that verify the peer.

```erlang
{ok, _} = application:ensure_all_started(ssl),
Opts = [{verify, verify_peer},
        {cacerts, public_key:cacerts_get()},                 % OTP 25+
        {server_name_indication, "example.org"},
        {customize_hostname_check,
          [{match_fun, public_key:pkix_verify_hostname_match_fun(https)}]},
        {versions, ['tlsv1.3', 'tlsv1.2']}],
{ok, S} = ssl:connect("example.org", 443, Opts, 5000).
```
- Since OTP 26 the default is `verify_peer`; you must supply `cacerts` (or `cacertfile`) or connect fails. Older releases defaulted to `verify_none` (insecure).
- Server side: `{certfile, ...}`, `{keyfile, ...}`, `ssl:listen/2`, `ssl:transport_accept/1`, `ssl:handshake/1`.
- Never ship `{verify, verify_none}` outside tests.

## Gotchas
- Missing SNI breaks virtual-hosted servers.
- Hostname checks are not done by default in older releases unless `customize_hostname_check` is set.

## Self-check
Connect to a public host with and without `cacerts` and compare results.
