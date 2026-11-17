---
id: computing-software.systems-network-administration.apache-guacamole.build-guacamole-server
name: build-guacamole-server
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, build-from-source, guacamole-server, native-installation, configure, freerdp, libssh2, libvncserver, pango, fonts]
level: practitioner
status: docs-checked
description: "Build and install guacamole-server from source: required and optional -dev packages, ./configure with systemd or init dir, make, make install, ldconfig, and the font gotcha."
sources:
  - https://guacamole.apache.org/doc/gug/guacamole-native.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build guacamole-server (native install)

Required dev packages: Cairo (`libcairo2-dev`), libjpeg-turbo (`libjpeg-turbo8-dev` / `libjpeg62-turbo-dev`), libpng (`libpng-dev`), libtool (`libtool-bin`), libuuid (`uuid-dev`), plus a C compiler.

Optional packages enable features:
- RDP: `freerdp2-dev` (FreeRDP 2.0.0+)
- SSH/SFTP: `libssh2-1-dev`
- SSH, telnet, Kubernetes terminals: `libpango1.0-dev`
- Encrypted web app to guacd link: `libssl-dev`
- VNC: `libvncserver-dev`
- `guacenc` video: libavcodec, libavformat, libavutil, libswscale dev packages
- Also telnet (libtelnet), WebSockets, PulseAudio, Vorbis, WebP

Steps:
```
tar -xzf guacamole-server-1.6.0.tar.gz && cd guacamole-server-1.6.0/
# from git instead: autoreconf -fi first
./configure --with-systemd-dir=/usr/local/lib/systemd/system
# or SysV: ./configure --with-init-dir=/etc/init.d
make
sudo make install
sudo ldconfig
```
Read the "Library status" and "Protocol support" summary printed by configure. A missing required library aborts; a missing optional one means the dependent feature or protocol is not enabled. Install it and re-run configure.

Gotchas:
- If libssl is present, guacd is built with SSL support (see apache-guacamole.guacd-conf-options).
- Terminal protocols need installed fonts; without them syslog shows `Unable to get font "monospace"`.
- `make install` does not start guacd (see apache-guacamole.run-guacd-service).

Verify: the configure summary lists each protocol you need as "yes".

## Checked

2026-11-04. Confirmed against the Guacamole manual page guacamole-native: required and optional dependency packages, FreeRDP 2.0.0 or later for RDP, libssl giving SSL support in guacd, autoreconf -fi for git sources, ./configure with --with-systemd-dir or --with-init-dir, the Library status and Protocol support listing, make, make install and ldconfig, the terminal font requirement with the syslog message, and that starting guacd is a separate step. Reworded: removed the word silently, which the page does not use.

Method: documentation only; no commands were run.
