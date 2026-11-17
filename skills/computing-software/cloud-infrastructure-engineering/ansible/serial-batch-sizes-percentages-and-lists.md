---
id: computing-software.cloud-infrastructure-engineering.ansible.serial-batch-sizes-percentages-and-lists
name: serial-batch-sizes-percentages-and-lists
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, strategies-forks, serial-batches, serial-percent, serial, max-fail-percentage, rolling-update]
level: practitioner
status: docs-checked
description: "Size rolling-update batches with serial as a number, a percentage or an escalating list, and combine it with max_fail_percentage and any_errors_fatal correctly."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# serial: numbers, percentages and batch lists

Without `serial`, every task runs on all play hosts before the next task (subject to forks).
`serial` splits the play into batches; each batch runs the **whole play** before the next starts.

```yaml
serial: 3              # 3 hosts per batch
serial: "30%"          # 30% of the play's hosts per batch (fraction truncated, minimum 1 host)
serial: [1, 5, "20%"]  # first batch 1 host, then 5, then 20% repeatedly for the rest
serial: [1, "10%", "100%"]  # canary, small wave, then everything left
```
The last value in a list repeats until all hosts are done; the final batch holds whatever remains.

## Failure policy per batch
- Default: if **all** hosts in a batch fail, the play stops. A batch with some failures continues to the next batch!
- `max_fail_percentage: 20` — applies to each batch: abort the rest of the play when more than 20% of the batch fails. The percentage must be exceeded, not equalled (serial 4, abort on 2 failures: set 49, not 50).
- `max_fail_percentage: 0` — any failure in a batch exceeds 0%, so it aborts the rollout.
- `any_errors_fatal: true` — Ansible finishes the failed task on all hosts in the current batch, then stops the play on all hosts.

Rolling updates almost always want `max_fail_percentage: 0` (or small) with `serial`.

## Useful variables
- `ansible_play_batch` — active hosts in the current batch (failed or unreachable hosts are not active).
- `ansible_play_hosts` — hosts of the play not limited by serial, excluding failed and unreachable ones.
- `ansible_play_hosts_all` — every host targeted by the play.

## Interaction with other features
- `run_once` runs once per batch.
- `order:` decides which hosts land in which batch; use `sorted` for determinism.
- `throttle:` limits the workers for a block or task (CPU-heavy work, rate-limited APIs); it can only lower the effective parallelism set by `forks` or `serial`.

## Choosing sizes
- Capacity: the hosts outside the current batch must carry the traffic; size batches from your own load numbers.
- Time: total is roughly batches x play duration. 100 hosts at serial 1 with a 3-minute play = 300 minutes.
- Canary: start with 1.

## Gotchas
- The host count per batch is truncated and never below 1: `"30%"` of 3 hosts = 0.9 → 1; of 20 hosts = 6, 6, 6, 2.
- `serial` is a play keyword only; it cannot be set on a block or task.
- `--limit` changes the host count, so percentage batches shift with the limit.

## Verify
- [ ] Output shows `PLAY [...]` batch boundaries (hosts per batch) as intended in a `--check` run.
- [ ] A forced failure in batch 1 stops the run (`max_fail_percentage` honoured).

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Controlling playbook execution (playbooks_strategies.rst) and Error handling (playbooks_error_handling.rst), devel; ansible-core helpers.py, play.py, special_variables.rst.
Confirmed:
- serial number, percentage and list forms; last list value repeats; minimum 1 host; percentage is truncated (pct_to_int in utils/helpers.py).
- max_fail_percentage is per batch and must be exceeded, not equalled; any_errors_fatal finishes the task on the current batch then stops.
- ansible_play_batch, ansible_play_hosts and ansible_play_hosts_all definitions; serial is a play-only keyword; throttle can only lower parallelism.
- Removed handler-flush, fact-availability and capacity-percentage claims that no doc covers.

Method: documentation only; no commands were run.
