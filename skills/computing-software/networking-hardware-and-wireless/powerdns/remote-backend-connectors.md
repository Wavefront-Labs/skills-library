---
id: computing-software.networking-hardware-and-wireless.powerdns.remote-backend-connectors
name: remote-backend-connectors
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, remote-backend, remote-connection-string, http, unix, zeromq, json-rpc]
level: advanced
status: docs-checked
description: "Connect PowerDNS to an external backend with remote-connection-string: unix, pipe, http and zeromq strings, initialize and lookup, caveats."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/remote.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote backend connectors

Settings: `remote-connection-string` and `remote-dnssec`. Every connector takes `timeout` in ms (default 2000).

Connection strings:
- `unix:path=/path/to/socket`
- `pipe:command=/path/to/executable,timeout=2000`
- `http:url=http://localhost:63636/dns,url-suffix=.php` (also `post` and `post_json`, accepting 1, yes, on or true)
- `zeromq:endpoint=ipc:///tmp/tmp.sock`

Mandatory methods:
- `initialize`: `{"method":"initialize","parameters":{...}}`; reply `{"result":true}` or false. Not called for HTTP.
- `lookup` with parameters `qtype`, `qname`, `zone_id`, optionally `remote`, `local`, `real-remote`. The docs list the parameter as `zone_id` but their JSON example spells it `zone-id`; their example is `{"method":"lookup","parameters":{"qtype":"ANY","qname":"www.example.com.","zone-id":-1}}`. Reply with an array of objects holding `qtype`, `qname`, `content`, `ttl` and optionally `domain_id`, `scopeMask`, `auth`.

Reply rules:
- Always a JSON hash with `result`; boolean false means failure.
- An HTTP 200 with no body counts as `{"result":true}`.
- An optional `log` array is written at info level.

Caveats:
- Since 4.0 names carry a trailing dot and priority is part of `content` (MX, SRV).
- HTTPS is unsupported (use stunnel), as is HTTP authentication.
- Leaving out `auth` can cause trouble with DNSSEC.
- Build with `--with-modules="remote"`; ZeroMQ needs `--enable-remotebackend-zeromq`.

## Checked

2026-11-08. Read docs/backends/remote.rst up to the end of the list and getBeforeAndAfterNamesAbsolute methods (roughly the first 330 lines: feature table, notices, compiling, usage and all four connectors, reply rules, required-methods table, initialize, lookup, APILookup and list); the later DNSSEC and zone-management method sections were not read and the skill makes no claims about them. Corrected the lookup example to the docs' own spelling zone-id and flagged the inconsistency. Description shortened.

Method: documentation only; no commands were run.
