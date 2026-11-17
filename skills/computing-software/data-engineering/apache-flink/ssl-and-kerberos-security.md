---
id: computing-software.data-engineering.apache-flink.ssl-and-kerberos-security
name: ssl-and-kerberos-security
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-ssl, kerberos, rest-api-security, internal-tls, delegation-tokens]
level: advanced
status: docs-checked
description: "Secure a Flink cluster: internal TLS between JobManager and TaskManagers, REST endpoint TLS and client auth, Kerberos keytabs and delegation tokens for HDFS/HBase."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/security/security-ssl/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/security/security-kerberos/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/security/security-delegation-token/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSL and Kerberos security

Flink's internal RPC (Pekko), blob server, data exchange and REST endpoint each have their own SSL switch; treat the REST port as sensitive because the REST API can submit jobs.

## Internal TLS (RPC, blob, data exchange)
```yaml
security.ssl.internal.enabled: true
security.ssl.internal.keystore: /etc/flink/tls/internal.keystore
security.ssl.internal.truststore: /etc/flink/tls/internal.truststore
security.ssl.internal.keystore-password: ${INTERNAL_KS_PW}
security.ssl.internal.key-password: ${INTERNAL_KEY_PW}
security.ssl.internal.truststore-password: ${INTERNAL_TS_PW}
```
- Internal connections are **mutually authenticated**; use a dedicated self-signed cert per cluster (the docs recommend one key pair shared by all cluster processes, trusted only by that cluster). Certificate pinning: `security.ssl.internal.cert.fingerprint`.
- Kubernetes operator: generate the keystore per deployment (cert-manager + init container) and mount it.
- `security.ssl.provider` selects the SSL engine: `JDK` (default) or `OPENSSL` (system libraries via netty-tcnative).

## REST endpoint TLS
```yaml
security.ssl.rest.enabled: true
security.ssl.rest.keystore: /etc/flink/tls/rest.keystore
security.ssl.rest.truststore: /etc/flink/tls/rest.truststore
security.ssl.rest.authentication-enabled: true      # require client certs (mTLS) for REST clients and CLI
```
Prefer mTLS for REST clients, and put the endpoint behind a reverse proxy/ingress with SSO and a cluster-internal Service.

## Kerberos
```yaml
security.kerberos.login.keytab: /etc/security/flink.keytab
security.kerberos.login.principal: flink/orders@CORP.EXAMPLE.COM
security.kerberos.login.contexts: Client,KafkaClient     # JAAS contexts
security.kerberos.login.use-ticket-cache: false
```
- With a keytab, Flink logs in and ships credentials so long-running jobs survive ticket expiry.
- Delegation token framework: `security.delegation.tokens.enabled`; providers such as HDFS and HBase obtain tokens on the JobManager and distribute them to TaskManagers (see the delegation token page for the full list and per-provider switches).

## Verify
- [ ] `openssl s_client` to the RPC/data ports fails without the internal cert; REST rejects clients without a cert when mTLS is on.
- [ ] Job runs past the Kerberos ticket lifetime without auth errors.

## Checked
2026-11-01: confirmed against the Flink SSL, Kerberos and delegation token security pages: internal and REST SSL switches, mutual authentication, self-signed guidance, cert fingerprint option, security.ssl.provider values JDK and OPENSSL, rest authentication-enabled, Kerberos login keytab/principal/contexts/use-ticket-cache, delegation tokens enabled option. Removed: web.submit.enable and web.cancel.enable, version gate, Kafka SASL properties, performance claims, remote code execution wording, Kafka delegation provider.
Method: documentation only; no commands were run.
