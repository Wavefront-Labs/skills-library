---
id: computing-software.systems-network-administration.cisco-networking.file-transfer-tftp-scp-and-verify
name: file-transfer-tftp-scp-and-verify
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, tftp, ftp, scp, scp-server, verify-md5, verify-sha512, ip-tftp-source-interface, ip-ftp-username, copy-command, ios-file-system, config-backup, ip-scp-server-enable]
level: practitioner
status: draft
description: "Move IOS images and configs on and off Cisco devices with TFTP, FTP, SCP and HTTP: source interfaces, VRFs, size limits, SCP server setup and hash verification."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fundamentals/configuration/xe-16/fundamentals-xe-16-book/cf-config-files.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_ssh/configuration/xe-16/sec-usr-ssh-xe-16-book/sec-secure-copy.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# File transfer with TFTP/FTP/SCP and verifying it

## Which protocol
| Protocol | Use | Caveat |
|---|---|---|
| TFTP (UDP 69) | quick lab copies, configs | no auth, no encryption, many servers cap at 32 MB (block-number rollover) |
| FTP (TCP 21) | large images from a server | cleartext credentials |
| SCP (TCP 22) | default for production | needs SSH and AAA authorization on the device |
| HTTP/HTTPS | big images fast | `ip http client source-interface` |

## Device as client
```
ip tftp source-interface Vlan99        ! or GigabitEthernet0/0 in Mgmt-vrf
ip ftp source-interface Vlan99
ip ftp username backup
ip ftp password <FTP_PASSWORD>
copy running-config tftp://<SERVER>/r1.cfg
copy ftp://<SERVER>/cat9k_iosxe.17.12.04.SPA.bin flash:
copy scp://<USER>@<SERVER>/images/<IMAGE>.bin flash:
copy tftp://<SERVER>/r1.cfg running-config      ! MERGES, it does not replace
```
On management VRF interfaces add `vrf Mgmt-vrf` where supported, e.g. `ip tftp
source-interface GigabitEthernet0/0` with the copy URL reachable in that VRF.

## Device as SCP server (push from a laptop)
```
ip scp server enable
aaa new-model
aaa authentication login default local
aaa authorization exec default local     ! SCP fails with "Privilege denied" without this
username admin privilege 15 secret <SECRET>
```
From the laptop: `scp -O <IMAGE>.bin admin@<SWITCH>:flash:<IMAGE>.bin`. Modern OpenSSH
uses SFTP by default; `-O` forces the legacy SCP protocol that IOS expects.

## Verify integrity
```
verify /md5 flash:<IMAGE>.bin
verify /sha512 flash:<IMAGE>.bin
verify flash:<IMAGE>.bin            ! embedded signature check on signed images
```
Compare with the hash on software.cisco.com. A short copy (e.g. TFTP stalled at 33,554,432
bytes) fails the hash; re-copy with SCP/FTP/HTTP.

## Gotchas
- `copy tftp running-config` merges: lines absent from the file stay. Use `configure replace`
  for a full swap.
- Interrupted copies leave a partial file that still shows in `dir`. Delete it before retrying.
- Large copies on slow links: increase `ip tcp window-size` or use HTTP; avoid console logging
  storms during the transfer.

## Verify
- [ ] `dir flash:` size equals the source file size.
- [ ] `verify /sha512` matches the published hash.
- [ ] Backup file opens on the server and contains `end` as the last line.
