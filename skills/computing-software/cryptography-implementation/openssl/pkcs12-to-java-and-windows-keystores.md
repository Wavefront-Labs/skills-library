---
id: computing-software.cryptography-implementation.openssl.pkcs12-to-java-and-windows-keystores
name: pkcs12-to-java-and-windows-keystores
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, pkcs12, pfx, keystore-conversion, java-keystore, keytool, jks, windows-cert-store]
level: practitioner
status: draft
description: "Convert between PKCS#12, JKS and Windows certificate stores: keytool -importkeystore, aliases and passwords, Java truststores from PEM, and Import-PfxCertificate."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/keytool.html", "https://docs.openssl.org/master/man1/openssl-pkcs12/", "https://learn.microsoft.com/en-us/powershell/module/pki/import-pfxcertificate"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PKCS#12 to Java and Windows keystores

## Java: keep PKCS#12 as the store format
PKCS#12 is the default keystore type since JDK 9; JKS is proprietary and weaker. Most JVM
servers (Tomcat, Spring Boot, Kafka, Elasticsearch) take a `.p12` directly:
```
server.ssl.key-store=classpath:api.p12
server.ssl.key-store-type=PKCS12
server.ssl.key-store-password=${KEYSTORE_PASSWORD}
server.ssl.key-alias=api
```

## Convert JKS <-> PKCS#12
```
keytool -importkeystore -srckeystore old.jks -srcstoretype JKS \
  -destkeystore new.p12 -deststoretype PKCS12
keytool -importkeystore -srckeystore api.p12 -srcstoretype PKCS12 \
  -destkeystore api.jks -deststoretype JKS -srcalias "api.example.com 2026-10" -destalias api
keytool -list -v -keystore new.p12 -storetype PKCS12 | grep -E "Alias|Entry type|Owner|Valid"
```
- The alias comes from the PFX friendlyName (lower-cased by keytool); check with `-list` and
  pass `-srcalias` when there are several.
- keytool expects the key password to equal the store password for PKCS#12; mismatched
  passwords from other tools give `Get Key failed: Given final block not properly padded`.

## Truststores (certs only)
```
keytool -importcert -noprompt -alias corp-root -file root.pem \
  -keystore truststore.p12 -storetype PKCS12 -storepass:env TS_PASS
```
A certs-only PKCS#12 made by OpenSSL is read by Java as having no trusted entries, because Java
looks for its own trusted-key-usage attribute. Use keytool, or OpenSSL 3.2+:
`openssl pkcs12 -export -nokeys -in root.pem -jdktrust anyExtendedKeyUsage -out ts.p12`.

To trust a private CA JVM-wide instead: `keytool -importcert -cacerts -alias corp-root -file root.pem`
(changes the JDK's `cacerts`; redo after every JDK upgrade, or bake into the image).

## Windows certificate store
```powershell
$pw = Read-Host -AsSecureString
Import-PfxCertificate -FilePath .\api.pfx -CertStoreLocation Cert:\LocalMachine\My -Password $pw
# non-interactive: certutil -f -p <password> -importpfx My api.pfx NoExport
Get-ChildItem Cert:\LocalMachine\My | Where-Object Subject -like "*api.example.com*"
```
- Omit `-Exportable` (PowerShell) or pass `NoExport` (certutil) so the key cannot be exported
  again.
- IIS/HTTP.sys services also need the private key ACL to allow the app pool identity
  (`certlm.msc` > Manage Private Keys).
- Export: `Export-PfxCertificate -Cert $c -FilePath out.pfx -Password $pw -ChainOption BuildChain`.

## Gotchas
- Store passwords in a secrets manager; `-storepass:env VAR` and `:file` avoid argv exposure.
- Java `SSLHandshakeException: PKIX path building failed` = missing trust anchor, not a keystore format issue.
- Converting does not change key strength; a 1024-bit key is still 1024 bits after import.

## Verify
- [ ] `keytool -list -v` shows `PrivateKeyEntry` with the full chain length you expect.
- [ ] Truststore lists `trustedCertEntry` items.
- [ ] Windows store entry shows "You have a private key" and is non-exportable where intended.
