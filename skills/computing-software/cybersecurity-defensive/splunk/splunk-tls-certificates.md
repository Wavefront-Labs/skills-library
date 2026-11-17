---
id: computing-software.cybersecurity-defensive.splunk.splunk-tls-certificates
name: splunk-tls-certificates
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-architecture, splunk-tls-certificates, server-conf, outputs-conf, forwarder-tls, splunk-web-ssl, certificate-rotation, mtls]
level: advanced
status: draft
description: "Replace Splunk default certificates: splunkd, Splunk Web and forwarder-to-indexer TLS with your own CA, sslVerifyServerCert, mutual TLS, and safe rotation."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Security/AboutsecuringyourSplunkconfigurationwithSSL", "https://docs.splunk.com/Documentation/Splunk/latest/Security/ConfigureSplunkforwardingtousesignedcertificates", "https://docs.splunk.com/Documentation/Splunk/latest/Security/Securingyourdeploymentserverandclients"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TLS certificates for Splunk

Out of the box every Splunk instance uses a certificate signed by the same Splunk-shipped CA.
Anyone with a Splunk install can impersonate your indexers or forwarders. Replace it.

## Build the PEM files
Splunk wants the server certificate, private key and chain in one PEM (cert, then key, then
intermediate, then root):
```
cat idx01.crt idx01.key intermediate.crt root.crt > idx01-combined.pem
```
Encrypted key is supported with `sslPassword`. Separate CA file for verification: `cacert.pem`.

## Forwarder to indexer (port 9997)
Indexer inputs.conf:
```
[splunktcp-ssl:9997]
disabled = 0
[SSL]
serverCert = $SPLUNK_HOME/etc/auth/mycerts/idx01-combined.pem
sslPassword = <key password>
requireClientCert = true
sslVersions = tls1.2
```
Forwarder outputs.conf:
```
[tcpout:primary]
server = idx01.example.com:9997, idx02.example.com:9997
clientCert = $SPLUNK_HOME/etc/auth/mycerts/uf-combined.pem
sslVerifyServerCert = true
sslCommonNameToCheck = idx01.example.com, idx02.example.com
```
server.conf `[sslConfig] sslRootCAPath = $SPLUNK_HOME/etc/auth/mycerts/cacert.pem` on both sides.

## splunkd management port (8089) and Splunk Web (8000)
server.conf `[sslConfig] serverCert = ...`, `sslRootCAPath = ...`; to verify peers set
`sslVerifyServerCert = true` and `sslVerifyServerName = true` (9.x).
web.conf:
```
[settings]
enableSplunkWebSSL = true
serverCert = $SPLUNK_HOME/etc/auth/mycerts/web.pem
privKeyPath = $SPLUNK_HOME/etc/auth/mycerts/web.key
```

## Rotation without an outage
1. Issue new certs from the same CA (or add the new CA to `sslRootCAPath` everywhere first).
2. Roll indexers one at a time (cluster: rolling restart), then forwarders via deployment server app.
3. Only then remove the old CA from trust stores.
Track expiry: `splunk cmd openssl x509 -enddate -noout -in <pem>`; alert 30 days ahead.

## Gotchas
- Order inside the combined PEM matters; wrong order gives "unable to load certificate".
- `sslCommonNameToCheck` must match CN or SAN exactly; wildcards depend on version.
- Deployment server clients talk on 8089; if you enforce verification there, every UF needs the CA.
- Splunk Cloud manages its side; you install the Splunk Cloud forwarder credentials app instead.

## Verify
- `openssl s_client -connect idx01:9997 -cert uf.crt -key uf.key -CAfile cacert.pem` handshakes.
- `index=_internal sourcetype=splunkd component=TcpOutputProc (ssl OR certificate) log_level=ERROR` is empty.
- `index=_internal source=*metrics.log group=tcpin_connections ssl=true` lists your forwarders.
