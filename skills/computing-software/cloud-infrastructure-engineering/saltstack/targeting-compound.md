---
id: computing-software.cloud-infrastructure-engineering.saltstack.targeting-compound
name: targeting-compound
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, targeting, compound, matchers, boolean, top-file]
level: practitioner
status: docs-checked
description: "Build Salt compound targets with -C: letter@ matcher prefixes, and/or/not, parentheses spacing, alternate delimiters and use in the top file."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/targeting/compound.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compound targeting

Default match is glob; prefix `letter@` to switch matcher:

| Letter | Matcher | Example |
|---|---|---|
| G | grains glob | `G@os:Ubuntu` |
| E | PCRE on minion ID | `E@web\d+\.(dev\|qa\|prod)\.loc` |
| P | grains PCRE | `P@os:(RedHat\|Fedora\|CentOS)` |
| L | list | `L@minion1.example.com,minion3.domain.com` |
| I | pillar glob | `I@pdata:foobar` |
| J | pillar PCRE | `J@pdata:^(foo\|bar)$` |
| S | subnet/IP | `S@192.168.1.0/24` |
| R | range cluster | `R@%foo.bar` |
| N | nodegroup | `N@group1` |

Combine with `and`, `or`, `not`: `salt -C 'not web-dc1-srv'` (leading `not` needs 2015.8.0+; before that use `'* and not G@kernel:Darwin'`). The page does not state precedence, so group with parentheses and put spaces around them: `'( ms-1 or G@id:ms-3 ) and G@id:ms-3'`.

Alternate delimiter (2015.8.0+, only G, P, I, J): put it between letter and `@`, e.g. `J|@foo|bar|^foo:bar$`.

Top file use needs `match: compound`:

```yaml
base:
  'webserv* and G@os:Debian or E@web-dc1-srv.*':
    - match: compound
    - webserver
```

## Checked

2026-11-04: read the Salt compound matchers page in full. Confirmed the letter table and examples, and/or/not, the 2015.8.0 leading-not note, parentheses spacing, alternate delimiters (Yes only for G, P, I, J) and the top file example. Nothing removed.

Method: documentation only; no commands were run.

