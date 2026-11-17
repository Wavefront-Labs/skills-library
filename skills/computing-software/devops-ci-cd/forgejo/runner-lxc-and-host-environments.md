---
id: computing-software.devops-ci-cd.forgejo.runner-lxc-and-host-environments
name: runner-lxc-and-host-environments
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [lxc-runner, lxc-helpers, host-runner, runner-isolation]
level: advanced
status: docs-checked
description: "Prepare an LXC or host execution environment for the runner and know the isolation limits."
sources:
  - https://forgejo.org/docs/latest/admin/actions/installation/binary/
  - https://forgejo.org/docs/latest/admin/actions/configuration/
  - https://forgejo.org/docs/latest/user/actions/advanced-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
LXC: the runner needs passwordless sudo for all `lxc-*` commands on a Debian bookworm system with LXC installed. The docs use the lxc-helpers scripts:

```
git clone https://code.forgejo.org/forgejo/lxc-helpers
sudo cp -a lxc-helpers/lxc-helpers{,-lib}.sh /usr/local/bin
lxc-helpers.sh lxc_container_create myrunner
lxc-helpers.sh lxc_container_start myrunner
lxc-helpers.sh lxc_container_user_install myrunner 1000 debian
```

The runner can then be installed inside the container. Bookworm is needed for multiarch Go builds and binfmt. Warning: LXC containers do not give a security level that makes them safe for potentially malicious users; they isolate jobs that may accidentally damage the host.

Host: no requirements, and no isolation. A single job can permanently destroy the host, and processes forked out of a job may linger, possibly forever, if the job fails to wait for them.

Label examples from the configuration page: `bookworm:lxc://debian:bookworm:lxc docker` and `self-hosted:host`. LXC defaults are template `debian` and release `bullseye`.

Remember the contrast with the other backends: Docker, Podman and LXC are installed and configured independently of the runner, and services declared in a workflow are supported with the docker backend but not with the lxc backend (Advanced features page).

## Checked

Date: 2026-11-07
Confirmed against the "Installation from binary" page (read in full; LXC and Host sections, the lxc-helpers command list, the two warnings and the bookworm note), the "Forgejo Runner Configuration" page (read in full; LXC and Host label examples and defaults) and the "Forgejo Actions | Advanced features" page (read in full; the services note), the latter two now listed in `sources`. The lxc-helpers repository page was not needed and not relied on.
Corrected: added the two extra sources for the claims that came from them; nothing else needed changing.
Method: documentation only; no commands were run.
