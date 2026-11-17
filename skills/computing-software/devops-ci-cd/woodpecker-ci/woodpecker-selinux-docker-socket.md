---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-selinux-docker-socket
name: woodpecker-selinux-docker-socket
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [selinux, docker-socket, permission-denied]
level: advanced
status: docs-checked
description: "Fix Woodpecker agent permission denied errors on the Docker socket under SELinux."
sources:
  - https://woodpecker-ci.org/docs/usage/troubleshooting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker agent and SELinux

On SELinux systems (RHEL, CentOS, Fedora and similar) SELinux can stop the agent reaching the Docker socket. The symptom:

```text
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock
```

Options:

1. Test only: `setenforce 0` sets permissive mode temporarily. To make it permanent, set `SELINUX=permissive` in `/etc/selinux/config`. Use it only to confirm SELinux is the cause.
2. Recommended: build a custom policy module:

```bash
ausearch -c 'docker' -avc | audit2allow -R -o woodpecker-docker.te
checkmodule -M -m -o woodpecker-docker.mod woodpecker-docker.te
semodule_package -o woodpecker-docker.pp -m woodpecker-docker.mod
semodule -i woodpecker-docker.pp
```

3. Relabel the mount with `:z` or `:Z` in Docker or Compose:

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock:z
```

`:z` relabels the content for SELinux. `:Z` relabels it exclusively for this container, so use it with caution.

4. Use Podman instead of Docker, which has better SELinux integration.

## Checked

2026-11-08. Read the Woodpecker Troubleshooting page in full (SELinux section and clone debugging) and confirmed the symptom, the four options and the commands. Removed the claim that Podman is not officially supported and the `DOCKER_HOST` suggestion, which the page does not state, and the "least to most invasive" ordering.

Method: documentation only; no commands were run.
