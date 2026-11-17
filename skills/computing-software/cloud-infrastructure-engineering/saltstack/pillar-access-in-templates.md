---
id: computing-software.cloud-infrastructure-engineering.saltstack.pillar-access-in-templates
name: pillar-access-in-templates
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, pillar, jinja, pillar-get, templates, states]
level: practitioner
status: docs-checked
description: "Read Salt pillar values in states and Jinja templates: the pillar dict, salt['pillar.get'] with nested keys and defaults, and the pillar top file saltenv note."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/pillar/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessing pillar in states and templates

Direct dictionary access:

```jinja
{{ pillar['apache'] }}
```

For nested lookups with a default, call the Salt function:

```jinja
{{ salt['pillar.get']('foo:bar:baz', 'qux') }}
```

Plain `pillar.get()` in a template calls the standard dict method, which lacks the `:` nested-key delimiter. Prefer `salt['pillar.get']`.

In Jinja used inside pillar top files, use `{{ saltenv }}`, not `{{ pillarenv }}`.

Pillar can also set minion options: top-level pillar keys such as `mysql.pass` configure the minion.

## Checked

2026-11-04: read the Salt pillar reference page in full. Confirmed pillar dictionary access, salt['pillar.get'] with nested keys and a default, the pillar.get() versus salt['pillar.get']() note, the saltenv note for pillar top files and minion config in pillar. Removed "Salt default handling", which the page does not say.

Method: documentation only; no commands were run.

