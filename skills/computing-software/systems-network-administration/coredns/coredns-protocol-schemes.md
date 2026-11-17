---
id: computing-software.systems-network-administration.coredns.coredns-protocol-schemes
name: coredns-protocol-schemes
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, dot, doh, grpc, scheme, tls]
level: practitioner
status: docs-checked
description: "Choose between plain DNS, DNS over TLS, DNS over HTTPS and DNS over gRPC by prefixing the zone in a server block with a scheme."
sources:
  - https://coredns.io/manual/configuration/
  - https://coredns.io/plugins/tls/
  - https://coredns.io/plugins/timeouts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make a server block accept a specific DNS transport.

CoreDNS accepts four protocols. Prefix the zone name in the block header with a scheme:
- `dns://` plain DNS. This is the default when no scheme is given.
- `tls://` DNS over TLS, RFC 7858.
- `https://` DNS over HTTPS, RFC 8484.
- `grpc://` DNS over gRPC.

Examples adapted from the tls plugin docs (file names are placeholders):

```
tls://.:5553 {
    tls cert.pem key.pem ca.pem
    forward . /etc/resolv.conf
}
grpc://. {
    tls cert.pem key.pem ca.pem
    forward . /etc/resolv.conf
}
https://. {
    tls cert.pem key.pem ca.pem
    forward . /etc/resolv.conf
}
```

Notes:
- The tls plugin supplies the certificate for the TLS, gRPC and DoH servers. If it is omitted, no encryption takes place.
- The tls plugin's optional CA argument is only meaningful with client_auth verify_if_given or require_and_verify.
- The timeouts plugin applies read, write and idle timeouts to the TCP, TLS and DoH servers; DoQ servers (quic://) use read and idle only.
- The manual lists four protocols; the timeouts plugin docs also show a quic:// scheme for DNS over QUIC.

## Checked

2026-11-08. Read the configuration manual page in full plus the tls and timeouts plugin READMEs in full. Replaced placeholder machine paths, dropped unsupported claims on root-relative cert paths and the server metrics label, and added the https and quic schemes as shown in the plugin docs.

Method: documentation only; no commands were run.
