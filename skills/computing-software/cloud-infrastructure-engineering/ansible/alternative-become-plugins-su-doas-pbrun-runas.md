---
id: computing-software.cloud-infrastructure-engineering.ansible.alternative-become-plugins-su-doas-pbrun-runas
name: alternative-become-plugins-su-doas-pbrun-runas
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, become, become-plugins, become-method, su, doas, pbrun, dzdo, runas, ksu, pfexec, machinectl, sesu, enable, community-general-become, windows-runas, openbsd, powerbroker, centrify]
level: practitioner
status: docs-checked
description: "Use a become plugin other than sudo: su, doas, pbrun/dzdo/sesu, runas on Windows, machinectl, enable on network devices; the flags, prompts and passwords each needs."
sources: ["https://docs.ansible.com/ansible/latest/plugins/become.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/plugins/become/su.py", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/plugins/become/runas.py", "https://github.com/ansible-collections/community.general/tree/main/plugins/become", "https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/become/enable.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alternative become plugins (su, doas, pbrun, runas)

List what is installed: `ansible-doc -t become -l`. Core ships `sudo`, `su`, `runas`;
`community.general` adds `doas`, `pbrun`, `dzdo`, `sesu`, `ksu`, `pfexec`, `machinectl`;
`ansible.netcommon.enable` is for network devices.

## 1. su — sites with a root password and no sudo
```yaml
ansible_become_method: su
ansible_become_user: root
ansible_become_password: "{{ vault_root_password }}"   # root's password, not the login user's
ansible_become_flags: ""                                 # extra su options, for example "-l" for a login shell
```
The command built is `su <flags> <user> -c '<command>'`. Prompt detection uses a built-in list of
localised prompts (`Password`, `Mot de passe`, `Contraseña` and many others); for a language not in the
list, add it with `[su_become_plugin] localized_prompts` (env `ANSIBLE_SU_PROMPT_L10N`, var
`ansible_su_prompt_l10n`). Do not end a custom entry with a colon: Ansible adds the colon itself, and a
doubled colon makes the prompt match fail with a timeout.

## 2. doas — OpenBSD, Alpine, some hardened Linux
```yaml
ansible_become_method: community.general.doas
ansible_become_flags: -n       # non-interactive; requires a "permit nopass" rule in doas.conf
```
The plugin adds `-n` itself when no become password is set and the flags do not already contain it; with a
password, doas prompts and Ansible answers with `ansible_become_password`.

## 3. PowerBroker / Centrify / CA PAM
```yaml
ansible_become_method: community.general.pbrun      # BeyondTrust PowerBroker
ansible_become_flags: ""                            # the plugin matches the prompt "Password:"
ansible_become_exe: /usr/local/bin/pbrun
# Centrify: community.general.dzdo (default flags -H -S -n)
# CA Privileged Access Manager: community.general.sesu
```
Test with `ansible host -b -m command -a id -vvv` and read the exact wrapped command.

## 4. runas — Windows
```yaml
- ansible.windows.win_command: whoami
  become: true
  become_method: runas
  become_user: svc_deploy
  vars:
    ansible_become_password: "{{ vault_svc_deploy }}"
    ansible_runas_flags: logon_type=batch   # key=value pairs: logon_type and logon_flags only
```
`logon_type` accepts interactive, network, batch, service, unlock, network_cleartext and new_credentials;
`logon_flags` accepts none, with_profile and netcredentials_only. The plugin is implemented in the PowerShell
module handler and the plugin notes say it works only with winrm connections; the Secondary Logon service
(seclogon) must be running; `become_exe` is ignored.

## 5. machinectl, pfexec, ksu
- `community.general.machinectl`: runs `machinectl -q shell <flags> <user>@ <command>`. When the target user is not
  root it needs a polkit rule, and it does not work with connection pipelining.
- `community.general.pfexec`: profile-based execution; it ignores `become_user` and uses `exec_attr`.
- `community.general.ksu`: Kerberos substitute user (`ksu`).

## 6. enable — network devices
```yaml
ansible_connection: ansible.netcommon.network_cli
ansible_become: true
ansible_become_method: ansible.netcommon.enable
ansible_become_password: "{{ enable_secret }}"
```

## Gotchas
- Only one become method per task; chaining `su` then `sudo` means two tasks or a `command` with the inner wrapper.
- `pbrun` and `su` rely on prompt matching, so unexpected text printed before the prompt can cause a timeout.
- Collection become plugins need the FQCN unless the collection is listed in `collections:`.

## Verify
- [ ] `ansible host -b -m command -a id -vvv` shows the expected wrapper (`su root -c`, `doas -n`, `pbrun`...) and `uid=0`.
- [ ] A deliberately wrong `ansible_become_password` fails with an authentication error rather than hanging until timeout.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in plugins/become/su.py: command form `su <flags> <user> -c <cmd>`, built-in localised prompt list including Contraseña, `localized_prompts` ini key and env/var names, warning not to add a colon; plugins/become/runas.py: `logon_type` and `logon_flags` values, winrm-only note, seclogon requirement, become_exe ignored.
- Confirmed in community.general become plugins: doas adds `-n` automatically without a password; pbrun prompt "Password:"; dzdo default flags `-H -S -n`; machinectl command form, polkit note and pipelining incompatibility; pfexec ignores become_user; ksu, sesu and dzdo descriptions; ansible.netcommon enable plugin exists.
- Core ansible-core 2.22 ships only sudo, su and runas become plugins (directory listing).
- Removed unconfirmed claims: Windows privilege requirements, SYSTEM needing no password, policy-server remarks, secure_path remark.

Method: documentation only; no commands were run.
