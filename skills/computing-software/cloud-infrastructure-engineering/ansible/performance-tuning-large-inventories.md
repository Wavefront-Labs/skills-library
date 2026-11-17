---
id: computing-software.cloud-infrastructure-engineering.ansible.performance-tuning-large-inventories
name: performance-tuning-large-inventories
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, performance, performance-tuning, forks, pipelining, mitogen, profile-tasks, timer, fact-gathering, gather-subset, fact-caching, free-strategy, strategy, serial, async, controlpersist, callback-plugins, cgroup-perf-recap, slow-playbooks, scaling, large-inventory, loop-performance, package-lists, throttle, host-pinned]
level: advanced
status: docs-checked
description: "Make Ansible fast on hundreds of hosts: measure with profile_tasks, raise forks, enable pipelining, cache or skip facts, free strategy, throttle, batch module calls, Mitogen."
sources: ["https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_strategies.html", "https://docs.ansible.com/projects/ansible/latest/reference_appendices/config.html", "https://github.com/ansible-collections/ansible.posix/tree/main/plugins/callback", "https://mitogen.networkgenomics.com/ansible_detailed.html"]
licence: Apache-2.0
version: 6
updated: 2026-11-17
---

# Performance tuning for large inventories

**Goal:** a slow play across hundreds of hosts gets faster, and you know which
tasks ate the time before you touched a setting.

## 1. Measure first
```ini
[defaults]
callbacks_enabled = ansible.posix.profile_tasks, ansible.posix.timer, ansible.posix.profile_roles
```
The `ansible.posix` collection ships the `profile_tasks`, `profile_roles`, `timer` and
`cgroup_perf_recap` callback plugins; they must be enabled (`callbacks_enabled`, or
`ANSIBLE_CALLBACKS_ENABLED`). Read the collection docs for what each prints. Compare a single-host
run (`--limit` to one host) with the full run to see whether the problem is per-host latency or
parallelism.

## 2. Parallelism
- `forks` (`[defaults]`, env `ANSIBLE_FORKS`) defaults to 5. Raise it in steps while watching
  control-node CPU and memory.
- `strategy: free` lets each host run to the end of the play as fast as it can instead of waiting
  for the slowest host at each task (the default is `linear`). Use for independent hosts.
- `serial` limits how many hosts run at once (rolling updates; a number or percentage). Do not
  leave a one-off `serial` in a daily play.
- `throttle` limits workers for one task or block (CPU-heavy work, rate-limited APIs). It can
  only reduce concurrency: it must be lower than `forks` or `serial` to have an effect.

## 3. Connection cost
`pipelining` (default False, config key `pipelining`, env `ANSIBLE_PIPELINING`) reduces the
network operations per module run; read its description for the sudo `requiretty` caveat. The
connection `timeout` defaults to 10 seconds, so unreachable hosts cost time on every run.

## 4. Facts
- `gather_facts: false` on plays that do not need them.
- `gathering` defaults to `implicit` (facts per play). `smart` scans only hosts with no facts yet
  and does not contact a host again in the same run; `smart` and `explicit` use the fact cache.
- Choose a cache plugin with `fact_caching` (env `ANSIBLE_CACHE_PLUGIN`); `fact_caching_timeout`
  defaults to 86400 seconds.
- Many small plays with `hosts: all` each gather facts again; use one play, or
  `gather_facts: false` on the later ones.

## 5. Task design
- Pass a list to modules that accept one instead of looping (one package-module call with many
  names); check the module docs for list support.
- Do one-off actions (API calls, DNS) once with `delegate_to` and `run_once`, not per host.
- Avoid enormous registered results; filter in the module rather than afterwards.

## 6. Mitogen (optional)
Download a Mitogen release, then in `[defaults]` set `strategy_plugins` to its
`ansible_mitogen/plugins/strategy` directory and `strategy = mitogen_linear`; the environment
variable `ANSIBLE_STRATEGY=mitogen_linear` switches it per run. The Mitogen docs also list
`mitogen_free` and `mitogen_host_pinned`, state that Ansible become plugins are not yet
supported, list the supported connection types, and note that Mitogen applies connection and
become timeouts differently from Ansible. Pin it, test it, and keep the ability to run without it.

## 7. Control node
Run from a host near the targets (round-trip latency times tasks times hosts is the bill);
avoid very verbose output in CI.

## Gotchas
- A single unreachable host stalls each task up to the connection timeout; remove dead hosts from
  the run (`--limit`).
- A stale fact cache after a rebuild gives wrong facts; flush or expire it.
- Large inventories with many variables make templating slow; split inventories by environment.

## Verify
- [ ] The `profile_tasks` and `timer` output after tuning shows the slowest tasks are genuine long
  operations and the total dropped.
- [ ] A second run skips fact gathering when `smart` plus a cache plugin is configured.

## Checked
2026-11-01. Confirmed on the Ansible strategies page: linear is the default, `free`, `serial`
(number or percentage), `throttle` can only lower concurrency, 5 forks by default. Confirmed on
the configuration page: `forks` default 5, `strategy` default linear, `strategy_plugins`,
`pipelining` default False, `timeout` default 10, `gathering` choices and default `implicit`,
`fact_caching`, `fact_caching_timeout` default 86400, `callbacks_enabled`. Confirmed in the
ansible.posix callback directory: the four callback plugin files. Confirmed on the Mitogen page:
strategy settings, the three strategies, become-plugin and timeout notes.
Removed: the "20 slowest tasks" detail, cgroup requirements, specific forks values, `host_pinned`
semantics, the ssh_args example, `gather_subset`, the MaxStartups default, the sudoers
requirement, the package-module and `include_tasks` cost claims, `ansible-config` and
`--flush-cache` commands, and the 30 s verify target.
Method: documentation only; no commands were run.
