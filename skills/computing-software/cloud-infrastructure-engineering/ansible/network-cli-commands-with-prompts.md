---
id: computing-software.cloud-infrastructure-engineering.ansible.network-cli-commands-with-prompts
name: network-cli-commands-with-prompts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, network-automation, cli-prompt, command-prompts, cli-command, ios-command, wait-for]
level: practitioner
status: docs-checked
description: "Run interactive network CLI commands that ask for confirmation with cli_command prompt/answer or platform command modules, and wait for output conditions."
sources: ["https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/modules/cli_command.py", "https://github.com/ansible-collections/cisco.ios/blob/main/plugins/modules/ios_command.py", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/network_debug_troubleshooting.rst", "https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/doc_fragments/connection_persistent.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network CLI commands with prompts

Commands like `copy running-config startup-config`, `reload`, `clear counters`, `delete flash:x`
ask questions. Without an answer the task hangs until `command_timeout` (default 30 s).

## cli_command (platform-agnostic)
```yaml
- name: Save config
  ansible.netcommon.cli_command:
    command: copy running-config startup-config
    prompt: 'Destination filename \[startup-config\]\?'
    answer: "\r"

- name: Clear counters (prompt + confirm)
  ansible.netcommon.cli_command:
    command: clear counters
    prompt: ['confirm']
    answer: ['y']

- name: Multiple prompts in sequence
  ansible.netcommon.cli_command:
    command: delete flash:old.bin
    prompt: ['Delete filename', 'confirm']
    answer: ["\r", 'y']
    check_all: true          # all prompts must be matched, in order
```
`prompt` values are **regexes**: escape `[ ] ? ( )`. `newline: false` if the device must not get
an extra Enter after the answer.

## Platform command modules
```yaml
- cisco.ios.ios_command:
    commands:
      - command: 'clear logging'
        prompt: 'Clear logging buffer \[confirm\]'
        answer: 'y'
```

## Waiting for state
```yaml
- cisco.ios.ios_command:
    commands: [show ip bgp summary]
    wait_for:
      - result[0] contains Established
    retries: 10
    interval: 6
```
`match: all|any` for several conditions.

## Reload and reconnect
```yaml
- ansible.netcommon.cli_command:
    command: reload
    prompt: ['Save\?', 'confirm']
    answer: ['n', 'y']
    check_all: true
  ignore_errors: true          # connection drops
- ansible.builtin.wait_for:
    host: "{{ ansible_host }}"
    port: 22
    delay: 60
    timeout: 900
  delegate_to: localhost
- ansible.builtin.meta: reset_connection
```

## Debugging hangs
Set `ANSIBLE_LOG_PATH=~/ansible.log` and `ANSIBLE_PERSISTENT_LOG_MESSAGES=True` (or the `ansible_persistent_log_messages` variable; logs sent/
received data, including passwords in plain text, so only temporarily), then look for the last received prompt.
Raise `ansible_command_timeout` for slow operations (`copy` of images).

## Gotchas
- Prompt text differs by version/platform; regex with `.*` slack: `'confirm'` not `'\[confirm\]$'`.
- In check mode, `ios_command` runs only `show` commands and skips the rest with a warning; do not count on check mode to exercise prompt handling — test prompts on a lab device.
- Answers containing secrets get logged in plain text with persistent log messages enabled; Ansible's own secret masking does not cover them.

## Verify
- [ ] Task completes in seconds rather than at `command_timeout`.
- [ ] `show startup-config | include hostname` reflects the saved config.

## Checked

Checked 2026-10-26 against the ansible.netcommon and cisco.ios collection sources on GitHub (main) and the Ansible network debug page. Confirmed: `cli_command` options `prompt`, `answer`, `newline` (default true) and `check_all` (default false) with `prompt` as regex patterns and prompt/answer required together; `persistent_command_timeout` / `ansible_command_timeout` default 30 s; `ios_command` `wait_for`, `match` (all or any, default all), `retries` and `interval`; check mode in `ios_command` skips commands that do not start with `show` with a warning; `ANSIBLE_LOG_PATH`, `ANSIBLE_PERSISTENT_LOG_MESSAGES` and the plain-text logging warning. Removed the guessed `/tmp` log path.

Method: documentation only; no commands were run.
