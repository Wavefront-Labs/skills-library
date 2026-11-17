---
id: computing-software.cryptography-implementation.crypto-libraries.go-crypto-tls-config-hardening
name: go-crypto-tls-config-hardening
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, golang, go-crypto, go-tls-config, tls-hardening, mtls, x25519mlkem768]
level: advanced
status: verified
description: "Harden Go crypto/tls Config for clients and servers: MinVersion, what CipherSuites affects, curve and PQ hybrid preferences, GetCertificate reload, mTLS and GODEBUG traps."
sources: ["https://pkg.go.dev/crypto/tls", "https://go.dev/doc/godebug", "https://go.dev/doc/go1.24", "https://go.dev/blog/tls-cipher-suites"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto/tls Config hardening (Go)

Go's defaults are good and get better each release; most hardening is about not undoing them.

## Server
```go
cfg := &tls.Config{
    MinVersion: tls.VersionTLS12,
    GetCertificate: certReloader.Get,   // hot reload; reads from an atomic.Pointer[tls.Certificate]
    // CipherSuites: leave nil; Go's default order is AEAD + ECDHE only
    // CurvePreferences: leave nil; Go 1.24+ default includes X25519MLKEM768 (Go 1.26+ adds SecP256r1MLKEM768 and SecP384r1MLKEM1024)
}
srv := &http.Server{Addr: ":443", TLSConfig: cfg, ReadHeaderTimeout: 10 * time.Second}
log.Fatal(srv.ListenAndServeTLS("", ""))
```
- `CipherSuites` only affects TLS 1.0-1.2. TLS 1.3 suites are not configurable (all are safe).
- `PreferServerCipherSuites` is deprecated and ignored; Go picks suites by hardware support.
- `MinVersion` defaults to TLS 1.2 for clients (Go 1.18+) and servers (Go 1.22+; a Go 1.27.3 server rejected a TLS 1.1
  client, checked). Set it anyway so older toolchains don't silently weaken.
- Session ticket keys rotate automatically (daily, dropped after seven days per the `SessionTicketKey` docs) until you call
  `SetSessionTicketKeys`, which turns automatic rotation off; if you run many replicas and set shared keys, rotate them
  yourself.

## Client
```go
cfg := &tls.Config{
    MinVersion: tls.VersionTLS12,
    RootCAs:    pool,          // nil = system roots; set only for private PKI
    ServerName: "api.example.com", // only if dialling by IP or through a tunnel
}
```
Never `InsecureSkipVerify: true` to fix a certificate problem. If you need custom verification
(SPIFFE, pinning), keep normal verification and add `VerifyConnection`, which runs after it.

## mTLS server
```go
cfg.ClientAuth = tls.RequireAndVerifyClientCert
cfg.ClientCAs  = clientCAPool
cfg.VerifyConnection = func(cs tls.ConnectionState) error {
    return authorise(cs.PeerCertificates[0])   // map identity to permissions
}
```
`RequireAnyClientCert` does **not** verify the chain; it only requires that something was sent (`crypto/tls` docs: the certificate is not required to be valid).

## GODEBUG compatibility switches
Go removes weak options from defaults and exposes temporary switches: `tlsrsakex=1` (RSA key
exchange, off by default since 1.22), `tls3des=1` (3DES, off since 1.23), `tls10server=1` (TLS 1.0 server minimum,
off since 1.22) and `tlsmlkem=0` (turn off the hybrid PQ group if a middlebox chokes on large ClientHellos; a client with
`GODEBUG=tlsmlkem=0` negotiated plain X25519, checked). **`tlsrsakex`, `tls3des` and `tls10server` were removed in Go 1.27**
(go.dev/doc/godebug), so on 1.27 the only way back to those is `MinVersion`/`CipherSuites` on the `tls.Config`.
Switches are set in `go.mod` (`godebug` block), `//go:debug` lines or the environment, and each one is a weakening that
should carry a ticket and removal date.

## Operational rules
- Don't modify a `tls.Config` after passing it to a server or client; `Clone()` and change the copy.
- `KeyLogWriter` writes session secrets; only behind a debug flag, never in production builds.
- HTTP/2 requires TLS 1.2+ with an AEAD suite; custom `CipherSuites` lists that drop
  `TLS_ECDHE_*_GCM_*` break HTTP/2 with an error from `ServeTLS` (checked): `http2: TLSConfig.CipherSuites is missing an HTTP/2-required AES_128_GCM_SHA256 cipher (need at least one of TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 or TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256)`.

## Verify
- [ ] No `InsecureSkipVerify`, `tlsrsakex`, or `tls10server` in code or config without an exception record.
- [ ] A test client with `MaxVersion: tls.VersionTLS11` is refused (`protocol version not supported`) and a default Go client
      reports `ConnectionState().CurveID == tls.X25519MLKEM768` on Go 1.24+ (both checked). `openssl s_client -groups
      X25519MLKEM768` needs an OpenSSL build with that group; 3.2.3 reports `group 'X25519MLKEM768' cannot be set`.
- [ ] Certificate rotation works without restart.
