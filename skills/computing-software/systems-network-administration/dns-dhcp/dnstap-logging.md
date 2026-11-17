---
id: computing-software.systems-network-administration.dns-dhcp.dnstap-logging
name: dnstap-logging
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dnstap, query-logging, bind, unbound, dnsdist, observability]
level: practitioner
status: docs-checked
description: "Enable dnstap structured logging on BIND, Unbound and dnsdist, collect with fstrm socket readers, and decode with dnstap-read for high-volume query analysis."
sources:
  - https://dnstap.info/
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-dnstap
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://doc.powerdns.com/dnsdist/reference/dnstap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnstap logging

dnstap logs DNS messages in protobuf over Frame Streams, asynchronously, with far less overhead
than text query logs; it can include full wire-format queries and responses.

## BIND (built with `--enable-dnstap`)
```
options {
    dnstap { client; auth response; resolver query; };
    dnstap-output unix "/var/run/named/dnstap.sock";      // or: file "/var/log/named/dnstap.fstrm" size 100m versions 5;
    dnstap-identity hostname;
};
```
Message types are `client`, `auth`, `resolver`, `forwarder`, `update` and `all`; each can take `query` or `response` (both by default). `dnstap-output` takes `file` or `unix` and a path; for `file`, `size`, `versions` and `suffix` control rolling (default: no rolling). It can only be set once while named runs (not changed by `rndc reload` or `reconfig`). `rndc dnstap -reopen` reopens the file and `rndc dnstap -roll [number]` rolls it. `dnstap-identity` defaults to the hostname and `dnstap-version` to the BIND version. BIND must be built with `--enable-dnstap` (libfstrm and protobuf-c).

## Unbound
```
dnstap:
    dnstap-enable: yes
    dnstap-socket-path: "/path/to/dnstap.sock"   # Unbound connects to a server listening here
    dnstap-send-identity: yes
    dnstap-log-client-query-messages: yes
    dnstap-log-client-response-messages: yes
```
Unbound must be built with dnstap support; `dnstap-ip` (with `dnstap-tls`) can send to a TCP/TLS server instead of a unix socket.

## dnsdist
```lua
fsul = newFrameStreamUnixLogger("/path/to/dnstap.sock")
addAction(AllRule(), DnstapLogAction("dnsdist", fsul))
addResponseAction(AllRule(), DnstapLogResponseAction("dnsdist", fsul))
```

## Collecting
- With a unix socket, a reader such as `fstrm_capture` (from libfstrm) must be listening on the socket, otherwise BIND does not send dnstap messages.
- `dnstap-read -y file` prints BIND's detailed YAML form (`-p` adds the DNS message text, `-x` a hex dump, `-t` long timestamps) for ingestion into your log pipeline.

## Gotchas
- Start the collector before enabling socket output. In BIND, resolver traffic in dnstap omits server-side socket addresses unless the query source address is set (or BIND is built with `-DISC_SOCKET_DETAILS=1`, which lowers performance).
- Logs contain user browsing data: retention and access policy needed.

## Verify
- [ ] `dnstap-read` shows client query/response pairs for a test lookup.

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27), read on 2026-10-26. NLnetLabs/unbound doc sources (unbound.conf.rst, unbound-control.rst, unbound-anchor.rst, repository pushed 2026-10-21), read on 2026-10-26. PowerDNS dnsdist reference docs (pdns repository, pushed 2026-10-23). Confirmed: BIND dnstap/dnstap-output/dnstap-identity/dnstap-version grammar and semantics, fstrm tunables exist, rndc dnstap -reopen/-roll, dnstap-read options -y -p -x -t, Unbound dnstap-* options (enable, socket-path, send-identity, log-client-*-messages, ip, tls), dnsdist newFrameStreamUnixLogger, DnstapLogAction and DnstapLogResponseAction. Removed unconfirmed fstrm_capture flags and third-party collectors.

Method: documentation only; no commands were run.
