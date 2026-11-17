---
id: computing-software.cryptography-implementation.crypto-libraries.go-tls-getcertificate-and-autocert
name: go-tls-getcertificate-and-autocert
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, getcertificate, golang, crypto-tls, autocert, acme, certificate-reload]
level: practitioner
status: verified
description: "Serve rotating certificates in Go with tls.Config.GetCertificate: hot reload from disk, per-SNI selection, autocert for ACME, and caching to avoid per-handshake I/O."
sources: ["https://pkg.go.dev/crypto/tls#Config", "https://pkg.go.dev/golang.org/x/crypto/acme/autocert"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GetCertificate hot reload and autocert

## Hot reload
```go
type certStore struct{ v atomic.Pointer[tls.Certificate] }

func (s *certStore) load(certFile, keyFile string) error {
    c, err := tls.LoadX509KeyPair(certFile, keyFile)
    if err != nil { return err }                 // keep serving the old cert on error
    s.v.Store(&c); return nil
}
store := &certStore{}
_ = store.load("tls.crt", "tls.key")
// reload on SIGHUP or a file watcher / ticker
srv := &http.Server{Addr: ":443", TLSConfig: &tls.Config{
    MinVersion: tls.VersionTLS12,
    GetCertificate: func(*tls.ClientHelloInfo) (*tls.Certificate, error) { return store.v.Load(), nil },
}}
srv.ListenAndServeTLS("", "")
```
- `ClientHelloInfo.ServerName` allows per-SNI selection; `hello.SupportsCertificate(c)` picks between RSA and
  ECDSA certificates.
- Do not read files inside GetCertificate on every handshake.

## autocert
```go
m := &autocert.Manager{Prompt: autocert.AcceptTOS, HostPolicy: autocert.HostWhitelist("example.com"),
    Cache: autocert.DirCache("/var/lib/acme")}
srv := &http.Server{Addr: ":443", TLSConfig: m.TLSConfig()}
go http.ListenAndServe(":80", m.HTTPHandler(nil))
```
- Always set `HostPolicy`; the `autocert.Manager` docs say that with nil `HostPolicy` clients connecting by IP address
  with a wrong host name can drive the Manager into the CA's rate limit.
- Persist `Cache`: the docs say a persistent cache such as `DirCache` is strongly recommended, and with a nil `Cache`
  certificates are kept only for the Manager's lifetime. `RenewBefore` defaults to the lesser of 30 days or 1/3 of the
  lifetime.
- Verified: a Manager with `HostWhitelist`, `DirCache`, `TLSConfig()` and `HTTPHandler(nil)` builds and runs against
  `golang.org/x/crypto` v0.58.0 on Go 1.27.3 (no ACME order was placed).
- For clusters use a shared cache or a dedicated ACME client (cert-manager, Caddy).

## Verify
- [ ] Replace cert files, trigger reload, `openssl s_client` shows new serial without restart.
