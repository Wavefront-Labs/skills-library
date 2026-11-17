---
id: computing-software.it-support-helpdesk.desktop-support.windows-proxy-and-pac-settings
name: windows-proxy-and-pac-settings
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-networking, proxy-settings, pac-file, wpad, winhttp, netsh-winhttp, wininet, proxy-bypass, ssl-inspection]
level: practitioner
status: docs-checked
description: "Diagnose browsing and app failures caused by proxies: WinINET vs WinHTTP proxy, PAC/WPAD, bypass lists, 'netsh winhttp' and TLS inspection certificate problems."
sources:
  - "https://learn.microsoft.com/en-us/windows/win32/winhttp/netsh-exe-commands"
  - "https://learn.microsoft.com/en-us/defender-endpoint/configure-proxy-internet"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# windows-proxy-and-pac-settings

Goal: work out which proxy a failing app is actually using and fix the
right layer.

## Two proxy stacks
- **WinINET (Internet Options / user proxy settings)** and **WinHTTP** keep
  separate proxy configurations. WinHTTP is configured with netsh, and can
  copy the Internet Explorer/WinINET settings:
  ```cmd
  netsh winhttp show proxy
  netsh winhttp import proxy source=ie      :: copy the IE/WinINET proxy settings
  netsh winhttp set proxy proxy-server="proxy.corp:8080" bypass-list="*.corp.example.com;<local>"
  netsh winhttp reset proxy
  ```
  In `bypass-list`, `<local>` bypasses all short-name hosts; `proxy-server`
  can also be a per-protocol list such as `"http=myproxy;https=sproxy:88"`.
  Run these from an elevated prompt.

## Gotchas
- Compare `netsh winhttp show proxy` with the user-level proxy when a
  browser works but a service or agent cannot connect.
- For Microsoft services behind a proxy, use Microsoft's published endpoint
  lists and bypass guidance for that service (for example Defender for
  Endpoint's proxy configuration page) rather than guessing.

## Verify
`netsh winhttp show proxy` and the browser's effective proxy both match the
intended design, and the failing service reaches its endpoint.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn WinHTTP netsh commands page, as published October 2026. Confirmed: netsh winhttp show proxy, import proxy source=ie, set proxy with proxy-server and bypass-list including <local> and per-protocol lists, reset proxy. Removed: HKCU Internet Settings registry path, PAC and WPAD details (DHCP option 252, wpad DNS name), edge://net-internals, SYSTEM-context and NTLM/Kerberos remarks, Teams/TLS-inspection pinning claims and the PsExec test, none of which a fetched page covers.

Method: documentation only; no commands were run.
