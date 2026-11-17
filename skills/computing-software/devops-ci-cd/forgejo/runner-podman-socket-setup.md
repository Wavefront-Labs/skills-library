---
id: computing-software.devops-ci-cd.forgejo.runner-podman-socket-setup
name: runner-podman-socket-setup
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [podman-socket, systemd-linger, docker-host, rootless-podman]
level: advanced
status: docs-checked
description: "Run the runner against rootless Podman by enabling podman.socket for the runner user and lingering."
sources:
  - https://forgejo.org/docs/latest/admin/actions/installation/binary/
  - https://forgejo.org/docs/latest/user/actions/advanced-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On recent Linux distributions the `podman` package alone is enough to run containers as the unprivileged runner user; no Docker-compatibility or rootless extras are needed. Some configuration is still needed so the runner is started at boot and can access the Podman service. The docs' steps (Debian 13, likely Ubuntu and other systemd distributions):

1. `sudo apt install podman`
2. Enable the socket for the runner user: `sudo systemctl --user -M runner@ enable --now podman.socket`
3. Check it: `sudo systemctl --user -M runner@ status podman.socket`. The `Listen:` line shows the path, for example `/run/user/1004/podman/podman.sock`.
4. Put that path in the `docker_host` parameter of the `container` section of the runner configuration, for example `docker_host: unix:///run/user/1004/podman/podman.sock` (the `DOCKER_HOST` environment variable also works).
5. Make the socket exist at boot: `sudo loginctl enable-linger runner`.

On non-systemd systems pick any path and run, as the runner user, `podman system service -t 0 unix:///path/to/runner-home/podman.sock`, arranging for it to start at boot via your init system. The page's example puts the socket in the runner user's home directory.

Podman 5 with Pasta networking can break the Actions cache because containers cannot reach the host's primary IP; the Advanced features page suggests either configuring Podman not to copy the host's primary IP, or setting `cache.actions_cache_url_override` (with `proxy_port: 4000`) to `http://host.containers.internal:4000`, which only suits a runner whose back-end is Podman alone because every back-end would receive that cache URL.

## Checked

Date: 2026-11-07
Confirmed against the "Installation from binary" page (read in full, including code blocks and the LXC and host sections that this skill does not use): the Podman section for Debian 13 (trixie), `sudo apt install podman`, `sudo systemctl --user -M runner@ enable --now podman.socket`, the status command and `Listen:` line, `sudo loginctl enable-linger runner`, the non-systemd `podman system service -t 0 unix://...` command, and the `container.docker_host` configuration with `DOCKER_HOST` as an alternative. The Podman 5 / Pasta cache problem and the `host.containers.internal` override were confirmed on the "Forgejo Actions | Advanced features" page (read in full), now listed in `sources`.
Corrected: the first paragraph said configuration is only for boot; the page says it is needed to start the runner at boot and to reach the Podman service. Replaced a vague pointer to "the cache documentation" with the page's actual two options.
Method: documentation only; no commands were run.
