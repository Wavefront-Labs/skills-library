---
id: computing-software.data-engineering.druid.druid-enable-tls
name: druid-enable-tls
category: computing-software
field: data-engineering
product: druid
tags: [tls, https, jetty, keystore, enable-tls-port]
level: practitioner
status: docs-checked
description: "Turn on HTTPS for Druid services: Jetty key store, client certificates, internal TLS client setup and the HTTP-to-HTTPS migration order."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/tls-support.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Connectors

`druid.enablePlaintextPort` (HTTP, default true) and `druid.enableTlsPort` (HTTPS, default false). Both can be enabled but this is not recommended. Ports are `druid.plaintextPort` and `druid.tlsPort` per process; see each service's configuration for valid and default values. To go HTTPS-only set `druid.enablePlaintextPort=false` and `druid.enableTlsPort=true`.

## Jetty server (embedded web server) settings

Required: `druid.server.https.keyStorePath` (path or URL), `.keyStoreType`, `.certAlias`, `.keyStorePassword` (a password provider or string).
Optional: `.reloadSslContext` (default false; detect key store changes and reload), `.reloadSslContextSeconds` (default 60), `.forceApplyConfig` (default false; apply TLS configs even if an `SslContextFactory.Server` is already bound).

Client certificate authentication:
- `.requireClientCertificate` (default false): clients must present a certificate or connections fail.
- `.requestClientCertificate` (default false): certificate optional; ignored if `requireClientCertificate` is true. If both are false, the rest of this group is ignored.
- `.trustStorePath` (required only if `requireClientCertificate` is true), `.trustStoreType` and `.trustStoreAlgorithm` (JVM defaults), `.trustStorePassword`.
- `.validateHostnames` (default true): match client hostname to certificate CN/subjectAltNames.
- `.crlPath` (default null): static certificate revocation lists.

Advanced, use caution: `.keyManagerFactoryAlgorithm`, `.keyManagerPassword`, `.includeCipherSuites` / `.excludeCipherSuites` (exact name or regular expression; Jetty defaults), `.includeProtocols` / `.excludeProtocols` (exact names; Jetty defaults). Valid algorithm and suite names come from the Java Cryptography Architecture standard names for your JDK; the Jetty secure-protocols guide, the JSSE reference guide and the `SslContextFactory` reference help interpret the settings.

## Internal communication

Processes use HTTPS to talk to each other whenever possible. Druid's HttpClient needs an `SSLContext` that can validate server certificates, otherwise communication fails. By default Druid looks for an `SSLContext` Guice binding provided by an extension; the bundled simple-client-sslcontext extension covers simple cases, or write your own.

## Migrating clients to HTTPS

When Coordinator or Overlord have both HTTP and HTTPS enabled, a request to a non-leader is always redirected to the leader's HTTPS endpoint. Safe order: upgrade clients to follow HTTPS redirects, then upgrade and configure Coordinator/Overlord with both ports, then point clients at the HTTPS endpoint, then disable the HTTP port.

## Custom certificate checks

`druid.tls.certificateChecker` (default `"default"`) names a checker from an extension implementing `org.apache.druid.server.security.TLSCertificateChecker`. The default delegates to the standard trust manager with no extra checks. Non-default checkers have their own extension properties.

## Checked

2026-11-08. Read the cited TLS support page in full. Expanded the draft with all listed properties and defaults, client certificate options, internal TLS setup and the migration order.

Method: documentation only; no commands were run.
