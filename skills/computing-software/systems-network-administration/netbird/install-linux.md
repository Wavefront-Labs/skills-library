---
id: computing-software.systems-network-administration.netbird.install-linux
name: install-linux
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, install-linux, install-script, apt, dnf, rpm-ostree, homebrew]
level: intro
status: docs-checked
description: "Install the NetBird client on Linux via script, APT, DNF, Homebrew, rpm-ostree or binary, then verify, update and log in with SSO or a setup key."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/get-started/install/linux.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Quickest path on any distro:

```
curl -fsSL https://pkgs.netbird.io/install.sh | sh
```

Package options:
- Ubuntu/Debian: add the repo, `sudo apt-get update`, `sudo apt-get install netbird`.
- Fedora/RHEL 10+/Amazon Linux 2023: repo at `https://pkgs.netbird.io/yum/`, then `sudo dnf install netbird`. RHEL 9 / Amazon Linux 2 use `yum` (CLI only).
- Silverblue/Universal Blue: `rpm-ostree install netbird`, reboot, `systemctl enable --now netbird`.
- Homebrew (CLI only): `brew install netbirdio/tap/netbird`, then `netbird service install` and `netbird service start` with sudo.
- Binary: extract the tarball, put `netbird` in `/usr/bin`, run `sudo netbird service install` and `sudo netbird service start`.

The desktop app (`netbird-ui`) needs GTK 4.10+ and WebKitGTK 6.0 and is x86_64 only; on older systems install the CLI only.

Verify: `netbird status`. To check the peer IP, run `ip addr show wt0`.

Log in:
- SSO: run `netbird up` and finish browser authentication.
- Setup key: `netbird up --setup-key <KEY>`; for self-hosted add `--management-url <URL>`.

Update (script installs): `netbird down`, download `install.sh` from `https://pkgs.netbird.io/install.sh`, run `./install.sh --update`, then `netbird up`. Package-manager installs update through the package manager.

With the Homebrew install on Fedora-based systems (including Universal Blue), SELinux may block the binary; the page gives `semanage fcontext` and `restorecon` fixes.

## Checked

2026-11-04. Confirmed against the NetBird Linux installation page: install script, APT, DNF and YUM repositories, rpm-ostree, Homebrew, binary install, desktop app requirements, update steps, SSO and setup key login. Narrowed the SELinux line to the Homebrew case and replaced the unstated claim about the interface name with the page's `ip addr show wt0` check.
Method: documentation only; no commands were run.
