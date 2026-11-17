---
id: computing-software.web-development.vite.troubleshoot-dev-server-network
name: troubleshoot-dev-server-network
category: computing-software
field: web-development
product: vite
tags: [self-signed-cert-caching, header-431, devcontainer-port-forwarding, watch-polling]
level: advanced
status: docs-checked
description: "Fix dev server network issues: self-signed certificates breaking caching, 431 header errors, VS Code port forwarding needing 127.0.0.1, and unwatchable file systems."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Network requests stop loading: with a self-signed SSL certificate Chrome ignores all caching directives, which Vite relies on. Use a trusted certificate. On macOS install one with `security add-trusted-cert -d -r trustRoot -k ~/Library/Keychains/login.keychain-db your-cert.cer`, or set it to Always Trust in Keychain Access.

431 Request Header Fields Too Large: Node.js limits header size (CVE-2018-12121 mitigation). Reduce headers (delete a long cookie) or raise `--max-http-header-size`.

Dev Containers / VS Code port forwarding: set `server.host` to `127.0.0.1`, because VS Code port forwarding does not support IPv6.

Illegal operation error when watching (`EISDIR: illegal operation on a directory, watch ...`): the file system lacks file events (for example a VirtualBox shared folder). Enable `server.watch.usePolling`, which costs high CPU.

WSL2: Vite cannot watch file changes in some conditions; see the `server.watch` option.

## Checked

2026-11-07. Re-read the Vite Troubleshooting guide (docs/guide/troubleshooting.md) in full, Dev Server section. Confirmed the self-signed certificate caching problem and macOS trust command, the 431 error with CVE-2018-12121 and --max-http-header-size, the Dev Containers port forwarding advice (server.host 127.0.0.1), the EISDIR watch error with server.watch.usePolling, and the WSL2 pointer to server.watch. Nothing removed.

Method: documentation only; no commands were run.
