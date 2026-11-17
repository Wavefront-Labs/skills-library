---
id: computing-software.data-engineering.apache-kafka.delegation-tokens
name: delegation-tokens
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-security, delegation-tokens, sasl-scram, kerberos, token-renewal]
level: advanced
status: docs-checked
description: "Use Kafka delegation tokens to give short-lived credentials to distributed jobs (Spark, Flink) without shipping keytabs or certs: create, renew, expire, and configure SCRAM auth."
sources:
  - https://kafka.apache.org/documentation/#security_delegation_token
  - https://github.com/apache/kafka/blob/trunk/docs/security/authentication-using-sasl.md
  - https://github.com/apache/kafka/blob/trunk/server-common/src/main/java/org/apache/kafka/server/config/DelegationTokenManagerConfigs.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delegation tokens

**Use when:** a framework launches many short-lived workers (Spark executors, Flink TaskManagers, MapReduce) and you do not want to distribute Kerberos keytabs or TLS keys to every one. The driver, authenticated with strong credentials, obtains a token and hands it out; workers authenticate with SASL/SCRAM using the token.

## Broker setup
```properties
delegation.token.secret.key=<long random secret, same on all brokers and controllers>
delegation.token.max.lifetime.ms=604800000      # default: 7 days hard cap
delegation.token.expiry.time.ms=86400000        # default: renew every 24 h
sasl.enabled.mechanisms=GSSAPI,SCRAM-SHA-512    # SCRAM must be enabled on the listener
```
Token details are stored with the other metadata on the controller nodes; the secret key sits in plain text in `server.properties`, so use this when controllers sit on a private network or broker-controller traffic is encrypted. Without the secret key, token authentication and API operations fail. Rotating the secret needs expiring all tokens, a rolling restart, then new tokens.

## Lifecycle
```bash
kafka-delegation-tokens.sh --bootstrap-server $BS --command-config admin.properties \
  --create --max-life-time-period -1 --renewer-principal User:renewer-app
# prints TOKENID and HMAC
kafka-delegation-tokens.sh --bootstrap-server $BS --command-config admin.properties --renew --renew-time-period -1 --hmac <HMAC>
kafka-delegation-tokens.sh --bootstrap-server $BS --command-config admin.properties --expire --expiry-time-period -1 --hmac <HMAC>
kafka-delegation-tokens.sh --bootstrap-server $BS --command-config admin.properties --describe
```
- Token requests (create, renew, expire, describe) must use SASL or SSL authenticated channels, and a connection that itself authenticated with a token cannot request tokens.
- `--owner-principal` creates a token for another owner. Owners and renewers can renew or expire tokens and always describe their own; describing others needs the DESCRIBE_TOKEN permission on the owner's User resource. The token owner is the principal used for ACL checks.

## Client config using a token
```properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
  username="<TOKENID>" password="<HMAC>" tokenauth="true";
```

## Verify
- [ ] Workers connect with the token id and HMAC and no keytab present.
- [ ] Expired token: clients fail auth (renewal works in long jobs).

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: config names `delegation.token.secret.key`, `delegation.token.max.lifetime.ms`, `delegation.token.expiry.time.ms` and their defaults (24 h renewal, 7 days maximum), `kafka-delegation-tokens.sh` create/renew/expire/describe options, `--owner-principal`, the DESCRIBE_TOKEN rule, no token-from-token requests, SCRAM-based authentication with `tokenauth="true"`, and the manual secret-rotation procedure. Removed: the old `delegation.token.master.key` name, the unconfirmed 3.3 and 3.6 version gates and the Spark and Flink bullets (their documentation did not mention Kafka tokens where checked).

Method: documentation only; no commands were run.
