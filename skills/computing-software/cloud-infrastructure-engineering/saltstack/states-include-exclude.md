---
id: computing-software.cloud-infrastructure-engineering.saltstack.states-include-exclude
name: states-include-exclude
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, states, include, exclude, relative-include, ordering]
level: practitioner
status: docs-checked
description: "Use Salt include and exclude in SLS files: cross-environment includes, relative dotted includes, exclude by sls or id, and why include does not set run order."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/include.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# include and exclude

**include** adds everything from the named SLS files to the run. Formulas come from the includer's environment unless you name one, e.g. `- dev: http`. It does not inject states at that spot; use requisites for guaranteed order.

**Relative includes:** `.virt` is relative to the current formula (0.16.0); extra dots climb levels like Python imports (2015.8). From `example.dev.virtual`, `..http` is `example.http` and `...base` is `base`.

**exclude** (0.10.3) hard-removes an SLS (`- sls: http`) or an ID (`- id: /etc/vimrc`) after high data is compiled.

Duplicate IDs error even if one is excluded.

Ordering: each SLS is processed depth-first and loaded once. Execution order is set by requisites, then `order`, then the compiler tie-breaker (resolution order). Reordering `include` entries can change that order silently, so add an explicit `require` instead (the page's example adds `require: - pkg: web-pkg` to the config file state). Include cycles resolve, but requisite cycles are a hard error.

## Checked

2026-11-04: read the Salt include and exclude page in full. Confirmed include syntax, the environment form, relative includes (0.16.0, 2015.8, the example.dev.virtual example), exclude (0.10.3) by sls or id, the duplicate ID note and the resolution versus execution order section. Clarified the require example wording.

Method: documentation only; no commands were run.

