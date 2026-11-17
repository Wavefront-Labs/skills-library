---
id: computing-software.systems-network-administration.dns-dhcp.rndc-confgen-and-control-keys
name: rndc-confgen-and-control-keys
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, rndc-confgen, rndc, tsig, controls]
level: practitioner
status: docs-checked
description: "Set up rndc control for BIND: rndc-confgen -a and explicit key/controls configuration, the default control channel, read-only channels, and disabling the channel."
sources:
  - https://bind9.readthedocs.io/en/latest/manpages.html#rndc-confgen-rndc-key-generation-tool
  - https://bind9.readthedocs.io/en/latest/reference.html#controls-block-definition-and-usage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rndc-confgen and key files

rndc talks to named over a control channel, authorised by the `allow` and `keys` clauses of the
`controls` statement.

## Default local setup
```
rndc-confgen -a
```
- `-a` creates `/etc/rndc.key`, read by both rndc and named on startup. It defines a default
  command channel and key so rndc can talk to named on the local host with no further config.
- `-A algorithm` picks the TSIG algorithm (hmac-md5, hmac-sha1, hmac-sha224, hmac-sha256,
  hmac-sha384, hmac-sha512; default hmac-sha256). `-c keyfile` (with `-a`) gives an alternate
  location, `-u user` sets the file owner, `-k keyname` sets the key name (default `rndc-key`).
- With no `controls` statement, named listens on 127.0.0.1 and ::1; likewise when `controls` has
  no `keys` clause, named loads the key from `/etc/rndc.key`.

## Explicit config (for example remote use)
Run `rndc-confgen` without `-a`: it prints a sample `rndc.conf` and the matching `controls` and
`key` statements to insert into `named.conf`. Options: `-s address` (address named listens on,
default 127.0.0.1), `-p port` (default 953), `-b keysize` (1 to 512 bits; default the hash size).

An `inet` control channel is a TCP socket; if no port is given, 953 is used. `*` is the IPv4
wildcard and `::` the IPv6 wildcard, but the manual recommends the loopback address when rndc is
only used on the local host. Shape of a statement:

```
controls {
    inet 127.0.0.1 port 953 allow { 127.0.0.1; } keys { "rndc-key"; };
};
```
`allow` is simple IP filtering; `keys` is the primary authorisation mechanism.

## Restricting and disabling
- `read-only yes;` on a channel limits it to: nta -dump, null, status, showzone, zonestatus.
  Default is read-write.
- An empty `controls { };` disables the command channel.

## Verify
- [ ] `rndc status` (a read-only command) works locally with the generated key.

## Checked
2026-11-01. Confirmed in the BIND 9 ARM (rndc-confgen man page and the controls block section):
`-a`, `-A`, `-b`, `-c`, `-k`, `-p`, `-s`, `-u` and defaults, `/etc/rndc.key`, default loopback
channel, port 953, `allow`/`keys`, `read-only` command list, empty `controls { }`. Removed: the
wrong `rndc-confgen -a -A` combined example's `/etc/bind` path, chown/chmod lines, a version
gate for read-only keys, the troubleshooting table and the encryption claim, which these pages
do not state.
Method: documentation only; no commands were run.
