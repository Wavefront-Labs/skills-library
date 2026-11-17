---
id: computing-software.messaging-and-integration.apache-kafka.kafka-delegation-tokens
name: kafka-delegation-tokens
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, delegation-tokens, kafka-delegation-tokens-sh, kip-48]
level: advanced
status: docs-checked
description: "Use delegation tokens as shared secrets so processing workers authenticate without Kerberos keytabs or keystores."
sources:
  - https://kafka.apache.org/42/security/authentication-using-sasl/
  - https://kafka.apache.org/42/security/authorization-and-acls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let frameworks distribute work to workers securely, without distributing Kerberos TGT/keytabs or keystores for two-way SSL (KIP-48).

Delegation tokens are lightweight shared secrets between brokers and clients that complement SASL and SSL authentication. Under the default `principal.builder.class`, the token owner is the authenticated principal used for ACLs.

Typical flow:
1. A user authenticates to the cluster via SASL or SSL and obtains a delegation token, using the Admin API or the `kafka-delegation-tokens.sh` script.
2. The user passes the token securely to Kafka clients, which use it to authenticate.
3. The token owner or renewer can renew or expire the token.

Authorization: the DelegationToken ACL resource protects actions such as describing tokens (`kafka-acls.sh --delegation-token`), and the `CreateTokens` and `DescribeTokens` operations can be granted on User resources so one principal can create and describe tokens for other users (KIP-373). Read KIP-48 for the special behaviour of these objects.

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/security/authentication-using-sasl/ (delegation tokens section) and kafka.apache.org/42/security/authorization-and-acls/ (DelegationToken and User resource notes); added to sources
