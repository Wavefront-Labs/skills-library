---
id: computing-software.cloud-infrastructure-engineering.saltstack.requisites-listen-prereq-use
name: requisites-listen-prereq-use
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, requisites, listen, prereq, use, states]
level: practitioner
status: docs-checked
description: "Use the Salt listen, prereq and use requisites: end-of-run mod_watch, running a state before a target only if it would change, and copying state arguments."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/requisites.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Requisites: listen, prereq and use

**listen** (since 2014.7.0): triggers the `mod_watch` of the listening state's module at the end of the whole state run, without changing execution order. Declare it on the listener, or use `listen_in` on the target.

```yaml
restart-apache2:
  service.running:
    - name: apache2
    - listen:
      - file: /etc/apache2/apache2.conf
```

**prereq**: runs this state before the target, but only if the target would report changes. The target is first evaluated in `test=True` mode.
- If the target would change nothing, neither state runs.
- If the prereq state fails, the target does not run.

```yaml
graceful-down:
  cmd.run:
    - name: service apache graceful
    - prereq:
      - file: site-code

site-code:
  file.recurse:
    - name: /opt/site_code
    - source: salt://site/code
```

**use**: copies the arguments of another state ID into the current one. Requisites of the used state are not copied.

```yaml
/etc/bar.conf:
  file.managed:
    - source: salt://bar.conf
    - use:
      - file: /etc/foo.conf
```

## Checked

2026-11-04: read the Salt requisites reference page in full. Confirmed listen (2014.7.0) and listen_in, prereq test=True behaviour and its examples, and use not inheriting the requisites of the targeted state. Corrected the listen sentence to say the listening state's module runs mod_watch.

Method: documentation only; no commands were run.

