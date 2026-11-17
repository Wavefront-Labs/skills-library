---
id: computing-software.cryptography-implementation.protocol-implementation.sni-based-multi-certificate-hosting
name: sni-based-multi-certificate-hosting
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, sni-routing, server-name-indication, multi-tenant-tls, virtual-hosting, nginx, haproxy]
level: practitioner
status: docs-checked
description: "Host many TLS certificates on one IP with SNI: nginx and HAProxy certificate selection, default server behaviour, clients without SNI, and verifying with openssl s_client."
sources: ["https://www.rfc-editor.org/rfc/rfc6066#section-3", "https://nginx.org/en/docs/http/configuring_https_servers.html", "https://docs.haproxy.org/2.8/configuration.html#5.1-crt-list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNI-based multi-certificate hosting

## How selection works
The client sends the hostname in the ClientHello `server_name` extension (RFC 6066 section 3). Literal IPv4 and
IPv6 addresses are not permitted in `HostName`; nginx notes some browsers erroneously send the server's IP, so do
not rely on it. The server picks a certificate before any HTTP request is seen.

## Configuration
- nginx: one `server { listen 443 ssl; server_name a.example.com; ssl_certificate ...; }` per name. A client that
  sends no SNI gets the entire SSL configuration of the default server.
- HAProxy: `bind :443 ssl crt <directory>` loads certificates from a directory and presents the one whose CN or
  alt subjects match the client's SNI (a wildcard replaces the first label only). An empty directory stops
  HAProxy starting unless `strict-sni` is used; with `strict-sni`, a handshake with no matching certificate is
  rejected rather than served the default.

## Default certificate
Clients without SNI get the default certificate. Choose deliberately: a generic certificate, or refuse them with
nginx `ssl_reject_handshake on;` in the default server (the nginx docs show it with `return 421;`) or HAProxy
`strict-sni`, so scanners do not learn your hostnames from the default certificate.

## Pitfalls
- nginx needs SNI support in both the OpenSSL it was built with and the one it is linked to at run time; `nginx -V`
  shows "TLS SNI support enabled" when built in.
- Client certificate verification in name-based servers: a client without SNI is handled by the default server's
  whole SSL configuration, so limit such connections with `ssl_reject_handshake` there.

## Verify
```sh
for h in a.example.com b.example.com; do openssl s_client -connect 203.0.113.10:443 -servername $h </dev/null 2>/dev/null | openssl x509 -noout -subject; done
openssl s_client -connect 203.0.113.10:443 -noservername </dev/null    # default behaviour
```

## Checked
2026-11-01. Confirmed against RFC 6066 section 3, the nginx HTTPS servers page (SNI, default server, ssl_reject_handshake, SNI build support) and the HAProxy 2.8 configuration manual (crt directory loading, wildcard matching, strict-sni). Removed Envoy, Go, ssl_preread, ECH, domain-fronting, nginx version and legacy-client claims (not in the fetched pages).
Method: documentation only; no commands were run.
