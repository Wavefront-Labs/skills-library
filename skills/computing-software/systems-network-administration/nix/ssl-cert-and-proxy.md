---
id: computing-software.systems-network-administration.nix.ssl-cert-and-proxy
name: ssl-cert-and-proxy
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-ssl-cert-file, proxy, https-intercept]
level: practitioner
status: docs-checked
description: "Install and run Nix behind an HTTPS-intercepting proxy: NIX_SSL_CERT_FILE, ssl-cert-file for the daemon and the proxy variables the installer copies."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/env-variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Behind an HTTPS-intercepting proxy, set `NIX_SSL_CERT_FILE` to your custom certificate bundle. If unset, Nix installs and uses its own bundle.

Before installing:

```
export NIX_SSL_CERT_FILE=/etc/ssl/my-certificate-bundle.crt
curl -L https://nixos.org/nix/install | sh
```

To persist, add the same `export` line to shell profile and rc files such as `/etc/bashrc` and `/etc/zshrc`.

Gotcha: do not add the export to your profile before running the installer. The installer detects existing Nix configuration and aborts.

With the Nix daemon, also add to `/etc/nix/nix.conf`:

```
ssl-cert-file = /etc/ssl/my-certificate-bundle.crt
```

Proxy variables: the installer specially handles `http_proxy`, `https_proxy`, `ftp_proxy`, `all_proxy`, `no_proxy` and their uppercase forms. If any is set during install, it creates `/etc/systemd/system/nix-daemon.service.d/override.conf` so `nix-daemon` uses them.

## Checked

2026-11-04: NIX_SSL_CERT_FILE behaviour, install order warning, rc-file persistence, ssl-cert-file, the proxy variable list and the systemd override file confirmed against the Environment Variables manual page. Removed the Verify line (daemon-reload and TLS check), which the page does not state.

Method: documentation only; no commands were run.
