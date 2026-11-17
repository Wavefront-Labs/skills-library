---
id: computing-software.systems-network-administration.coredns.coredns-tls-plugin
name: coredns-tls-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, tls, dot, doh, client-auth]
level: practitioner
status: docs-checked
description: "Configure server certificates for DNS-over-TLS, gRPC and DoH with the tls plugin, including client_auth modes and keylog."
sources:
  - https://coredns.io/plugins/tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: terminate TLS for encrypted DNS transports.

Syntax:

```
tls CERT KEY [CA] {
    client_auth nocert|request|require|verify_if_given|require_and_verify
    keylog FILE
}
```

- Without the plugin there is no encryption.
- `client_auth` maps to the Go tls ClientAuthType values NoClientCert, RequestClientCert, RequireAnyClientCert, VerifyClientCertIfGiven and RequireAndVerifyClientCert. Default is `nocert`. Supplying CA only makes sense with `verify_if_given` or `require_and_verify`; without CA, system CAs verify client certificates.
- `keylog FILE` exports TLS secrets for external decryption. It compromises security and is for debugging only.
- Minimum TLS version is 1.2; maximum, cipher suites and key exchange follow Go crypto/tls defaults.
- Certificates can instead be obtained and renewed with ACME (`tls { acme DOMAIN... }`). It uses the DNS-01 challenge only, answered by the same CoreDNS process on port 53, so the domain's authoritative DNS must reach that instance. Optional properties: `email`, `ca` (defaults to the Let's Encrypt production directory), `storage`, `ca_root`, `resolver` (HOST:PORT).

Examples, one per transport:

```
tls://.:5553 {
    tls /path/to/cert.pem /path/to/key.pem /path/to/ca.pem
    forward . /path/to/resolv.conf
}
grpc://. {
    tls /path/to/cert.pem /path/to/key.pem /path/to/ca.pem
    forward . /path/to/resolv.conf
}
```

The gRPC protobuf is defined in pb/dns.proto as a simple wrapper around the DNS wire message. The same plugin supplies the certificate for DoH: use an `https://.` server block.

## Checked

2026-11-08. Checked in full against the tls plugin README. Removed an unsupported root-plugin claim and a reference to grpc_server; added the ACME mode (DNS-01 only, defaults) and the DoH note.

Method: documentation only; no commands were run.
