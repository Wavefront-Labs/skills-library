---
id: computing-software.database-administration.couchdb.tls-distribution-certificates
name: tls-distribution-certificates
category: computing-software
field: database-administration
product: couchdb
tags: [tls, erlang-distribution, certificates, couch-dist-conf, verify-peer]
level: advanced
status: docs-checked
description: "Prepare the couch_dist.conf certificate options for TLS between CouchDB nodes: server and client sections, verify_peer, and certificate pitfalls."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/tls_erlang_distribution.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
TLS Erlang distribution protects data moving between nodes, and can coexist with plain TCP to some nodes. It needs a `couch_dist.conf` file:

```
[{server,
  [{cacertfile, "</absolute_path/to/ca-cert.pem>"},
   {certfile,   "</absolute_path/to/erlserver.pem>"},
   {secure_renegotiate, true},
   {verify, verify_peer},
   {fail_if_no_peer_cert, true}]},
 {client,
  [{cacertfile, "</absolute_path/to/ca-cert.pem>"},
   {keyfile,    "</absolute_path/to/key.pem>"},
   {certfile,   "</absolute_path/to/cert.pem>"},
   {secure_renegotiate, true},
   {verify, verify_peer}]}].
```

`erlserver.pem` holds the certificate and its private key (the page builds it with `cat key.pem cert.pem`); the certificate must be trusted by a known root.

Notes:

- With `verify_peer`, also set `server_name_indication`.
- `{fail_if_no_peer_cert, true}` goes on the server side only in OTP 26; earlier versions allow both sides.
- The Common Name must differ between the CA certificate and the node certificate, and the node certificate's FQDN must equal the hostname.
- The page's example cert commands are not an endorsement of any expiry, key size or algorithm.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/tls_erlang_distribution page: couch_dist.conf server and client options, the erlserver.pem construction, and the notes on server_name_indication, fail_if_no_peer_cert on OTP 26, Common Name and FQDN, no endorsement of certificate parameters. Nothing removed.

Method: documentation only; no commands were run.
