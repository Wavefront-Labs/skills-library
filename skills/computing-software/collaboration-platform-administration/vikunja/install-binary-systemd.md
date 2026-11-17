---
id: computing-software.collaboration-platform-administration.vikunja.install-binary-systemd
name: install-binary-systemd
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, binary-install, gpg-signature, opt-vikunja, systemd-unit]
level: practitioner
status: docs-checked
description: "Install Vikunja from the release zip: verify the GPG signature, unpack to /opt/vikunja, symlink the binary and run it as a systemd service."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Download the build for your architecture from the download page, then verify it. Releases are GPG-signed with key `FF054DACD908493A`:

```
gpg --keyserver keyserver.ubuntu.com --recv FF054DACD908493A
gpg --verify vikunja-<version>-linux-amd64-full.zip.sig vikunja-<version>-linux-amd64-full.zip
```

Install:

```
mkdir -p /opt/vikunja
unzip <vikunja-zip-file> -d /opt/vikunja
chmod +x /opt/vikunja
sudo ln -s /opt/vikunja/vikunja /usr/bin/vikunja
```

Set `service.publicurl` or disable CORS (`cors.enable: false`), since CORS is on by default.

Save a unit at `/etc/systemd/system/vikunja.service` with `After=network.target`, `WorkingDirectory=/opt/vikunja`, `ExecStart=/usr/bin/vikunja`, `Restart=always`, `RestartSec=2s`, `WantedBy=multi-user.target`. Uncomment `Requires=` lines for your database or redis service. For ports below 1024 enable `CapabilityBoundingSet` and `AmbientCapabilities` as `CAP_NET_BIND_SERVICE`.

Then `sudo systemctl enable vikunja` and `sudo systemctl start vikunja`. See the systemd hardening skill for sandboxing.

## Checked

2026-11-04. Confirmed against the Vikunja Installing page (setup/install, Install from binary): signing key and gpg commands, the /opt/vikunja install commands, the CORS and publicurl warning, the systemd unit values and capability lines, and the enable and start commands. Nothing removed.

Method: documentation only; no commands were run.
