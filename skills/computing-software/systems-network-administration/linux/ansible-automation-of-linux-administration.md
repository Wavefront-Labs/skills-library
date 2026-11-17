---
id: computing-software.systems-network-administration.linux.ansible-automation-of-linux-administration
name: ansible-automation-of-linux-administration
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ansible, ansible-playbook, configuration-management, inventory, ansible-vault, roles, collections, ansible-galaxy, idempotent, handlers, templates, jinja2, ansible-lint, check-mode, become, ansible-navigator, rhce, ex294, system-roles, ansible-pull, automation, sysadmin, ansible-facts, ansible-conditionals]
level: practitioner
status: gated
description: "Automate Linux administration with Ansible the RHCE way: inventory, group_vars, idempotent playbooks, roles, collections, vault, handlers and check mode."
sources:
  - https://docs.ansible.com/ansible/latest/user_guide/index.html
  - https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/automating_system_administration_by_using_rhel_system_roles/index
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Ansible automation of Linux administration — every manual step becomes a task

**Goal:** describe hosts in inventory, express the desired state in idempotent
playbooks/roles, run them safely (check, diff, limit), and keep secrets out of git.

## 1. Control node and inventory
```bash
dnf install ansible-core      # apt install ansible; pipx install ansible-core; collections via ansible-galaxy
ansible-galaxy collection install ansible.posix community.general fedora.linux_system_roles
```
```ini
# inventory/hosts.ini
[web]
web01.corp.example
web02.corp.example ansible_host=10.0.10.22
[db]
db01.corp.example
[prod:children]
web
db
```
```ini
# ansible.cfg (project root)
[defaults]
inventory = inventory/hosts.ini
remote_user = ansible
host_key_checking = true
forks = 20
interpreter_python = auto_silent
roles_path = roles
collections_path = collections
[privilege_escalation]
become = true
become_method = sudo
```
Per-group/host variables in `inventory/group_vars/web.yml`, `host_vars/web01.corp.example.yml`. (gated: unconfirmed, source is paywalled or blocked)
Precedence (low→high): role defaults < inventory vars < group_vars < host_vars < play vars <
`-e` extra vars. Bootstrap: an `ansible` user with key + `NOPASSWD` sudo on every host
(cloud-init/kickstart), then `ansible all -m ping` and `ansible all -m setup -a 'filter=ansible_distribution*'`.

## 2. A real playbook
```yaml
# site.yml
- name: Base config for all hosts
  hosts: all
  gather_facts: true
  vars_files: [vars/common.yml]
  tasks:
    - name: Ensure admin group and user
      ansible.builtin.group: { name: ops, state: present }
    - ansible.builtin.user:
        name: alice
        groups: [ops, wheel]
        append: true                       # without append the user is REMOVED from other groups
        shell: /bin/bash
        password: "{{ vault_alice_hash }}"  # mkpasswd -m sha-512; never plaintext
    - ansible.posix.authorized_key: { user: alice, key: "{{ lookup('file', 'files/alice.pub') }}" }
    - name: Packages
      ansible.builtin.package: { name: [chrony, vim-enhanced, tmux], state: present }   # distro-agnostic; use dnf/apt for options
    - name: sshd hardening drop-in
      ansible.builtin.template:
        src: templates/sshd-hardening.conf.j2
        dest: /etc/ssh/sshd_config.d/10-hardening.conf
        owner: root
        group: root
        mode: "0600"
        validate: /usr/sbin/sshd -t -f %s   # refuse to deploy a broken config
      notify: restart sshd
    - name: sysctl
      ansible.posix.sysctl: { name: net.ipv4.ip_forward, value: "1", sysctl_file: /etc/sysctl.d/90-ansible.conf, reload: true }
    - name: Firewall
      ansible.posix.firewalld: { service: https, permanent: true, immediate: true, state: enabled }
    - name: Storage (RHCE favourite)
      block:
        - community.general.lvol: { vg: vg0, lv: data, size: 20g, resizefs: true }
        - community.general.filesystem: { fstype: xfs, dev: /dev/vg0/data }
        - ansible.posix.mount: { path: /srv/data, src: /dev/vg0/data, fstype: xfs, state: mounted }
      when: "'db' in group_names"
    - name: Service state
      ansible.builtin.service: { name: chronyd, state: started, enabled: true }
    - name: Scheduled job
      ansible.builtin.cron: { name: nightly-backup, minute: "0", hour: "2", job: /usr/local/sbin/backup.sh, user: root }
    - name: Line in a file (prefer templates for whole files)
      ansible.builtin.lineinfile: { path: /etc/default/grub, regexp: '^GRUB_TIMEOUT=', line: 'GRUB_TIMEOUT=3' }
      notify: regenerate grub
  handlers:
    - name: restart sshd
      ansible.builtin.service: { name: sshd, state: restarted }
    - name: regenerate grub
      ansible.builtin.command: grub2-mkconfig -o /boot/grub2/grub.cfg
```
```bash
ansible-playbook site.yml --syntax-check
ansible-playbook site.yml --check --diff --limit web01.corp.example   # dry run with diffs
ansible-playbook site.yml --limit web --tags firewall -e env=prod
ansible-playbook site.yml --start-at-task "Firewall" --step
ansible-lint site.yml
```
A second run must report `changed=0`. Things that break idempotency: `command`/`shell`
without `creates:`/`changed_when:`, `lineinfile` without `regexp`, `user` without
`append`, templates with timestamps, `get_url` without `checksum`.

