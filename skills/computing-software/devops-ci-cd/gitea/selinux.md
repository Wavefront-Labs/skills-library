---
id: computing-software.devops-ci-cd.gitea.selinux
name: selinux
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-selinux, gitea, semanage-fcontext, restorecon, ausearch-avc, audit2allow, ambient-capabilities]
level: advanced
status: docs-checked
description: "Run Gitea under SELinux enforcing mode: bind ports below 1024 via systemd ambient capabilities, label the binary and data dir, read AVC denials."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/selinux.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea under SELinux

Applies to Fedora, RHEL, CentOS Stream, Rocky, AlmaLinux and any SELinux-enabled host, for binary or source installs (distro packages ship a fitting policy). Do not disable SELinux: `setenforce 0` is only a test that a failure is SELinux, then `setenforce 1`.

## Ports below 1024
`setcap 'cap_net_bind_service=+ep' /usr/local/bin/gitea` is the least robust choice: the capability sits in an extended attribute and is lost whenever the binary is replaced (every upgrade), and the policy must also allow it for the binary's label. Let systemd grant it instead (the sample unit has these lines commented out):
```ini
[Service]
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
```
Then `sudo systemctl daemon-reload && sudo systemctl restart gitea`. If the capability still does not arrive, add `PrivateUsers=false` (sandboxing otherwise runs the service in a user namespace). Alternatives that avoid privileged ports: a reverse proxy owning 80/443, or a firewall redirect such as `firewall-cmd --permanent --add-forward-port=port=80:proto=tcp:toport=3000`.

## Labels
Needs `policycoreutils-python-utils`. Use `semanage fcontext` plus `restorecon`, not `chcon` (its labels are reverted by the next filesystem relabel):
```sh
sudo semanage fcontext -a -t bin_t '/usr/local/bin/gitea'
sudo restorecon -v /usr/local/bin/gitea
sudo semanage fcontext -a -t var_lib_t '/var/lib/gitea(/.*)?'
sudo restorecon -Rv /var/lib/gitea
```
`/etc/gitea` normally needs nothing. Adjust paths if you did not follow the binary layout.

## Finding denials
Denials go to the audit log, not Gitea's log, so they look like unexplained permission errors:
```sh
sudo ausearch -m AVC -c gitea --start recent
```
For uncovered denials build a local module, but read the `.te` before installing because `audit2allow` writes down everything denied, including denials that were right:
```sh
sudo ausearch -c gitea --raw | audit2allow -M gitea-local
cat gitea-local.te
sudo semodule -i gitea-local.pp
```
If a denial points at a path Gitea should not use at all, fix the path instead.

## Checked
2026-11-03. Every claim confirmed against the Gitea docs page selinux.md (raw markdown, gitea/docs main branch). Nothing removed.
Method: documentation only; no commands were run.
