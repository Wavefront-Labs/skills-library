---
id: computing-software.systems-network-administration.zabbix.secret-and-vault-macros
name: secret-and-vault-macros
category: computing-software
field: systems-network-administration
product: zabbix
tags: [secret-macros, vault, hashicorp, cyberark, secrets-reload, secret, macro]
level: advanced
status: docs-checked
description: "Protect credentials with Secret text and Vault secret macros, and know where they are still unmasked."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/macros/secret_macros
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two options protect sensitive macro values: Secret text and Vault secret. Change the type with the button at the end of the Value field.

Secret text is masked with asterisks and cannot be viewed after saving. Use Set new value to replace it; that erases the current value. Important: the real value is available to the server, so it can be revealed through use in items (for example an external script that echoes it). URLs containing a secret macro will not work.

Vault secret stores the value in an external vault: the macro value must point to a vault secret (the docs give HashiCorp and CyberArk examples) and the input format depends on the provider.
- The server, and the proxy when Resolve secret vault macros by is set to Zabbix server and proxy, fetch values on every configuration refresh and keep them in the configuration cache.
- With the server-only setting, the proxy receives values from the server on each configuration sync. After a restart it cannot collect data until it receives that sync.
- Use the secrets_reload runtime control option (server only) to refresh manually.
- Encrypt server-to-proxy traffic, or the server logs a warning.
- If a value cannot be fetched, items using it become unsupported.

Secret values are unmasked in places such as item key parameters, SNMP community and credentials, HTTP agent URL, query fields, body, headers and passwords, script items, database monitor queries, and SSH or Telnet credentials. They stay masked when referenced indirectly, for example through {ITEM.KEY}. Secret macros cannot be used in trigger expressions.

## Checked

2026-11-09. Confirmed against the Zabbix manual page Secret user macros (current): the two secret types, masking and Set new value behaviour, URL limitation, vault refresh on configuration sync, proxy restart behaviour, secrets_reload, encryption warning, unsupported items on fetch failure, the unmasked locations list and indirect masking.

Method: documentation only; no commands were run.
