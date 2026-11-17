---
id: computing-software.cloud-infrastructure-engineering.alertmanager.matcher-yaml-quoting
name: matcher-yaml-quoting
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, matchers, yaml-quoting, escaping]
level: advanced
status: docs-checked
description: "YAML quoting versus matcher-token quoting for Alertmanager matchers: plain, single-quoted and double-quoted YAML styles and when each is safe."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# YAML quoting versus matcher quoting

Each entry in a `matchers:` list is one YAML string that Alertmanager parses after YAML processing. YAML quoting applies to the entire matcher string and does not protect individual tokens inside it. The double quotes handled by Alertmanager's own parser are applied after YAML has finished.

Three YAML styles:
- Plain (no surrounding quotes): works when the matcher contains no YAML special characters `{ } [ ] , # | > :`. Example: `env !~ preprod`.
- Single-quoted: protects against all YAML special characters and allows literal double quotes inside. Example: `'env =~ "prod|staging"'`.
- Double-quoted: supports YAML escape sequences; literal double quotes inside the value must be escaped as `\"`. Example: `"env !~ \"uat\""`.

Writing `env =~ "prod"` with no YAML quotes is valid plain-style YAML, but the inner double quotes are stripped by Alertmanager's parser and give no protection against YAML special characters. Always quote the entire matcher at the YAML level when the value may contain special characters.

For short-form lists, double quotes avoid comma problems:

```yaml
matchers: [ "foo = \"bar,baz\"", "dings != bums" ]
```

For awkward values, use a YAML block:

```yaml
matchers:
  - |
      {quote=~"She said: \"Hi, all!( How're you…)?\""}
```

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference source (prometheus/alertmanager, docs/configuration.md, main branch, read in full), the published form of the cited prometheus.io page: the YAML quoting rules for matchers. Removed: nothing.

Method: documentation only; no commands were run.
