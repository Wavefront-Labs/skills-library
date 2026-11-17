---
id: computing-software.cloud-infrastructure-engineering.ansible.async-tasks-in-loops
name: async-tasks-in-loops
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, async-polling, async-loop, async-status, loops]
level: advanced
status: docs-checked
description: "Launch many async jobs from a loop with poll 0 and wait for all of them with an async_status loop and until, to run tasks concurrently on one host."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_async.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/async_status_module.html", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_async.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Async tasks in loops

Loops run items sequentially. To run items in parallel on the same host, start each one with
`async` and `poll: 0`, then collect the results afterwards.

```yaml
- name: Start image downloads in parallel
  ansible.builtin.get_url:
    url: "{{ item.url }}"
    dest: "/srv/images/{{ item.name }}"
    checksum: "{{ item.checksum }}"
  loop: "{{ images }}"
  loop_control:
    label: "{{ item.name }}"
  async: 1800
  poll: 0
  register: dl_jobs

- name: Wait for all downloads
  ansible.builtin.async_status:
    jid: "{{ item.ansible_job_id }}"
  loop: "{{ dl_jobs.results }}"
  loop_control:
    label: "{{ item.item.name }}"
  register: dl_status
  until: dl_status is finished
  retries: 180
  delay: 10

- name: Clean up job files
  ansible.builtin.async_status:
    jid: "{{ item.ansible_job_id }}"
    mode: cleanup
  loop: "{{ dl_jobs.results }}"
  loop_control:
    label: "{{ item.item.name }}"
```

## Notes
- With `poll: 0` Ansible does not clean up the job cache file (default `~/.ansible_async/`); the
  cleanup task above does it with `mode: cleanup`.
- If `async` is too low, the status task fails because the job's status file was never written or
  no longer exists.
- Async tasks always report changed; put `changed_when` or `creates` logic on the `async_status` task.
- To limit concurrency, batch the list: the documented pattern loops over
  `sleep_durations | batch(2) | list` with `include_tasks`, and the included file starts the async
  items and waits for them (`async_status` with `until: ... is finished`).
- Do not use `poll: 0` with operations that need exclusive locks (such as yum transactions) if
  later tasks use the same resources; pass a package list to one task instead.

## Gotchas
- Async tasks do not support check mode and fail when run in it.
- Async failures appear in the status loop, not in the launch loop.

## Verify
- [ ] Total wall time is close to the longest single item, not the sum.

## Checked
Checked 2026-10-23 against the ansible-documentation playbook guide (playbooks_async.rst) and the
ansible-core devel `async_status` module and action plugin sources. Confirmed: `poll: 0` behaviour,
no automatic cleanup, `mode: cleanup`, `is finished` test, the `batch(2)` include pattern, changed-always
rule and check-mode note. Removed unconfirmed claims about skipped-item filtering and `get_url`/`copy`
async support.
Method: documentation only; no commands were run.
