---
id: computing-software.cloud-infrastructure-engineering.saltstack.targeting-glob-regex-list
name: targeting-glob-regex-list
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, targeting, glob, regex, pcre, list, minion-id]
level: intro
status: docs-checked
description: "Target Salt minions by ID using globs, PCRE regex (-E) and explicit lists (-L), including the top file match option and shell-quoting rules."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/targeting/globbing.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeting by minion ID: glob, regex, list

Each minion needs a unique ID (default: its FQDN on first start; override with the minion `id` setting). The ID is used to generate the minion's keys, so if it changes the master must accept the new key as for a new host.

**Glob** (default): shell-style matching on the ID. Single-quote the target so your shell does not expand it.

| Target | Matches |
|---|---|
| `'*'` | all minions |
| `'*.example.net'` | the example.net domain |
| `'web?.example.net'` | webN.example.net, such as web1.example.net and web2.example.net |
| `'web[1-5]'` | web1 to web5 |
| `'web[1,3]'` | web1 and web3 |
| `'web-[x-z]'` | web-x, web-y, web-z |

**Regex** (`-E`, PCRE): `salt -E 'web1-(prod|devel)' test.version`

**List** (`-L`): `salt -L 'web1,web2,web3' test.version`

In a top file, a non-glob matcher must be the first option under the target:

```yaml
base:
  'web1-(prod|devel)':
    - match: pcre
    - webserver
```

## Checked

2026-11-04: read the Salt minion ID targeting page in full. Confirmed default FQDN id, glob examples, -E, -L, single-quote note and the top file match: pcre example. Reworded the key sentence and the web? row, which claimed web1 to web9 although ? matches any single character.

Method: documentation only; no commands were run.

