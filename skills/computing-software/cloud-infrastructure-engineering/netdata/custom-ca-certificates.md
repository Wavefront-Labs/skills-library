---
id: computing-software.cloud-infrastructure-engineering.netdata.custom-ca-certificates
name: custom-ca-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, custom-ca, tls-intercepting-proxy, update-ca-certificates]
level: advanced
status: docs-checked
description: "Make the Netdata Agent trust a private or corporate CA on Linux distros, Docker and Windows, including the Windows go.d tls_ca and streaming caveats."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/configuration/using-custom-ca-certificates-with-netdata.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Certificate must be PEM or DER with a `.crt` extension, readable by all and writable only by root.

- Debian/Ubuntu and Alpine: copy to `/usr/local/share/certificates`, run `sudo update-ca-certificates` (Alpine needs the `ca-certificates` package).
- RHEL/Fedora: copy to `/etc/pki/ca-trust/source/anchors`, run `sudo update-ca-trust`.
- SUSE: `/etc/pki/trust/anchors`, then `sudo update-ca-certificates`.
- Arch: `/etc/ca-certificates/trust-store/anchors`, then `sudo update-ca-trust`.
- Static builds: install into the system trust store before installing Netdata.

Docker custom image:

```
FROM netdata/netdata:stable
RUN mkdir -p /usr/local/share/certificates
COPY local.pem /usr/local/share/certificates
RUN update-ca-certificates
```

Windows (default install under Program Files): copy the cert into `Program Files\Netdata\etc\pki\ca-trust\source\anchors`, then from elevated PowerShell:

```
& "$env:ProgramFiles\Netdata\usr\bin\bash.exe" -lc /usr/bin/update-ca-trust
Restart-Service Netdata
```

Gotchas:
- Re-run `update-ca-trust` after every Agent upgrade; the derived bundles are rebuilt.
- go.d uses the Windows store unless a job sets `tls_ca`.
- Streaming trust: use `CAfile` or `CApath` in `[stream]`, not skip verification.

## Checked

2026-11-04. Confirmed against the Netdata custom CA certificates page: PEM or DER with a .crt extension and the permissions rule, the Debian, Ubuntu, RHEL, Fedora, SUSE, Arch and Alpine directories and commands, static builds installing the certificate before Netdata, the Docker image example, the Windows MSYS2 steps with the bash.exe one-liner and Restart-Service, and the upgrade, go.d tls_ca and streaming caveats. Replaced the drive placeholder with the documented Program Files default.

Method: documentation only; no commands were run.
