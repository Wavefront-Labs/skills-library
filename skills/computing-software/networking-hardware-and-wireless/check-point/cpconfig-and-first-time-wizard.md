---
id: computing-software.networking-hardware-and-wireless.check-point.cpconfig-and-first-time-wizard
name: cpconfig-and-first-time-wizard
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, cpconfig, first-time-wizard, gateway-install]
level: practitioner
status: draft
description: "Run the Gaia First Time Wizard and cpconfig to set gateway or management role, SIC one-time password, and administrators."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Installation_and_Upgrade_Guide/Default.htm
  - https://www.checkpoint.com/training/certification/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# First Time Configuration Wizard and cpconfig

```
config_system -t /var/tmp/cfg.txt          # unattended, answer file (generate with config_system --dump)
cpconfig                                    # menu: Administrator, GUI Clients, SNMP, Random Pool, Automatic Start, Certificate Authority, Secure Internal Communication
cpconfig  -> "Secure Internal Communication" -> set activation key (one-time password)
cpstop ; cpstart
cplic print
```
- Wizard steps: management interface, hostname, DNS, NTP, then "Products" - choose Security Gateway and/or Security Management (standalone = both). Unattended `config_system` takes `install_security_gw=true`, `install_security_managment=true`, `mgmt_admin_name`, `mgmt_gui_clients_radio=any` (confirm keys).
- For a gateway, `cpconfig` > SIC sets the one-time password; the same string is typed in SmartConsole when you create the gateway object and click Communication.
- On a management server `cpconfig` has "Administrator" (creates the first SmartConsole admin) and "GUI Clients" (the allowed IPs). If SmartConsole says "connection refused", the client IP is missing here.
- Change of hostname or IP after configuration breaks the certificate and SIC; do it before running the wizard where possible.
- Gotcha: choosing the wrong role means reinstalling the image (`clish -c "set ..."` cannot convert).

Verify: `cpstat -f all fw` on the gateway, `cpconfig` shows "Secure Internal Communication"; SmartConsole shows the gateway with `Trust established`. `api status` on the management server shows the API is ready.
