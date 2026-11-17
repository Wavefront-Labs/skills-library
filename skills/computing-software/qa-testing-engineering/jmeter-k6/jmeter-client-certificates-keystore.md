---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-client-certificates-keystore
name: jmeter-client-certificates-keystore
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter-keystore, mutual-tls, client-certificates, ssl-manager, keystore-config]
level: practitioner
status: docs-checked
description: "Load-test mTLS-protected services with JMeter: PKCS12/JKS keystores, javax.net.ssl properties, Keystore Configuration element for per-thread certs, and TLS troubleshooting."
sources:
  - https://jmeter.apache.org/usermanual/component_reference.html#Keystore_Configuration
  - https://jmeter.apache.org/usermanual/properties_reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client certificates and keystore configuration

## Single client certificate
```properties
# system.properties (or -D on the command line)
javax.net.ssl.keyStore=certs/client.jks
javax.net.ssl.keyStorePassword=<keystore-password>
# trust a private CA (if not in the JVM truststore)
javax.net.ssl.trustStore=certs/truststore.jks
javax.net.ssl.trustStorePassword=<truststore-password>
```
For a PKCS11 store set `javax.net.ssl.keyStoreType` to `PKCS11` and `javax.net.ssl.keyStore` to `NONE`.
```bash
jmeter -n -t plan.jmx -Djavax.net.ssl.keyStore=certs/client.jks -Djavax.net.ssl.keyStorePassword=$KS_PASS
```
Create the keystore with the Java `keytool` utility or your PKI; keys issued by a PKI must be imported into a format a Java key store accepts.

## Many certificates (one per virtual user)
Put multiple key entries in one keystore, then add **Keystore Configuration** (Config Element):
- Preload: true (usually the best option)
- Variable name holding certificate alias: e.g. `certAlias`, filled from a CSV Data Set
- Alias Start Index / End Index: 0-based; End Index defaults to -1, which loads all keys. When using the alias variable, make the range large enough that all keys are loaded at startup.
- To use more than one certificate, set `https.use.cached.ssl.context=false` in `jmeter.properties` or `user.properties` and use the HttpClient 4 implementation for the HTTP Request.

## TLS settings
```properties
https.default.protocol=TLS
https.use.cached.ssl.context=false
```
`https.default.protocol` is the default HTTPS protocol level (the shipped default is `TLS`); `https.socket.protocols` takes a space-separated protocol list for servers that need a specific one. `https.use.cached.ssl.context` is deprecated since JMeter 5.0 but must be false for multiple client certificates.

## Gotchas
- The HTTP Request must use the HttpClient 4 implementation for the Keystore Configuration element to apply.
- Passwords in property files end up in repos; pass them on the command line or from the CI secret store.

## Verify
Server access logs show the expected client cert subjects distributed across threads.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: the Keystore Configuration properties and its multi-certificate note, the javax.net.ssl system properties, PKCS11 settings, `https.use.cached.ssl.context` deprecation since 5.0, `https.default.protocol` and `https.socket.protocols`. Removed unconfirmed openssl, TLS debug and exception-mapping details.

Method: documentation only; no commands were run.
