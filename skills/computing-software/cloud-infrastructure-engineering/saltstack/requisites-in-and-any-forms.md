---
id: computing-software.cloud-infrastructure-engineering.saltstack.requisites-in-and-any-forms
name: requisites-in-and-any-forms
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, requisites, require-in, watch-in, require-any, watch-any, onlyif, unless, creates]
level: practitioner
status: docs-checked
description: "Reverse Salt dependencies with the _in requisite forms, use the _any variants, and guard states with onlyif, unless and creates."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/requisites.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Requisite _in and _any forms, guards

**_in forms**: `require_in`, `watch_in`, `onchanges_in`, `listen_in`, `onfail_in` and `prereq_in` declare the dependency from the target's side. Useful in loops and when a file is defined after the service it affects.

```yaml
httpd:
  pkg.installed:
    - require_in:
      - service: httpd
  service.running: []
```

There is no combined form such as `require_any_in`.

**_any forms**:
- `require_any` (since 2018.3.0): runs if at least one target succeeds, not all.
- `watch_any`, `onchanges_any`, `onfail_any`: trigger if any target has changes or fails.

```yaml
A:
  cmd.run:
    - name: echo A
    - require_any:
      - cmd: B
      - cmd: C
```

**exclude**: if a state removed by `exclude` is still referenced by a requisite, compilation raises a hard error.

**Guards** (not requisites):
- `onlyif` and `unless` run their commands through a shell with `python_shell=True`.
- `creates` (since 3001) runs the state only when the listed file does not exist; with a list of files it runs if any is missing.

## Checked

2026-11-04: read the Salt requisites reference page in full. Confirmed the _in forms, no combined _any_in form, the 2018.3.0 _any forms, the exclude hard error and the onlyif, unless and creates guards. Expanded the creates line to match the page.

Method: documentation only; no commands were run.

