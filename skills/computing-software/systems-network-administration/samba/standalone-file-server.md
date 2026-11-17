---
id: computing-software.systems-network-administration.samba.standalone-file-server
name: standalone-file-server
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, standalone-file-server, standalone, guest-share, smbpasswd, smb-conf]
level: intro
status: docs-checked
description: "Set up a standalone Samba file server with an authenticated share and a guest share: smb.conf, local users with smbpasswd, SELinux contexts, permissions, testing."
sources:
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_a_Standalone_Server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# standalone file server
smb.conf:
```
[global]
        log file = /var/log/samba/%m
        log level = 1
        server role = standalone server
        map to guest = Bad User

[guest]
        path = /srv/samba/guest/
        read only = no
        guest ok = yes
        guest only = yes

[demo]
        path = /srv/samba/demo/
        read only = no
        inherit permissions = yes
        ; valid users = @demoGroup
```
`workgroup` defaults to `WORKGROUP`.

Users: the local account must be enabled, then add a Samba password:
```
useradd -M -s /sbin/nologin demoUser
passwd demoUser
smbpasswd -a demoUser
groupadd demoGroup
usermod -aG demoGroup demoUser
```
Directories and permissions:
```
mkdir -p /srv/samba/guest/ /srv/samba/demo/
chown -R nobody:nogroup /srv/samba/guest/
chgrp -R demoGroup /srv/samba/demo/
chmod 2770 /srv/samba/guest/ /srv/samba/demo/
```
If SELinux enforces: `semanage fcontext -a -t samba_share_t "/srv/samba/demo(/.*)?"` then `restorecon -Rv /srv/samba/demo/`.

Verify: `testparm -s` after every edit, then `smbclient -U demoUser //SA/demo`; the guest login to `demo` should fail with `NT_STATUS_ACCESS_DENIED`.

## Checked
2026-11-04: both smb.conf examples, user and group commands, directory permissions, the SELinux commands and the testing steps compared with the Setting up Samba as a Standalone Server wiki page. Nothing removed.
Method: documentation only; no commands were run.
