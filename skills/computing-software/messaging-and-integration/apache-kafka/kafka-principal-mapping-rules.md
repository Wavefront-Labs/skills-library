---
id: computing-software.messaging-and-integration.apache-kafka.kafka-principal-mapping-rules
name: kafka-principal-mapping-rules
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, ssl-principal-mapping-rules, sasl-kerberos-principal-to-local-rules, principal-builder-class]
level: advanced
status: docs-checked
description: "Shorten SSL distinguished names and Kerberos principals into ACL principals with ssl.principal.mapping.rules and auth_to_local style rules."
sources:
  - https://kafka.apache.org/42/security/authorization-and-acls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control the principal name that ACLs match.

SSL: the default user name looks like `CN=writeuser,OU=Unknown,O=Unknown,L=Unknown,ST=Unknown,C=Unknown`. Set `ssl.principal.mapping.rules` to an ordered list of rules; the first match wins and later rules are ignored. Each rule is `RULE:pattern/replacement/` or `RULE:pattern/replacement/[LU]` where `/L` or `/U` forces lower or upper case. `DEFAULT` returns the full distinguished name. Example:
```
RULE:^CN=(.*?),OU=ServiceUsers.*$/$1/,
RULE:^CN=(.*?),OU=(.*?),O=(.*?),L=(.*?),ST=(.*?),C=(.*?)$/$1@$2/L,
RULE:^.*[Cc][Nn]=([a-zA-Z0-9.]*).*$/$1/L,
DEFAULT
```
These map CN=serviceuser,OU=ServiceUsers,... to serviceuser, and CN=adminUser,OU=Admin,... to adminuser@admin.

SASL Kerberos: the default name is the primary part of the principal. Customize with `sasl.kerberos.principal.to.local.rules`, which works like auth_to_local in krb5.conf, with formats such as `RULE:[n:string](regexp)s/pattern/replacement/g/L`. To map user@MYDOMAIN.COM to user and keep the default:
`sasl.kerberos.principal.to.local.rules=RULE:[1:$1@$0](.*@MYDOMAIN.COM)s/@.*//,DEFAULT`

For advanced needs set `principal.builder.class` to your own class (it must implement KafkaPrincipalSerde in KRaft).

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/security/authorization-and-acls/ (Customizing SSL User Name and Customizing SASL User Name sections read; unsourced rollout advice dropped)
