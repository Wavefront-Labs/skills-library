---
id: computing-software.networking-hardware-and-wireless.check-point.cpuse-upgrade-and-jumbo-hotfix
name: cpuse-upgrade-and-jumbo-hotfix
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, cpuse, jumbo-hotfix, upgrade]
level: practitioner
status: draft
description: "Install Jumbo Hotfix and upgrade packages with CPUSE (clish installer), verify, and sequence cluster member upgrades."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Installation_and_Upgrade_Guide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Gaia_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CPUSE: upgrades and Jumbo Hotfix installation

```
clish -c "show installer status build"
clish -c "show installer packages available-for-download"
clish -c "installer download-and-install 3"      # number from the list; or: installer download <n>
clish -c "installer verify 3"
clish -c "show installer package 3"
clish -c "installer import local /var/tmp/Check_Point_R81.20_T99_sk.tar"
cpinfo -y all ; installed_jumbo_take
```
- CPUSE (Check Point Upgrade Service Engine) installs hotfixes (Jumbo, GA fixes) and upgrades. Always run **Verifier** (`installer verify`) before installing; it checks prerequisites and conflicts.
- Take a **snapshot** first (`add snapshot`), because uninstalling a Jumbo can be done (`installer uninstall`) but a full upgrade cannot be undone except by snapshot revert.
- Cluster order: upgrade the **standby** member, make sure it joins and syncs (`cphaprob stat` shows Standby, `fw ctl pstat`), failover to it (`clusterXL_admin down` on the old active), then upgrade the former active. Members on different versions use Full HA mode compatibility; check the release notes for minimum versions allowed in the cluster (confirm).
- Management first: upgrade the management server before the gateways it manages; gateways cannot be newer than the management.
- Installation reboots the box when the package requires it; plan the window. The log is `/var/log/CPUSE/` (`dasdebug`).
- Gotcha: CPUSE needs HTTPS access to the Check Point download servers; offline: download the package and `installer import local`.

Verify: `show installer status build` shows `Succeeded`; `installed_jumbo_take` increments; `cphaprob stat` and `fw stat` after reboot.
