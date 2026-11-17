---
id: computing-software.software-engineering.go.tls-servers-and-clients-with-crypto-tls
name: tls-servers-and-clients-with-crypto-tls
category: computing-software
field: software-engineering
product: go
tags: [go, golang, crypto-tls, tls, mtls, x509, certificate-rotation, autocert, https, go-http2]
level: advanced
status: docs-checked
description: "Configure Go TLS servers and clients with crypto/tls: minimum versions, mutual TLS, custom CA pools, hot certificate rotation, and why InsecureSkipVerify is wrong."
sources: ["https://pkg.go.dev/crypto/tls", "https://pkg.go.dev/crypto/x509", "https://pkg.go.dev/golang.org/x/crypto/acme/autocert", "https://go.dev/doc/go1.24#cryptotlspkgcryptotls"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# TLS servers and clients with crypto/tls

**Goal:** correct, modern TLS on both ends, including mTLS between services and certificates that
rotate without restarts.

## Server
```go
srv := &http.Server{
    Addr: ":8443",
    TLSConfig: &tls.Config{
        MinVersion: tls.VersionTLS12,  // the default minimum is already TLS 1.2; TLS 1.3 is negotiated when both sides support it
    },
    ReadHeaderTimeout: 10 * time.Second,
}
log.Fatal(srv.ListenAndServeTLS("server.crt", "server.key"))
```
- Go's defaults are good: cipher suites for TLS 1.3 are not configurable, and the TLS 1.2 default
  list excludes weak suites. Do not hand-craft `CipherSuites` unless a compliance profile demands it.
- If the certificate is signed by a CA, `server.crt` should be the concatenation of the server's certificate, any intermediates and the CA's certificate (see the `ListenAndServeTLS` documentation).
- Go 1.24 enables the hybrid post-quantum key exchange X25519MLKEM768 by default; `GODEBUG=tlsmlkem=0` reverts the default (or set `CurvePreferences`) if a middlebox breaks.

## Hot rotation
```go
var cert atomic.Pointer[tls.Certificate]
reload := func() error {
    c, err := tls.LoadX509KeyPair(crtPath, keyPath)
    if err == nil { cert.Store(&c) }
    return err
}
cfg := &tls.Config{GetCertificate: func(*tls.ClientHelloInfo) (*tls.Certificate, error) {
    return cert.Load(), nil
}}
// call reload() on SIGHUP or a file watcher (cert-manager renews files in place)
```
Public endpoints: `autocert.Manager{Prompt: autocert.AcceptTOS, HostPolicy: autocert.HostWhitelist("example.com"), Cache: autocert.DirCache("certs")}` and `TLSConfig: m.TLSConfig()`.

## Client with a private CA
```go
pool, _ := x509.SystemCertPool()              // or x509.NewCertPool() to trust ONLY your CA
pool.AppendCertsFromPEM(caPEM)
tr := http.DefaultTransport.(*http.Transport).Clone()
tr.TLSClientConfig = &tls.Config{RootCAs: pool, MinVersion: tls.VersionTLS12}
client := &http.Client{Transport: tr, Timeout: 15 * time.Second}
```
`InsecureSkipVerify: true` disables all server authentication and makes the connection
man-in-the-middle-able. For tests use `httptest.NewTLSServer` and its `ts.Client()`, which trusts
the test cert.

## Mutual TLS
Server:
```go
cfg := &tls.Config{
    ClientAuth: tls.RequireAndVerifyClientCert,
    ClientCAs:  clientCAPool,
    MinVersion: tls.VersionTLS13,
}
// in handler: r.TLS.PeerCertificates[0].Subject.CommonName or URIs (SPIFFE IDs)
```
Client: `Certificates: []tls.Certificate{clientCert}` (or `GetClientCertificate` for rotation).
Authorise on identity (SAN URI/DNS) after verification; verification alone only proves the CA
issued it.

## Debugging
- `SSLKEYLOGFILE` style: set `tls.Config.KeyLogWriter` (dev only) to decrypt in Wireshark.
- Errors: `x509: certificate signed by unknown authority` (missing intermediate or CA),
  `certificate is valid for X, not Y` (SAN mismatch; certificates that rely on the legacy Common Name field are rejected, so use SANs).

## Verify
- [ ] A client restricted to TLS 1.1 is refused.
- [ ] Certificate swap on disk is picked up without restart.
- [ ] mTLS rejects a client cert from another CA.
- [ ] No `InsecureSkipVerify` in non-test code (`grep -r InsecureSkipVerify`).

## Checked

2026-10-25. Checked against the Go source and release notes (crypto/tls `Config`: default `MinVersion` TLS 1.2 and maximum TLS 1.3, TLS 1.3 cipher suites not configurable, `KeyLogWriter` is for debugging only, `ClientAuth` with `RequireAndVerifyClientCert`, `GetClientCertificate`; crypto/x509 legacy Common Name rejection and `SystemCertPool`; net/http `ListenAndServeTLS` certificate file layout; `httptest.NewTLSServer` and `Server.Client`; Go 1.24 notes on X25519MLKEM768 and `GODEBUG=tlsmlkem=0`) and golang.org/x/crypto autocert (`Manager`, `AcceptTOS`, `HostWhitelist`, `DirCache`, `TLSConfig`). Corrected the certificate-file wording and the Common Name remark; removed unconfirmed third-party tool commands.

Method: documentation only; no commands were run.
