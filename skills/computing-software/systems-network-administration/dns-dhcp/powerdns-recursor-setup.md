---
id: computing-software.systems-network-administration.dns-dhcp.powerdns-recursor-setup
name: powerdns-recursor-setup
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, powerdns-recursor, recursor, resolver, lua-scripting]
level: practitioner
status: docs-checked
description: "Deploy PowerDNS Recursor: YAML/legacy config, allow-from, forward zones, DNSSEC validation modes, Lua policy hooks, RPZ and rec_control monitoring."
sources:
  - https://doc.powerdns.com/recursor/
  - https://doc.powerdns.com/recursor/yamlsettings.html
  - https://doc.powerdns.com/recursor/manpages/rec_control.1.html
  - https://doc.powerdns.com/recursor/lua-scripting/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerDNS Recursor

A recursive resolver with Lua scripting hooks.

## Config (5.x YAML, `recursor.yml` in the config directory, usually `/etc/powerdns`)
```yaml
incoming:
  listen: [0.0.0.0, '::']
  allow_from: [127.0.0.0/8, 10.0.0.0/8, '::1/128']
recursor:
  forward_zones:
    - zone: corp.example
      forwarders: [10.1.1.10, 10.1.1.11]
  serve_rfc1918: true
dnssec:
  validation: validate      # off, process-no-validate, process (default), log-fail, validate
recordcache:
  max_entries: 2000000
webservice:
  webserver: true
  address: 127.0.0.1
  api_key: <secret>
```
Defaults: `incoming.listen` is `[127.0.0.1, '::1']`, `incoming.allow_from` is the loopback, private and
link-local ranges, `recordcache.max_entries` is 1000000, `webservice.webserver` is false and `webservice.address`
is 127.0.0.1. If both `recursor.conf` and `recursor.yml` exist, the YAML file is used; from 5.1.0 a `recursor.conf`
is read as YAML first. Old-style names are `allow-from`, `forward-zones`, `local-address`, `serve-rfc1918`.
`rec_control show-yaml [FILE]` shows the YAML conversion of an old-style file.

## DNSSEC validation
`process` does validation for clients that request it (AD or DO bit in the query); `log-fail` also validates
RRSIGs and logs bogus responses; `validate` is full validation and sends SERVFAIL on bogus responses.
Negative trust anchors for broken domains: `rec_control add-nta broken.example "vendor issue"`
(syntax `add-nta DOMAIN [REASON]`).

## Lua policy
```lua
function preresolve(dq)
  if dq.qname:equal("blocked.example") then
    dq.rcode = pdns.NXDOMAIN
    return true
  end
  return false
end
```
Set the script with `recursor.lua_dns_script` (path to your policy file). `preresolve()` must return true when
it has taken over the query; `pdns.NXDOMAIN` is a valid rcode to set. RPZ zones are configured under
`recursor.rpzs`.

## Operations
```
rec_control get-all                        # all statistics; filter the output for cache and servfail counters
rec_control wipe-cache example.com$        # trailing $ wipes the whole tree; also wipes the negative cache
rec_control trace-regex 'example\.com\.$' -   # trace matching queries to stdout (FILE argument, 4.9.0 and later)
rec_control ping                           # check the server is alive
```
The trace regex is matched against names ending in a dot.

## Verify
- [ ] Queries from allowed nets resolve with AD on signed zones; disallowed nets get REFUSED; `rec_control ping` succeeds.

## Checked
Date: 2026-10-28.
Confirmed against the Recursor YAML settings reference (incoming.listen, allow_from, recordcache.max_entries,
recursor.forward_zones, serve_rfc1918, dnssec.validation modes, webservice.*, recursor.rpzs, lua_dns_script,
recursor.yml/recursor.conf rules), the rec_control man page (add-nta, get-all, wipe-cache, trace-regex, ping,
show-yaml) and the Lua hooks page (preresolve, dq.qname:equal, dq.rcode, pdns.NXDOMAIN). Corrected: the config file name (`recursor.yml`),
the trace-regex form (needs a FILE argument and matches names with a trailing dot), the validation mode list.
Removed: "popular at ISPs", the `rpzFile`/`rpzPrimary` names and the exact old-style forward-zones syntax (not on the
fetched pages).
Method: documentation only; no commands were run.
