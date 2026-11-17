---
id: computing-software.cryptography-implementation.crypto-libraries.tokio-rustls-and-hyper-tls
name: tokio-rustls-and-hyper-tls
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, tokio-rustls, rustls, hyper, tokio, rust, alpn]
level: advanced
status: draft
description: "Wire rustls into async Rust with tokio-rustls and hyper: TlsAcceptor and TlsConnector setup, ALPN for HTTP/2, root stores, certificate reload, and handshake timeouts."
sources: ["https://docs.rs/tokio-rustls/latest/tokio_rustls/", "https://docs.rs/hyper-rustls/latest/hyper_rustls/", "https://docs.rs/rustls/latest/rustls/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# tokio-rustls and hyper TLS integration

## Server
```rust
let certs = CertificateDer::pem_file_iter("tls.crt")?.collect::<Result<Vec<_>, _>>()?;
let key = PrivateKeyDer::from_pem_file("tls.key")?;
let mut cfg = rustls::ServerConfig::builder().with_no_client_auth().with_single_cert(certs, key)?;
cfg.alpn_protocols = vec![b"h2".to_vec(), b"http/1.1".to_vec()];
let acceptor = tokio_rustls::TlsAcceptor::from(Arc::new(cfg));
loop {
    let (tcp, _) = listener.accept().await?;
    let acceptor = acceptor.clone();
    tokio::spawn(async move {
        let tls = match tokio::time::timeout(Duration::from_secs(10), acceptor.accept(tcp)).await {
            Ok(Ok(s)) => s, _ => return,                // slow or failed handshake
        };
        // hand `tls` to hyper_util::server::conn::auto::Builder
    });
}
```
(PEM helpers come from `rustls-pki-types`.)

## Client with hyper
```rust
let https = hyper_rustls::HttpsConnectorBuilder::new()
    .with_platform_verifier()      // or .with_webpki_roots()
    .https_only().enable_http1().enable_http2().build();
let client = hyper_util::client::legacy::Client::builder(TokioExecutor::new()).build(https);
```

## Notes
- Pick a crypto provider (aws-lc-rs default, or ring) once at startup:
  `rustls::crypto::aws_lc_rs::default_provider().install_default()` when features are ambiguous.
- Certificate reload: implement `ResolvesServerCert` returning an `Arc<CertifiedKey>` swapped atomically.
- Always time out handshakes; otherwise idle sockets accumulate.

## Verify
- [ ] `curl --http2 -v https://localhost:8443` shows ALPN h2; handshake timeout test closes idle sockets.
