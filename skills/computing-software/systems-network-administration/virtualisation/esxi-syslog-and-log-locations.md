---
id: computing-software.systems-network-administration.virtualisation.esxi-syslog-and-log-locations
name: esxi-syslog-and-log-locations
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-syslog, vmkernel-log, hostd-log, vpxa-log, syslog-forwarding, log-retention, vsphere-monitoring, vmware, esxi, vsphere]
level: practitioner
status: docs-checked
description: "Know which ESXi log answers which question (vmkernel, hostd, vpxa, vobd, auth, vmware.log), forward to a remote syslog over TLS, and keep logs persistent."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-monitoring-and-performance-8-0/system-log-files.html
  - https://knowledge.broadcom.com/external/article?legacyId=2003322
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi syslog forwarding and log locations

**Goal:** logs survive host reboots and failures, land in the SIEM, and you know which
file to open first.

## Where to look
The ESXi Log File Locations page of the monitoring guide maps each log to what it
answers: the vmkernel log (storage paths, NIC link, driver errors), the host agent log
(VM power ops, snapshots, client sessions), the vCenter agent (vpxa) log on managed
hosts, logins and shell audit, the vSphere HA agent, and the per-VM log. View them from
the DCUI (View System Logs), the host client, or over SSH.

## Forward
```sh
esxcli system syslog config set --loghost='tcp://<siem>:514,udp://<backup-syslog>:514'
esxcli system syslog reload
esxcli network firewall ruleset set -r syslog -e true
esxcli system syslog mark -s "syslog test from $(hostname)"
```
If you forward over TLS, the SIEM certificate must be trusted by the host (or use vCenter
host certificate management). The same syslog configuration can be applied to a cluster
of similar hosts with Host Profiles (KB 2003322).

## Persistent local logs
On hosts booting from SD/USB without persistent OSDATA, logs are in RAM and lost on
reboot. Point `esxcli system syslog config set --logdir` at a datastore directory and add
`--logdir-unique` for per-host subdirectories (KB 2003322).
Increase rotation for busy logs if needed.

## Gotchas
- UDP syslog drops under load; TCP/TLS preferred.
- Time skew makes correlation impossible; NTP on every host.
- The vCenter can also forward its own logs (VAMI → Syslog).

## Verify
The test mark appears in the SIEM from every host; `esxcli system syslog config get` shows
the remote hosts and a persistent log directory.

## Checked
2026-10-31: `esxcli system syslog config set` with `--loghost`, `--logdir` and `--logdir-unique`, `esxcli system syslog reload`, the `esxcli system syslog mark` test, the Host-Profiles path for cluster-wide syslog, and the firewall note confirmed in KB 2003322; the View System Logs / ESXi Log File Locations topics and the vpxa agent log on managed hosts confirmed in the monitoring guide's System Log Files section. Removed unconfirmed specifics: the log-file name table (left as a pointer to ESXi Log File Locations), `ssl://` and the castore.pem path, the `Syslog.global.*` setting names, the logger rotation example and the three-target limit.
Method: documentation only; no commands were run.
