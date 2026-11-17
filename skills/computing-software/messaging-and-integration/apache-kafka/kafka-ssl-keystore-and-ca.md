---
id: computing-software.messaging-and-integration.apache-kafka.kafka-ssl-keystore-and-ca
name: kafka-ssl-keystore-and-ca
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, ssl, keytool, openssl-ca, truststore]
level: advanced
status: docs-checked
description: "Create broker keypairs with keytool (PKCS12), a private CA with openssl, and keystores/truststores for Kafka SSL."
sources:
  - https://kafka.apache.org/42/security/encryption-and-authentication-using-ssl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build the key material for SSL listeners. SSL is disabled by default.

1. Generate a keypair per broker, ideally on that broker so the key never leaves it, using PKCS12 explicitly (the default as of Java 9; JKS is deprecated):
`keytool -keystore server.keystore.jks -alias localhost -validity {validity} -genkey -keyalg RSA -destkeystoretype pkcs12 -ext SAN=DNS:{FQDN},IP:{IPADDRESS1}`
The key's validity differs from the certificate validity set at signing; one key can get several certificates over time.

2. Create a CA. Because of an OpenSSL bug the x509 module does not copy SAN extensions from CSRs, so use the `ca` module with an openssl-ca.cnf containing `copy_extensions = copy`, create `serial.txt` (`echo 01 > serial.txt`) and `index.txt`, then:
`openssl req -x509 -config openssl-ca.cnf -newkey rsa:4096 -sha256 -nodes -out cacert.pem -outform PEM`
Guard the CA key: whoever holds it can issue trusted certificates.

3. Trust the CA: `keytool -keystore client.truststore.jks -alias CARoot -import -file ca-cert`. Brokers need a truststore with the client CAs too when `ssl.client.auth` is requested or required.

4. Sign: `openssl ca -config openssl-ca.cnf -policy signing_policy -extensions signing_req -out {server certificate} -infiles {csr}`, then import the CA certificate (alias CARoot) and the signed certificate (alias localhost) into the keystore.

PEM alternative (2.7.0+): set `ssl.keystore.key` and `ssl.keystore.certificate.chain` directly; use `ssl.key.password` for encrypted keys.

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/security/encryption-and-authentication-using-ssl/ (key generation, CA, signing and PEM sections read)
