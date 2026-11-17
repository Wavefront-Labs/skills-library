---
id: computing-software.cloud-infrastructure-engineering.ansible.timed-pause-and-wait-steps
name: timed-pause-and-wait-steps
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, prompts-interactive, timed-pause, pause-seconds, wait-for, until-retries]
level: intro
status: docs-checked
description: "Pause a play for a fixed time with pause seconds or minutes, know it runs once for all hosts, and replace fixed sleeps with wait_for or until loops where possible."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/pause_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_module.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html#retrying-a-task-until-a-condition-is-met"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timed pause and wait steps

## pause with a timer
```yaml
- name: Let caches warm before the next batch
  ansible.builtin.pause:
    seconds: 30          # or minutes: 2 (not both)
```
Behaviour:
- It is not a per-host sleep: with `serial` it acts once for each group of hosts (module docs).
- Interactive terminals can skip with Ctrl+C then `c` (continue) or `a` (abort).
- Without an interactive stdin the action plugin warns that it is not waiting for a response to the prompt.
- With `serial`, it pauses between batches — a common "soak time" pattern:
```yaml
- hosts: web
  serial: 1
  tasks:
    - ansible.builtin.include_role: {name: app}
    - ansible.builtin.pause: {minutes: 5}     # observe metrics before the next host
```

## Prefer a real condition
Fixed sleeps are either too short (flaky) or too long (slow). Wait for the thing itself:
```yaml
- ansible.builtin.wait_for:
    port: 8080
    host: "{{ ansible_host }}"
    delay: 5
    timeout: 300
  delegate_to: localhost

- ansible.builtin.wait_for:
    path: /var/log/app.log
    search_regex: "Started Application"
    timeout: 300

- ansible.builtin.uri: {url: "http://{{ ansible_host }}:8080/health"}
  register: hc
  until: hc.status == 200
  retries: 60
  delay: 5
  delegate_to: localhost
```
`wait_for` also handles `state: drained` (no active connections), `state: absent` (file/port gone).

## Per-host sleep
Need each host to sleep independently (e.g. staggered starts)? Use
`ansible.builtin.wait_for: {timeout: 10}` (sleeps on the target) or `command: sleep 10`.

## Gotchas
- `pause` with only a `prompt` (no timer) waits for input, and prompting for a set amount of time is not supported. Do not rely on prompts in automation; use timers or real conditions.
- Inside a loop, each iteration pauses.

## Verify
- [ ] The task result reports the pause (`stdout` such as "Paused for 0.04 minutes", plus `delta`).

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in modules/pause.py and plugins/action/pause.py (stable-2.22): minutes and seconds options are mutually exclusive, Ctrl+C then c continues and a aborts, with `serial` you are prompted once per group of hosts, prompting for a set time is unsupported, a warning is shown when stdin is not interactive, return values stdout and delta.
- Confirmed in modules/wait_for.py: options host, port, path, state (absent, drained, present, started, stopped), delay (default 0), timeout (default 300), search_regex, and that wait_for is the documented way to pause per host.
- Removed unconfirmed claims: pause running once for the whole play, CI/AWX behaviour, profile_tasks verification.

Method: documentation only; no commands were run.
