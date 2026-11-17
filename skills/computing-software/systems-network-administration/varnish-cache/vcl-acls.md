---
id: computing-software.systems-network-administration.varnish-cache.vcl-acls
name: vcl-acls
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [acl, client-ip, acl-flags, access-control]
level: practitioner
status: docs-checked
description: "Define VCL ACLs for IP matching: entries, subnets, negation, host-name resolution caveats, and the log, table, pedantic and fold flags."
sources:
  - https://www.varnish.org/docs/reference/vcl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vcl acls

```vcl
acl localnetwork {
    "localhost";            # myself
    "192.0.2.0"/24;         # and everyone on the local network
    ! "192.0.2.23";         # except for the dial-in router
}
sub vcl_recv {
    if (client.ip ~ localnetwork) { return (pipe); }
}
```

- An ACL declaration creates and initialises a named access control list used to match client addresses. Match with `~` (non-match `!~`). Entries can be host names, addresses and masks; `!` negates an entry.
- A host name Varnish cannot resolve matches any address it is compared to, so a negated unresolvable entry rejects every address. Enclosing the entry in parentheses makes it simply ignored when it cannot be resolved.

Flags per ACL, for example `acl foo -pedantic +log { "firewall.example.com" / 24; }`:
- `+log`: emit an `Acl` record in VSL telling whether a match was found.
- `+table`: implement the ACL with a table instead of compiled code; runs a little slower but compiles large ACLs much faster.
- `-pedantic`: allow masks to cover non-zero host bits. If the name resolves to both IPv4 and IPv6 you still get an error.
- `-fold`: do not fold supernets and adjacent networks. Folding is on by default: a subnet contained in another entry is skipped (1.2.3.128/25 inside 1.2.3.0/24) and adjacent entries are merged (1.2.3.0/25 and 1.2.3.128/25 become 1.2.3.0/24). Skips and folds are warnings at compile time unless `+fold(-report)` is used (`+fold(+report)` is the default); the report sub-flag is valid only with `+fold`. With folding on, VSL `VCL_acl` matches on skipped entries are logged as matches on the supernet, and folded matches use a shorter netmask marked `fixed: folded`. Negated entries are never folded.

Symbols that are declared but not used (such as an ACL) cause a compile error unless marked with `unused acl1;`; alternatively start varnishd with `-p vcc_feature=-err_unref` to make this a warning globally.

## Checked
2026-11-08. Read in full: the VCL reference page. Confirmed: ACL syntax, unresolvable-host behaviour, flags and fold details, unused marker. Changed: `+log` now matches the page wording (reports whether a match was found).
Method: documentation only; no commands were run.
