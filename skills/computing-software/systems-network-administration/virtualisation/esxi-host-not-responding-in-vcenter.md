---
id: computing-software.systems-network-administration.virtualisation.esxi-host-not-responding-in-vcenter
name: esxi-host-not-responding-in-vcenter
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [host-not-responding, vpxa, hostd, host-disconnected, port-902, heartbeat, vsphere-troubleshooting, vmware, esxi, vcenter]
level: practitioner
status: docs-checked
description: "Troubleshoot ESXi hosts Not Responding or Disconnected in vCenter: heartbeats, port 902/443 checks, restarting hostd and vpxa safely, and the other causes Broadcom lists."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1003409
  - https://knowledge.broadcom.com/external/article?legacyId=1003490
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi host "Not Responding" or "Disconnected" in vCenter

**Goal:** restore vCenter management of a host, working through the causes in order.

## Symptoms the Broadcom article lists
- Host shows not responding or disconnected; its VMs are greyed out in vCenter.
- Monitor > Event shows "Cannot synchronize host <fqdn>".
- vpxd.log shows `FixNotRespondingHost failed ... marking host as notResponding` or a
  connection state change to NO_RESPONSE; ESXi `/var/run/log/vpxa.log` shows
  `Can't connect to hostd. Shutting down.`
- The DCUI reports "hostd detected to be non-responsive".

Causes named: hostd or vpxa unresponsive; packet loss, unreachable gateway, LACP (LAG)
misconfiguration, management network problems, a physical switch feature such as Duplicate
MAC Address Suppression; storage latency or APD/PDL; host memory or CPU contention; a
vCenter snapshot revert or restore from backup. If vCenter gets no heartbeats from the host
it goes to not responding.

## Checks, in the article's order
The article says to work the steps in order, not skip any, and to try reconnecting the host
after each.
1. Check the host is reachable from vCenter or the vSphere Client and whether Connect works.
2. Check the host responds to vCenter at the correct managed IP address.
3. Packet-capture (pktcap-uw) while pinging the default gateway from the DCUI to find where
   packets drop; a drop in the physical network goes to the network team.
4. Check connectivity vCenter to host by IP and FQDN, and on TCP/UDP port 902 and 443.
5. Restart the management agents (below).
6. Check whether hostd has stopped responding.
7. If restarting agents fails, a hard power cycle through the server console (for example
   CIMC or iDRAC) is the article's next step; it reinitialises the ESXi kernel.
8. Check for a purple diagnostic screen and for storage problems (Fibre Channel, iSCSI, NFS).
9. Check the LAG configuration, that `/etc/vmware/vpxa/vpxa.cfg` lists the vCenter IP, that
   there is no MTU mismatch between the management vmk and vCenter, that the ESXi version is
   not higher than vCenter, and that `/var/run/log/vobd.log` shows no duplicate IP.

## Restarting management agents
Warning from the article: do not use `services.sh restart` or the DCUI "Restart Management
Agents" on hosts running vSAN (`esxcli vsan cluster get`), using LACP
(`esxcli network vswitch dvs vmware lacp status get`), with NSX
(`esxcli software vib list | grep -E 'nsx|vsipfwlib'`) or with shared graphics (vGPU, vDGA,
vSGA). Restart single services only. A restart can cause temporary disruption, instability
needing a host reboot, and affect running tasks and guest performance.
- Host Client: Host > Manage > Services, select vpxa or hostd and restart it.
- SSH or ESXi Shell: `/etc/init.d/hostd restart`, then `/etc/init.d/vpxa restart`. Allow
  1 to 2 minutes, then check the host shows Connected. If a service will not restart,
  inspect `/var/log/hostd.log`.

## Verify
The vSphere Client shows the host as Connected after the agents have had 1 to 2 minutes
to re-initialise.

## Checked
Date: 2026-11-07. Read both Broadcom KB articles in full: "ESXi host not responding or
disconnected" (symptoms, causes, resolution steps) and "Restarting Management Agents in
ESXi" (warning, Host Client and SSH procedures). Linked sub-articles (pktcap-uw, hostd
troubleshooting and others) were not opened. Removed as not on the pages: the UDP 902 10 s
and 60 s heartbeat timings, the DCUI menu path, `status` and `tail` commands, vdf and
ramdisk inode checks, certificate/thumbprint advice, the remove-from-inventory warning and
the HA agent verify step.
Method: documentation only; no commands were run.
