---
id: computing-software.cloud-infrastructure-engineering.ansible.sharing-run-once-results-across-hosts
name: sharing-run-once-results-across-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, delegation, run-once-results, run-once, register]
level: practitioner
status: docs-checked
description: "Use run_once results on every host: registered vars and set_fact are copied to all hosts in the batch, plus hostvars lookups, serial batches and conditional pitfalls."
sources: ["Controlling where tasks run, run_once (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html#running-on-a-single-machine-with-run-once)", "Playbook keywords, run_once (https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html)", "Kubernetes kubeadm token create (https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-token/)", "Kubernetes kubeadm join (https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sharing run_once results

```yaml
- name: Generate cluster join token once
  ansible.builtin.command: kubeadm token create --print-join-command
  register: join_cmd
  run_once: true
  delegate_to: "{{ groups['control_plane'] | first }}"
  changed_when: true

- name: Join workers
  ansible.builtin.command: "{{ join_cmd.stdout }}"
  args: {creates: /etc/kubernetes/kubelet.conf}
  when: inventory_hostname in groups['workers']
```

## Semantics
- The task executes on the first available host in the current batch (or on the delegate), and the **results and facts are applied to all hosts** in the same batch: `join_cmd` exists on all of them.
- `set_fact` with `run_once: true` likewise sets the fact on all hosts in the batch.
- `serial`: `run_once` runs on one host in *each* serial batch; to run exactly once regardless of `serial`, use `when: inventory_hostname == ansible_play_hosts_all[0]`.

## Reading it from another play
Results are per host; read from a known host:
```yaml
- hosts: workers
  tasks:
    - ansible.builtin.debug:
        msg: "{{ hostvars[groups['control_plane'] | first]['join_cmd'].stdout }}"
```

## Pitfalls
- `when` with `run_once`: the conditional uses the variables of the first host to decide whether the task runs; no other hosts are tested. Make the condition independent of the host, or filter hosts first.
- The keyword description says the task is attempted on the first host *available*, so an unreachable or failed host is not chosen.
- `delegate_to` changes where the task runs, but the information (variables) is still that of the original host.

## Verify
```yaml
- ansible.builtin.debug: {var: join_cmd.stdout}      # same value printed for every host
```

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and the Kubernetes website sources for kubeadm.
- Confirmed: `run_once` runs on the first host in the batch and applies results and facts to all hosts in the batch; with `serial` it runs once per batch and `ansible_play_hosts_all[0]` gives a single run; conditionals use the first host's variables; delegation keeps the original host's information; `kubeadm token create --print-join-command` exists.
- Removed as unconfirmed: the failure-propagation and `run_once` plus `loop` remarks.

Method: documentation only; no commands were run.
