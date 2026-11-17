---
id: computing-software.messaging-and-integration.apache-pulsar.tls-transport-encryption
name: tls-transport-encryption
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [tls, mtls, transport-encryption, hostname-verification, pem, tls-trust-certs-file-path]
level: practitioner
status: docs-checked
description: "Configure Pulsar TLS with PEM: broker, proxy and client settings, mTLS flag, protocol and cipher keys, hostname verification defaults, and key format rules."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/security-tls-transport.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt client, proxy and broker traffic, optionally with mutual TLS.

By default clients talk to Pulsar in plain text. PEM is the recommended certificate format; JKS KeyStore is optional. TLS adds overhead.

Certificates: a CA signs server and client certificates; keep the CA private key with the CA and distribute only its public certificate (trust cert). The page example makes the CA with `openssl genrsa -out ca.key.pem 2048` and `openssl req -x509 -new -nodes -key ca.key.pem -subj "/CN=CARoot" -days 365 -out ca.cert.pem`, then signs server and client requests. Server certificates need SANs (`alt_names`) matching the hostnames clients use. Convert the server key to PKCS#8 with `openssl pkcs8 -topk8 -inform PEM -outform PEM -in server.key.pem -out server.key-pk8.pem -nocrypt`. The PEM reader accepts unencrypted PKCS#8, PKCS#1 RSA and SEC1 EC keys (SEC1 needs Bouncy Castle `bcpkix`).

Broker:
```properties
brokerServicePortTls=6651
webServicePortTls=8081
tlsTrustCertsFilePath=/path/to/ca.cert.pem
tlsCertificateFilePath=/path/to/server.cert.pem
tlsKeyFilePath=/path/to/server.key-pk8.pem
tlsRequireTrustedClientCertOnConnect=true   # mTLS
brokerClientTlsEnabled=true                 # internal client
tlsProtocols=TLSv1.3,TLSv1.2
```
`tlsCiphers` selects suites; unset uses provider defaults. Proxy: `servicePortTls`, `webServicePortTls`, the same three cert keys, `tlsRequireTrustedClientCertOnConnect`, and `tlsEnabledWithBroker=true`.

Clients use `pulsar+ssl://host:6651/` and `https://` for the web service, with `tlsTrustCertsFilePath` (plus `tlsKeyFilePath` and `tlsCertificateFilePath` for mTLS). CLI tools use `webServiceUrl=https://...` and `brokerServiceUrl=pulsar+ssl://...` in client.conf.

Hostname verification is enabled by default: `enableTlsHostnameVerification(true)` (Java builder), `tlsHostnameVerificationEnable=true` (client.conf), `tlsHostnameVerificationEnabled=true` (broker/proxy/WebSocket), `tlsEnableHostnameVerification: true` (Functions worker). Keep `allowTlsInsecureConnection(false)` and `tlsAllowInsecureConnection=false` so untrusted certificates are rejected; trust and hostname checks are separate.

Verify: connect over pulsar+ssl with the right CA, then with a mismatched hostname and confirm failure.

## Checked

Method: docs-checked 2026-11-09 against pulsar-site docs/security-tls-transport.md (read in full)
