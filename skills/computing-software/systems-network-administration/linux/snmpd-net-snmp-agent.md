---
id: computing-software.systems-network-administration.linux.snmpd-net-snmp-agent
name: snmpd-net-snmp-agent
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, snmp, snmpd, net-snmp, snmpv3, snmpwalk, snmpget, mib, usm, vacm, extend, monitoring, sysadmin]
level: practitioner
status: docs-checked
description: "Expose Linux host metrics over SNMP with net-snmp: SNMPv3 users with auth+priv, views restricting what's readable, extend scripts, firewall, and testing with snmpwalk."
sources:
  - https://github.com/net-snmp/net-snmp/blob/master/man/snmpd.conf.5.def
  - https://github.com/net-snmp/net-snmp/blob/master/man/net-snmp-create-v3-user.1.def
  - https://github.com/net-snmp/net-snmp/blob/master/man/snmpcmd.1.def
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# snmpd (net-snmp) on Linux

**Goal:** let the NMS (LibreNMS, Zabbix, PRTG, Observium) poll CPU, memory, disks and
interfaces from a Linux host — over SNMPv3, read-only, from the NMS only.

## 1. Install
```bash
dnf install net-snmp net-snmp-utils      # apt install snmpd snmp (snmp-mibs-downloader for names)
```

## 2. SNMPv3 user (preferred)
```bash
systemctl stop snmpd
net-snmp-create-v3-user -ro -a SHA-512 -A '<auth-pass>' -x AES -X '<priv-pass>' nmsuser
systemctl start snmpd
```
This adds a `createUser` line to the persistent `snmpd.conf` (the line is read, removed and replaced by a localized key at start) and the matching access rule. Passphrases must be at least 8 characters. SHA-2 authentication and AES privacy need an OpenSSL-enabled build (snmpd.conf(5)); `-ro` makes the user read-only. Where the persistent directory is depends on the build.

## 3. snmpd.conf essentials
```
agentaddress udp:161                      # or udp:10.0.10.20:161 to bind one address
view   systemonly included .1.3.6.1.2.1.1
view   systemonly included .1.3.6.1.2.1.2       # interfaces
view   systemonly included .1.3.6.1.2.1.25      # HOST-RESOURCES (storage, processes)
view   systemonly included .1.3.6.1.4.1.2021    # UCD (load, memory, disk)
rouser nmsuser priv -V systemonly
sysLocation  DC1 rack 12
sysContact   ops@example.com
disk / 10%                                  # UCD disk table + error flag below 10 % free
load 12 10 8
extend raidstatus /usr/local/bin/raid-check.sh    # output under NET-SNMP-EXTEND-MIB
```
If v2c is forced by old tooling: `rocommunity <long-random-string> 10.0.99.5 -V systemonly` — source-restricted, never `public`.

## 4. Firewall and test
```bash
firewall-cmd --permanent --add-service=snmp --zone=internal && firewall-cmd --reload   # 161/udp
snmpwalk -v3 -l authPriv -u nmsuser -a SHA-512 -A '<auth-pass>' -x AES -X '<priv-pass>' 10.0.10.20 system
snmpget  -v3 ... 10.0.10.20 UCD-SNMP-MIB::laLoad.1
snmpwalk -v3 ... 10.0.10.20 NET-SNMP-EXTEND-MIB::nsExtendOutputFull
```

## Gotchas
- Check the shipped `snmpd.conf` for community or `com2sec` lines and remove any community you do not need.
- `Timeout: No Response` can be a firewall, a wrong `agentaddress`, or wrong v3 credentials; check the snmpd log.
- Logging: `-LS0-5d` logs priorities 0 to 5 to syslog facility daemon (snmpcmd(1) logging options); set it in the service's snmpd options.

## Verify
- [ ] v3 `snmpwalk` from the NMS returns system, interfaces and UCD values; the same request with a wrong password or from another host fails.
- [ ] `snmpwalk -v2c -c public host` fails unless you configured a community on purpose.

## Checked
2026-10-27. Checked against the Net-SNMP manual sources (snmpd.conf(5), net-snmp-create-v3-user(1), snmpcmd(1)) on the master branch. Confirmed: net-snmp-create-v3-user options -ro, -A, -a (MD5, SHA, SHA-224 to SHA-512), -X, -x (DES, AES, AES128); createUser semantics and the 8-character minimum passphrase; view, agentaddress, rouser syntax with the noauth, auth, priv levels and -V VIEW, rocommunity with a source and -V VIEW, disk PATH and percent, load, extend with NET-SNMP-EXTEND-MIB result tables, sysLocation; snmpcmd -l authPriv and -a and -x; -LS0-5d logging. Changed: rouser level token authpriv to priv (the documented token). Removed: fixed file paths for the persistent configuration, the default-public-community claim, the SELinux remark and the SHA/AES version claim. The Net-SNMP site links in sources use http and the same pages are in the repository manual sources.

Method: documentation only; no commands were run.
