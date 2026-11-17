---
id: computing-software.messaging-and-integration.redpanda.enable-sasl-authentication-and-superusers
name: enable-sasl-authentication-and-superusers
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [sasl, authentication, superusers, enable-sasl, authentication-method, kafka-enable-authorization]
level: practitioner
status: docs-checked
description: "Turn on Redpanda authentication safely: create a superuser first, choose enable_sasl or per-listener authentication_method, and avoid mixing the two approaches."
sources:
  - https://docs.redpanda.com/streaming/current/manage/security/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Terms: a **user** is a stored credential (for example from `rpk security user create`), a **principal** is the authenticated identity string used for ACLs and superuser assignment, and a **superuser** is a principal with unrestricted access. ACLs go to principals; a user with no granted principal has no access. SASL users need the `User:` prefix; OIDC principals use the value extracted from the token claims per your principal mapping (for example the `sub` claim), with no prefix.

**Create a superuser first.** Enabling authentication can implicitly enable authorization, and without a superuser you are locked out of managing the cluster.

```bash
rpk cluster config set superusers '["superuser-username"]'
rpk security user create <superuser-username> \
  -p '<superuser-password>' \
  --mechanism=<superuser-authentication-mechanism>
```
Valid mechanisms are `SCRAM-SHA-256` and `SCRAM-SHA-512`. Setting `superusers` does not create the user. Do not use the superuser for routine work and do not delete it, or someone could recreate it with another password. Edit the list with `rpk cluster config edit`.

**Option 1: `enable_sasl`** (legacy but supported; uniform SASL on all Kafka listeners, no restart):

```bash
rpk cluster config set enable_sasl true
```
It implicitly sets `kafka_enable_authorization` to true; do not also add `authentication_method: sasl`.

**Option 2: per listener** (recommended for new clusters; needs `redpanda.yaml` edits and a restart):

```bash
rpk cluster config set kafka_enable_authorization true
```
```yaml
redpanda:
  kafka_api:
    - address: 0.0.0.0
      port: 9092
      name: internal
      authentication_method: none  # No authentication for internal traffic
    - address: 0.0.0.0
      port: 9093
      name: external
      authentication_method: sasl  # SASL for external traffic
```

Do not combine the two; the page warns it can cause inconsistencies and initialization failures. Supported Kafka API methods include SASL/SCRAM, PLAIN, OAUTHBEARER (OIDC), GSSAPI (Kerberos) and mTLS; the Admin API, HTTP Proxy and Schema Registry use basic authentication or OIDC.

## Checked

The terminology, superuser steps, both enablement options and the warning were confirmed in the Enable authentication sections of the Authentication page.

Method: docs-checked 2026-11-09 against the Redpanda Authentication page (sections up to SASL/SCRAM, plus the HTTP API sections, read); no commands were run.
