---
id: computing-software.systems-network-administration.apache-tomcat.keystore-creation-keytool
name: keystore-creation-keytool
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, keystore, keytool, pkcs12, jks, openssl, self-signed-certificate, ssl-howto]
level: practitioner
status: docs-checked
description: "Create a Java keystore for Tomcat 10.1 with keytool, convert existing PEM key and cert to PKCS12 with openssl, and know the default keystore location and formats."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/ssl-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Create a keystore for Tomcat

Self-signed keystore (Unix; Windows uses `"%JAVA_HOME%\bin\keytool"`):
```
$JAVA_HOME/bin/keytool -genkey -alias tomcat -keyalg RSA -keystore /path/to/my/keystore
```
- Without `-keystore` the file is `~/.keystore` in the running user's home.
- The default keystore password used by Tomcat is `changeit` (lower case); you can choose a custom one but must then give it in server.xml. Passwords are case sensitive. Pressing ENTER at the key-password prompt uses the keystore password for the key; a different key password must also be given in server.xml.
- keytool asks for company and contact fields; users see them, so make them accurate.
- Formats: `JKS`, `PKCS11`, `PKCS12`. Use RSA for compatibility. Avoid aliases that differ only by case.

Existing PEM certificate and key to PKCS12:
```
openssl pkcs12 -export -in mycert.crt -inkey mykey.key \
  -out mycert.p12 -name tomcat -CAfile myCA.crt -caname root -chain
```
Then point the `<Certificate>` element's `certificateKeystoreFile` at the new file.

If you import PEM into a JKS with keytool, delete any OpenSSL comment lines before the key data; keytool rejects them.

Next: wire it into server.xml (`computing-software.systems-network-administration.apache-tomcat.tls-connector-jsse-setup`) or get a CA-signed cert (`...ca-signed-certificate-import`).

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 SSL/TLS how-to (Prepare the Certificate Keystore). Reworded the password notes, removed the certificateKeystoreType snippet and the generic verify line.

Method: documentation only; no commands were run.
