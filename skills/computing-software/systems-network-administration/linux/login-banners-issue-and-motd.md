---
id: computing-software.systems-network-administration.linux.login-banners-issue-and-motd
name: login-banners-issue-and-motd
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, login-banner, issue, issue-net, motd, update-motd, sshd-banner, pam-motd, cis-benchmark, legal-notice, sysadmin]
level: practitioner
status: docs-checked
description: "Show legal and operational notices at login: /etc/issue (console, escape codes), /etc/issue.net and sshd Banner (pre-auth), /etc/motd and dynamic MOTD (post-auth), CIS rules."
sources:
  - https://man7.org/linux/man-pages/man5/issue.5.html
  - https://man7.org/linux/man-pages/man8/agetty.8.html
  - https://man7.org/linux/man-pages/man5/sshd_config.5.html
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_motd/pam_motd.8.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Login banners: issue, issue.net, motd

**Goal:** a warning banner before authentication (legal requirement in many orgs), useful
host information after login, and no information leakage to unauthenticated users.

## 1. Which file shows where
| File | Shown | When |
|---|---|---|
| `/etc/issue` (+ `/etc/issue.d/*.issue`) | local console (agetty) | before login prompt |
| `/etc/issue.net` | SSH **only if** `Banner /etc/issue.net` is set | before authentication |
| sshd `Banner <file>` | SSH clients | before authentication |
| `/etc/motd` (+ `/run/motd`, `motd.d/` directories) | after successful login (pam_motd or sshd `PrintMotd`) | post-auth |

## 2. Pre-login warning
```
Authorized uses only. All activity may be monitored and reported.
```
```bash
cp banner.txt /etc/issue.net; cp banner.txt /etc/issue
echo 'Banner /etc/issue.net' > /etc/ssh/sshd_config.d/10-banner.conf
sshd -t && systemctl reload sshd
chmod 644 /etc/issue /etc/issue.net /etc/motd; chown root:root /etc/issue /etc/issue.net /etc/motd
```
Avoid putting the OS name, version or kernel (`\S`, `\s`, `\r`, `\v`, `\m` agetty escapes) in a pre-login
banner: it reveals host details to unauthenticated users. Check your hardening baseline for its exact banner rules.
agetty escapes (agetty(8)) are useful on internal consoles: `\4{eth0}` IPv4 address, `\n` hostname, `\l` tty line.
agetty also reads `/etc/issue.d/*.issue` and, since util-linux 2.35, `/run/issue` and `/usr/lib/issue` locations.

## 3. Post-login MOTD
- Static: `/etc/motd`.
- `pam_motd` shows `/etc/motd` (else `/run/motd`, else `/usr/lib/motd`) and the files in the `motd.d` directories
  under `/etc`, `/run` and `/usr/lib`; it must be enabled in the PAM stack of the login service.
- Distribution-specific dynamic MOTD schemes (for example script directories) are built on this; see your
  distribution's documentation.
- Avoid duplicates: if PAM shows motd, set `PrintMotd no` in sshd_config.

## 4. GUI login
Graphical greeters have their own banner settings (for GDM, through dconf); see the desktop's documentation.

## Gotchas
- Slow MOTD scripts (network calls) delay every SSH login; keep them local and fast.

## Verify
- [ ] `ssh host` shows the banner before the password/key prompt.
- [ ] Console login shows the sanitized `/etc/issue`; post-login shows the motd once.
- [ ] Your compliance scan passes the banner rules.

## Checked

Checked 2026-10-27 against util-linux agetty(8) source (issue files and escape codes), OpenSSH sshd_config(5) source (Banner, PrintMotd), linux-pam pam_motd(8) source, current master, 2026-10-27. Confirmed: agetty issue file locations and /etc/issue.d/*.issue, escape codes \4{iface}, \n, \l, \S and others, sshd Banner is sent before authentication and off by default, PrintMotd and its caveat, pam_motd file and directory search order. Removed or softened: CIS benchmark rule wording (paywalled), telnet remark, Ubuntu update-motd details, GDM dconf keys, ssh -q and ASCII gotchas.

Method: documentation only; no commands were run.
