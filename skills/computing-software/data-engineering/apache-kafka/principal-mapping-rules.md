---
id: computing-software.data-engineering.apache-kafka.principal-mapping-rules
name: principal-mapping-rules
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-security, principal-mapping, ssl-principal-mapping-rules, kerberos, kafka-acls, mtls]
level: advanced
status: docs-checked
description: "Map TLS certificate DNs and Kerberos principals to clean Kafka principals with ssl.principal.mapping.rules and sasl.kerberos.principal.to.local.rules so ACLs stay readable."
sources:
  - https://kafka.apache.org/documentation/#security_authz_ssl
  - https://github.com/apache/kafka/blob/trunk/docs/security/authorization-and-acls.md
  - https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/config/internals/BrokerSecurityConfigs.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Principal mapping rules

ACLs match on the principal string. Without mapping, an mTLS client is `User:CN=orders-svc,OU=Payments,O=Acme,L=London,C=GB` (full DN, exact order and spacing matter), and a Kerberos client is `User:orders-svc` only after default short-name mapping.

## TLS: ssl.principal.mapping.rules
```properties
ssl.principal.mapping.rules=RULE:^CN=([a-zA-Z0-9._-]+),OU=.*$/$1/L,RULE:^CN=([^,]+).*$/$1/,DEFAULT
```
- Rules are tried in order; first match wins and later rules are ignored. `RULE:<regex>/<replacement>/[L|U]` (L/U lower/upper-case the result). `DEFAULT` keeps the full distinguished name. The setting is ignored if a custom `principal.builder.class` is configured.
- The docs show names in the form `CN=writeuser,OU=Unknown,O=Unknown,L=Unknown,ST=Unknown,C=Unknown`. To see the exact string for a client, check the authorizer log (`kafka.authorizer.logger`) for the principal of a denied request.
- Commas inside an attribute value can break naive `[^,]+` patterns: test the regex against such a name.
- Inter-broker traffic over mTLS: broker certificates must map to a principal listed in `super.users` (semicolon-separated, because SSL names may contain commas).
- Broker configs can be prefixed per listener (`listener.name.<listener>.`); confirm in the Broker Configs table that this setting's update mode allows it.

## Kerberos: sasl.kerberos.principal.to.local.rules
```properties
sasl.kerberos.principal.to.local.rules=RULE:[1:$1@$0](.*@CORP.EXAMPLE.COM)s/@.*//,RULE:[2:$1@$0](.*@CORP.EXAMPLE.COM)s/@.*//,DEFAULT
```
- `[1:$1@$0]` forms a string from a one-component principal (`alice@REALM`) and `[2:$1@$0]` from a two-component one (`kafka/host@REALM`); the regex in parentheses then selects it and a sed-style `s/@.*//` strips the realm. The Kafka docs example is `RULE:[1:$1@$0](.*@MYDOMAIN.COM)s/@.*//,DEFAULT`.
- By default the SASL user name is the primary part of the Kerberos principal (`{username}/{hostname}@{REALM}` becomes `{username}`); keep `DEFAULT` after custom rules.
- If clients come from more than one realm, write an explicit rule per realm and test each.

## Custom builder
For anything rules cannot express, implement `KafkaPrincipalBuilder` and set `principal.builder.class`. In KRaft the class must implement `org.apache.kafka.common.security.auth.KafkaPrincipalSerde` so principals can be serialized for forwarding.

## Verify
- [ ] `kafka-acls.sh --list` principals match what the authorizer logs for test clients.
- [ ] A client with an unexpected DN is denied, not mapped to a privileged name by a loose regex.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: `ssl.principal.mapping.rules` grammar and first-match behaviour, the `L`/`U` suffix, the DEFAULT rule, the default DN form, the ignore-if-custom-builder note, `sasl.kerberos.principal.to.local.rules` example and default short-name behaviour, `principal.builder.class` with `KafkaPrincipalSerde` for KRaft, and the semicolon delimiter for `super.users`. Removed: the KIP-371 and 2.2 version gate, the SslTransportLayer DEBUG logger tip, the RFC 2253 claim, the unverified per-listener example and the multi-realm "do not match" detail.

Method: documentation only; no commands were run.
