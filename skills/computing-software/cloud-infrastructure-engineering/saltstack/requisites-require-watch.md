---
id: computing-software.cloud-infrastructure-engineering.saltstack.requisites-require-watch
name: requisites-require-watch
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, requisites, require, watch, mod-watch, states]
level: practitioner
status: docs-checked
description: "Order Salt states with require and watch: target form, SLS-level require, mod_watch behaviour and the caveats where a watch silently does not fire."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/requisites.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Requisites: require and watch

Requisite targets take the form `<state module>: <ID or name>`. They match the state ID or its `name` argument; the module name is optional since 2016.3.0.

**require**: the state waits until every target succeeds; if a target fails, this state fails too.

```yaml
nginx:
  service.running:
    - require:
      - pkg: nginx
```

To depend on a whole SLS file (since 0.16.0), include it and use `- sls: <name>` under `require`.

**watch**: like `require`, and additionally calls the watching module's `mod_watch` when a target reports changes (for `service.running` this means a restart).
- If the target result is `False`, the watching state does not run.
- No changes in the target, or no `mod_watch` in the watching module, means it behaves as plain `require`.
- Has no effect on SLS-level targets.

Caveats:
- `mod_watch` is skipped if the watching state itself produced changes (unless the state returns `force_mod_watch: True`). Enabling a service and restarting it in one state can therefore swallow the restart; split `service.running` and `service.enabled` into separate states.
- A skipped target propagates the skip to the dependent state.
- Wildcards `*`, `?`, `[]` match state IDs; quote a leading or bare `*`.

## Checked

2026-11-04: read the Salt requisites reference page in full. Confirmed target form and matching, 2016.3.0 optional module, require and the 0.16.0 sls form, watch and mod_watch behaviour, the force_mod_watch note, the service.enabled caveat, skip propagation (truth table notes) and wildcard rules. Nothing removed.

Method: documentation only; no commands were run.

