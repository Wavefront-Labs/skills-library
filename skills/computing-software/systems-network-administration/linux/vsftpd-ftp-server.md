---
id: computing-software.systems-network-administration.linux.vsftpd-ftp-server
name: vsftpd-ftp-server
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vsftpd, ftp-server, ftps, chroot-local-user, passive-mode, sftp-alternative]
level: practitioner
status: docs-checked
description: "Run an FTP or FTPS server with vsftpd: local vs virtual users, chroot jails, passive port ranges through firewalls, TLS, and when to use SFTP instead."
sources:
  - https://security.appspot.com/vsftpd/vsftpd_conf.html
  - https://manpages.debian.org/bookworm/vsftpd/vsftpd.conf.5.en.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# FTP server with vsftpd

Prefer SFTP (OpenSSH `internal-sftp` with `ChrootDirectory`) for anything new. Use vsftpd when legacy devices or partners only speak FTP/FTPS (scanners, PLCs, old ERP exports).

## Install
```bash
# install the vsftpd package of your distribution, then enable and start its service
```

## Baseline /etc/vsftpd.conf (local users, chrooted, FTPS)
```ini
listen=YES
listen_ipv6=NO
anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
chroot_local_user=YES
userlist_enable=YES
userlist_deny=NO                   # only users in /etc/vsftpd.user_list may log in
userlist_file=/etc/vsftpd.user_list
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=40100
pasv_address=203.0.113.10          # public IP when behind NAT
ssl_enable=YES
rsa_cert_file=/path/to/ftp.crt
rsa_private_key_file=/path/to/ftp.key
force_local_logins_ssl=YES
force_local_data_ssl=YES
require_ssl_reuse=NO               # YES requires SSL session reuse on data connections
xferlog_enable=YES
```

## Firewall
Open control port 21 plus the passive range set by `pasv_min_port` and `pasv_max_port`, and set `pasv_address` when the server is behind NAT.

## Virtual users (no shell accounts)
Authenticate through PAM (the service name is set by `pam_service_name`), then set `guest_enable=YES` so non-anonymous logins are remapped to `guest_username`, and use `user_config_dir` for per-user overrides such as `local_root`.

## Verify
- [ ] An FTPS client logs in as a listed user, lists a directory and uploads a test file.
- [ ] A user not in the user_list is rejected; `cd /` stays inside the chroot.
- [ ] A plain-text login without TLS is refused.

## Checked

Documentation check. Checked 2026-10-27 against the upstream vsftpd.conf page (security.appspot.com) and the Debian bookworm vsftpd.conf(5) page: `listen`, `listen_ipv6`, `anonymous_enable`, `local_enable`, `chroot_local_user`, `userlist_enable`, `userlist_deny`, `userlist_file`, `pasv_enable`, `pasv_address`, `ssl_enable`, `rsa_cert_file`, `rsa_private_key_file`, `force_local_logins_ssl`, `force_local_data_ssl`, `require_ssl_reuse`, `guest_enable`, `guest_username`, `user_config_dir` and `local_root`. Removed `allow_writeable_chroot` and `ssl_tlsv1_2` and the matching OOPS error text because neither checked page documents them, plus the SELinux, firewalld, conntrack, PAM module, package and lftp specifics.
Method: documentation only; no commands were run.
