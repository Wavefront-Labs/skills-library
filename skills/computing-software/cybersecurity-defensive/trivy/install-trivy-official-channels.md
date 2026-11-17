---
id: computing-software.cybersecurity-defensive.trivy.install-trivy-official-channels
name: install-trivy-official-channels
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [install, installation, docker-image, install-script, homebrew, apt, yum, github-release]
level: intro
status: docs-checked
description: "Install Trivy via official container images, GitHub release archives, the install script, RPM and DEB repositories, Homebrew, Windows zip or FreeBSD pkg."
sources:
  - https://trivy.dev/latest/docs/getting-started/installation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The installation page labels each channel Official or Community; only Official ones are supported by the Trivy team.

Container images: `docker.io/aquasec/trivy`, `ghcr.io/aquasecurity/trivy` and `public.ecr.aws/aquasecurity/trivy`. Mount a persistent cache directory from the host, and to scan container images mount the container engine socket:

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock -v <HOST_CACHE_DIR>:/root/.cache/ aquasec/trivy:<version> image python:3.4-alpine
```

GitHub release: download the archive for your OS and architecture, unpack with `tar -xzf ./trivy.tar.gz`, then `chmod +x ./trivy`.

Install script: `curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin <version>`.

RHEL/CentOS: add a `trivy.repo` file to `/etc/yum.repos.d` (baseurl under `aquasecurity.github.io/trivy-repo/rpm/releases/$basearch/`, `gpgcheck=1`), then `sudo yum -y install trivy`; or install the release `.rpm` directly with `rpm -ivh`.

Debian/Ubuntu: import the GPG key with `gpg --dearmor` into `/usr/share/keyrings/trivy.gpg`, add `deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main` to `/etc/apt/sources.list.d/trivy.list`, then `apt-get install trivy`; or `dpkg -i` the release `.deb`.

Others: `brew install trivy` (macOS, Linux), a Windows zip from the releases page, `pkg install trivy` on FreeBSD. Pacman, zypper, MacPorts, Nix, asdf and mise are Community channels.

## Checked

2026-11-03. Read and confirmed against the Installing Trivy page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
