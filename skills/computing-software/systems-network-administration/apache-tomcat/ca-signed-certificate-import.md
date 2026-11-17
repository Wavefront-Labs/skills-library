---
id: computing-software.systems-network-administration.apache-tomcat.ca-signed-certificate-import
name: ca-signed-certificate-import
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, csr, certificate-signing-request, keytool, certificate-chain, ca-certificate, keystore, ssl-howto]
level: practitioner
status: docs-checked
description: "Get a CA-signed certificate into a Tomcat 10.1 keystore: generate the key, create a CSR with keytool, import the chain first and then the server certificate under the same alias."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/ssl-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CA-signed certificate with keytool

1. Create the key entry (self-signed placeholder). The docs note some CAs want the domain in the "first and last name" field:
```
keytool -genkey -alias tomcat -keyalg RSA -keystore <keystore_file>
```
2. Create the CSR and send it to the CA:
```
keytool -certreq -keyalg RSA -alias tomcat -file certreq.csr -keystore <keystore_file>
```
3. Import the chain/root certificate first:
```
keytool -import -alias root -keystore <keystore_file> -trustcacerts -file <chain_certificate>
```
4. Import the issued certificate under the same alias as the key (`tomcat`):
```
keytool -import -alias tomcat -keystore <keystore_file> -file <your_certificate>
```

Notes:
- Import the chain or root certificate into the keystore first, then your own certificate. Download the chain certificate from the CA that issued yours.
- Each CA differs slightly (information required, certificate and chain formats) and issuing rules change over time, so the commands may need to be modified.
- If more than one key is in the keystore, configure `certificateKeyAlias` on the `<Certificate>` so the correct key is used.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 SSL/TLS how-to (CSR and Importing the Certificate sections; certificateKeyAlias from the HTTP Connector reference). Removed the path-building rationale and the generic verify line.

Method: documentation only; no commands were run.
