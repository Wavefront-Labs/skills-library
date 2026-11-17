---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-network-troubleshooting-tcpping-and-nameresolver
name: app-service-network-troubleshooting-tcpping-and-nameresolver
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service, tcpping, nameresolver, network-troubleshooter, vnet-integration, outbound-connectivity]
level: practitioner
status: docs-checked
description: "Debug App Service outbound connectivity from inside the sandbox: tcpping, nameresolver, curl, the network troubleshooter, and reading NSG/UDR/firewall evidence."
sources: ["https://learn.microsoft.com/troubleshoot/azure/app-service/troubleshoot-vnet-integration-apps", "https://learn.microsoft.com/azure/app-service/overview-vnet-integration", "https://learn.microsoft.com/azure/app-service/resources-kudu"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service network troubleshooting

**Goal:** prove where an outbound call from an app fails: DNS, routing, NSG, firewall or the destination.

## Tools inside the app
Windows (Kudu > Debug console, `https://<app>.scm.azurewebsites.net/DebugConsole`):
```
nameresolver sqlsrv.database.windows.net
tcpping sqlsrv.database.windows.net:1433
tcpping 10.20.1.4:443
curl -v https://api.partner.com/health
```
In native Windows apps `ping`, `nslookup` and `tracert` don't work in the console; use `nameresolver` for DNS and `tcpping` for host:port. `nameresolver.exe` does not work in custom Windows containers or in Linux apps.
Linux (SSH from portal or `az webapp ssh`; tools depend on the image):
```bash
nslookup sqlsrv.database.windows.net
nc -zv sqlsrv.database.windows.net 1433      # if nc is in the image; else curl telnet://host:port
curl -v https://api.partner.com/health
```

## Interpret
| Result | Likely cause |
|---|---|
| Name resolves to public IP but service has private endpoint | DNS (zone link / custom DNS) |
| tcpping times out to private IP | NSG on integration subnet or destination, UDR to firewall without rule, route not via integration |
| tcpping OK, app still fails | TLS/auth/firewall on the service (IP not allowed, expects private path) |
| Works on one instance only | Instance-specific (scale-out), cached DNS - restart |

## Platform helpers
- *Diagnose and solve problems* > **Network troubleshooter**: checks VNet integration health, subnet size,
  DNS and connectivity to a given endpoint.
- Integration subnet must have free IPs for the instances; check the VNet integration subnet requirements.
- Outbound path: a destination outside RFC1918 only goes through the VNet when Route All is enabled; check UDRs and the firewall logs for the integration subnet range.

## Gotchas
- Hybrid Connections and VNet integration are different paths; tcpping tests the actual path the app uses.

## Verify
- [ ] Each dependency resolves and tcpings from the app; firewall logs show allows; app health check green.

## Checked

2026-10-28. Confirmed on the VNet integration troubleshooting page: ping, nslookup and tracert do not work in the native Windows console, nameresolver and tcpping syntax, nameresolver unsupported in Linux apps and custom Windows containers, Route All matters for non-RFC1918 destinations. Removed: the ICMP-blocked explanation, the /26 subnet size, firewall log table names and the NAT gateway source-IP claim.

Method: documentation only; no commands were run.
