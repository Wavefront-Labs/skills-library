---
id: computing-software.cloud-infrastructure-engineering.saltstack.top-file-structure
name: top-file-structure
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, top-file, environments, file-roots, saltenv, match]
level: intro
status: docs-checked
description: "Understand the Salt state top file: environments, targets, match directives (glob, pcre, grain, pillar, ipcidr, nodegroup), saltenv and file_roots."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/top.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The state top file

`top.sls` sits at the top of the state tree and maps targets (minion groups) to the SLS files they receive. Structure: environment, then target, then states.

- Environments come from the master's `file_roots`, each pointing at a state tree directory. Most sites use only `base`.
- Pin a minion to an environment with `environment` in its minion config; select at runtime with `saltenv`, e.g. `state.highstate saltenv=prod`.

Matching: since 2014.7.0 the default matcher is compound, so a single glob works like a glob match. Add `- match: <type>` to change it. Types: `glob`, `pcre`, `list`, `grain`, `grain_pcre`, `pillar`, `pillar_pcre`, `pillar_exact`, `ipcidr`, `range`, `compound`, `nodegroup`, `data`.

Minion IDs containing spaces will not match the compound matcher; set `glob` explicitly.

## Checked

2026-11-04: read the Salt top file reference page in full. Confirmed the environment/target/states structure, file_roots, the environment minion option, saltenv, the 2014.7.0 compound default, the whitespace edge case and the list of match types. Replaced "one or more directories", which the page does not state.

Method: documentation only; no commands were run.

