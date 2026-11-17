---
id: computing-software.networking-hardware-and-wireless.haproxy.acl-definitions-and-matching
name: acl-definitions-and-matching
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, acl, acl-fetch, hdr-host, path-beg, acl-flags, acl-logic]
level: practitioner
status: docs-checked
description: "Write HAProxy ACLs with fetches and flags (-i, -m, -f), combine them with and/or/!, and avoid the common pattern-matching mistakes."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# acl definitions and matching
An ACL is `acl <name> <fetch> [flags] [-- ]<patterns>`. Fetches pull a value from the request (`hdr(host)`, `path`, `src`, `method`, `ssl_fc_sni`, `req.ssl_sni`), and the match type compares it.

```
acl is_api  path_beg /api/
acl is_host hdr(host) -i -m str api.example.com
acl is_internal src 10.0.0.0/8 192.168.0.0/16
acl is_img  path_end -i .png .jpg .gif
acl blocked src -f /etc/haproxy/blocked.lst
use_backend be_api if is_api is_host !is_internal
http-request deny if blocked
```
Conditions are ANDed implicitly, `or` (or `||`) is explicit alternation and `!` negates. Several ACLs declared with the same name are ORed together. Flags: `-i` ignore case for the patterns after it, `-f file` loads patterns from a file (several `-f` allowed), `-m <method>` forces the match method (`found`, `bool`, `int`, `ip`, `bin`, `len`, `str`, `sub`, `reg`, `beg`, `end`, `dir`, `dom`), `-M` loads the `-f` file like a map (two columns), `-n` forbids DNS resolution of IP lists, `-u` forces the ACL's unique id, and `--` ends the flags (needed when a pattern looks like a flag).

Gotchas: `-i` only applies to entries after it, not to files loaded before it; `-m`, if combined with `-f`, must come first; `path_beg /api` also matches `/apixyz` (it is a prefix match), so use `/api/`; a binary sample needs an explicit `-m`.

Verify: `haproxy -c -f <config>`; test with `curl -H 'Host: api.example.com' http://lb/api/x` and watch the chosen backend in the log.

## Checked
2026-11-03. Confirmed against configuration.html (section 7.1 ACL basics, flags and matching methods; 7.2 conditions, same-name ACLs ORed; sample fetches `ssl_fc_sni`, `req.ssl_sni`, `hdr`). Removed: the claim that `hdr(host)` includes the port while `hdr_dom` or `field(1,:)` strips it (not in the docs; `hdr_dom` is a domain match), and the `%b` log-field hint.
Method: documentation only; no commands were run.
