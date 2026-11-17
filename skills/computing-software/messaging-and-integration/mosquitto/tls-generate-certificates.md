---
id: computing-software.messaging-and-integration.mosquitto.tls-generate-certificates
name: tls-generate-certificates
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [tls, openssl, certificate-authority, csr, mosquitto-tls]
level: practitioner
status: docs-checked
description: "Generate a CA, server and client certificate with the openssl commands from the mosquitto-tls man page."
sources:
  - https://mosquitto.org/man/mosquitto-tls-7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: produce the files needed for Mosquitto TLS.

Certificate authority:
```
openssl req -new -x509 -days <duration> -extensions v3_ca -keyout ca.key -out ca.crt
```

Server:
```
openssl genrsa -aes256 -out server.key 2048
openssl req -out server.csr -key server.key -new
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days <duration>
```

When prompted for the CN (Common Name) on the server CSR, enter the server or broker hostname or domain name. The CSR can instead be sent to a CA.

Client: the same three steps with `client.key`, `client.csr` and `client.crt`:
```
openssl genrsa -aes256 -out client.key 2048
openssl req -out client.csr -key client.key -new
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days <duration>
```

Important note on the page: use different certificate subject parameters for your CA, server and clients. If the certificates appear identical, even though generated separately, the broker or client cannot distinguish between them and you get difficult to diagnose errors.

The page says the commands are given without context and points to an asciicast walkthrough. The resulting files map to the listener options `cafile`, `certfile` and `keyfile`.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto-tls(7); all commands and the different-subject note match the page. Claims unchanged; the closing mapping to cafile, certfile and keyfile is the skill's own inference, not stated on this page.