## 3. Roles, collections, system roles
```bash
ansible-galaxy role init roles/webserver     # tasks/ handlers/ templates/ files/ defaults/ vars/ meta/
# requirements.yml → ansible-galaxy install -r requirements.yml (roles and collections)
```
```yaml
- hosts: web
  roles:
    - role: webserver
      vars: { web_port: 8080 }
- hosts: all
  roles:
    - role: fedora.linux_system_roles.timesync   # RHEL System Roles: timesync, selinux, firewall, storage, network, sshd, podman, journald
      vars: { timesync_ntp_servers: [{ hostname: ntp1.corp.example, iburst: true }] }
```
Roles own one concern, expose variables in `defaults/main.yml`, and use handlers for
restarts. Fully-qualified collection names (`ansible.builtin.copy`) always; `ansible-lint`
enforces it. Pin collection versions in `requirements.yml` and install into the project's
`collections_path` for reproducibility (`ansible-navigator`/execution environments on RHEL).

## 4. Secrets and facts
```bash
ansible-vault create inventory/group_vars/all/vault.yml   # vault_alice_hash: "$6$..."
ansible-vault encrypt_string --name vault_db_pass 'S3cret'   # inline encrypted value
ansible-playbook site.yml --vault-password-file ~/.vault_pass   # or --ask-vault-pass; vault_password_file in ansible.cfg
ansible-vault view/edit/rekey file
```
Convention: `vault.yml` holds `vault_*` vars; `vars.yml` maps `db_pass: "{{ vault_db_pass }}"` so
`grep` still finds variable names. Facts: `ansible_facts['distribution']`, `ansible_facts['default_ipv4']['address']`,
`ansible_facts['mounts']`; conditionals `when: ansible_facts['os_family'] == 'RedHat'`; custom facts in
`/etc/ansible/facts.d/*.fact` (INI/JSON) show up under `ansible_local`. Cache facts
(`fact_caching = jsonfile`) on big inventories.

## 5. Patterns worth copying
- `serial: 2` + `max_fail_percentage: 0` + `pre_tasks` that drain a load balancer for rolling updates.
- `block`/`rescue`/`always` for cleanup; `failed_when`/`changed_when` on commands;
  `register` + `debug: var=result` while developing; `until: … retries: 10 delay: 6` for services coming up.
- `delegate_to: localhost` + `run_once: true` for API calls; `throttle: 1` for shared resources.
- `ansible-pull -U https://git.example/infra.git site.yml` from a timer on hosts that must
  self-heal without a control node.
- Dynamic inventory (`amazon.aws.aws_ec2`, `community.libvirt.libvirt`) when hosts churn.
- `ANSIBLE_STDOUT_CALLBACK=yaml`, `-vvv` for module args, `ANSIBLE_KEEP_REMOTE_FILES=1` to see the generated script.

## Failure modes
- "Missing sudo password": `become` without NOPASSWD → `-K` or fix sudoers.
- "Failed to connect ... Host key verification failed": add host keys first (`ssh-keyscan >> known_hosts`), not `host_key_checking = false` in prod.
- `template`/`copy` `mode: 644` (unquoted) is octal-mangled → `"0644"`.
- Playbook works with `--check` but fails for real: modules that can't predict (commands); add `check_mode: false` where a later task depends on a command's output.
- Python missing on a minimal image: `raw: dnf install -y python3` as a bootstrap play with `gather_facts: false`.

## Verify
- [ ] `ansible-playbook site.yml` twice: second run `changed=0 failed=0`; `ansible-lint` clean.
- [ ] `--check --diff` on a host with a hand-edited file shows exactly the drift you expect.
- [ ] Secrets: `git grep -i password` finds only vault references; `ansible-vault view` works with the team's password source.

## Checked

2026-11-02

- Confirmed: The ansible.builtin module index was fetched and the RHEL 9 system roles guide index.
- Removed or gated: Collection names (ansible.posix, community.general, fedora.linux_system_roles) and ansible.cfg keys are not stated on the fetched index pages (the Ansible user-guide URL returned an empty page); gated, confirm in the Ansible docs.

Method: documentation only; no commands were run.
