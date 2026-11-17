---
id: computing-software.cloud-infrastructure-engineering.ansible.services-on-sysvinit-and-openrc
name: services-on-sysvinit-and-openrc
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, services-systemd, sysvinit, openrc, service-mgr, runit, service-module]
level: practitioner
status: docs-checked
description: "Manage services on non-systemd hosts (SysV init, OpenRC on Alpine/Gentoo, runit) with ansible.builtin.service, sysvinit and openrc modules, and detect the service manager."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/sysvinit_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/service.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/sysvinit.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/service_facts.py", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/runit.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Services on SysV init and OpenRC

`ansible.builtin.service` normally uses the `ansible_service_mgr` fact to pick a backend and falls back to
`ansible.legacy.service` (module docs); `use` forces a specific one.

```yaml
- ansible.builtin.debug: {var: ansible_facts.service_mgr}
```

## Generic
```yaml
- ansible.builtin.service:
    name: nginx
    state: started
    enabled: true
    use: "{{ 'openrc' if ansible_facts.os_family == 'Alpine' else 'auto' }}"
```
`use:` (default `auto`) forces a specific backend module.

## SysV init specifics
```yaml
- ansible.builtin.sysvinit:
    name: legacy-app
    state: started
    enabled: true
    runlevels: [3, 5]
    sleep: 2                  # seconds between stop and start on restart or reload (default 1)
    pattern: legacy-app.jar   # process match if the init script has no working 'status'
```
Install the init script first. `runlevels` overrides the runlevels set by the package or init script; not all init
scripts support `restarted` or `reloaded` natively, so the module then does a stop and start. `daemonize: true` helps with
badly written init scripts that hold the tty.

## OpenRC (Alpine, Gentoo)
```yaml
- ansible.builtin.service:
    name: nginx
    state: started
    enabled: true
    runlevel: default         # OpenRC runlevel (service module option)
```
`runlevel` is only for OpenRC init scripts (it is ignored on systemd hosts). The service module's code uses `rc-service`
and `rc-update` when `rc-service` is found.

## runit / s6
`community.general.runit` exists for runit. For other supervisors with no module, use `command` with a suitable
`changed_when`.

## Querying
`ansible.builtin.service_facts` populates `ansible_facts.services`; its support depends on the fact-gathering plugin for each platform.

## Gotchas
- If a service does not respond to the status command, `pattern` names a substring to look for in `ps` output as a stand-in for status.

## Verify
- [ ] A second run reports no change and the service is running.

## Checked
Checked 2026-10-26 against ansible-core devel `service.py`, `sysvinit.py`, `service_facts.py` and community.general
`runit.py`. Confirmed: `use` default and fallback, `runlevel` (OpenRC only), `sleep`, `pattern`, `runlevels`, `daemonize`,
rc-service/rc-update usage in code, `service_facts` platform note. Removed unconfirmed claims: container detection problems,
chkconfig/update-rc.d and LSB header requirements, softlevel file, s6 advice, WSL behaviour, and the status-command failure texts.
Method: documentation only; no commands were run.
