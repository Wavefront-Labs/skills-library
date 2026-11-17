---
id: computing-software.digital-forensics-incident-response.log-analysis.deploying-velociraptor-server-and-clients
name: deploying-velociraptor-server-and-clients
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [velociraptor-deployment, velociraptor, enterprise-ir, msi-deployment, dfir]
level: practitioner
status: draft
description: "Deploy Velociraptor for an incident: server config generation, TLS and authentication, client MSI rollout via GPO/Intune/EDR, scaling and securing the server."
sources: ["https://docs.velociraptor.app/docs/deployment/", "https://docs.velociraptor.app/docs/deployment/clients/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deploying Velociraptor server and clients

**Goal:** stand up a Velociraptor server quickly during an incident and get agents onto the
estate so you can collect and hunt at scale.

## Server
```bash
velociraptor config generate -i            # interactive: deployment type, public DNS name, TLS (Let's Encrypt or self-signed), SSO or basic auth
velociraptor --config server.config.yaml debian server --binary velociraptor   # builds a .deb with service
sudo dpkg -i velociraptor_server*.deb
velociraptor --config server.config.yaml user add analyst --role administrator
```
- Host it **outside** the compromised environment (cloud VM) so a compromised domain cannot
  reach the server's admin plane; expose only the frontend port (8000) to clients and the GUI
  (8889) to analysts via VPN/IP allow-list or SSO (OIDC with Google/Azure/Okta).
- Sizing: a single server handles thousands of clients; datastore on fast disk, plan storage
  for collections (triage zips are hundreds of MB each).

## Clients
```bash
velociraptor --config server.config.yaml config client > client.config.yaml
# Windows MSI with embedded config (GUI: Server Artifacts -> Server.Utils.CreateMSI) or repack:
velociraptor config repack --msi velociraptor-windows-amd64.msi client.config.yaml velo-client.msi
```
Deploy via GPO software installation, Intune, SCCM, or the EDR's script/run capability;
Linux `.deb`/`.rpm` via config management; macOS pkg. Service name `Velociraptor`.

## Security
- Client config contains only the server CA and URL; safe to distribute.
- Restrict GUI roles (investigator vs administrator); audit logs of analyst actions.
- Remove agents after the engagement (uninstall MSI) unless kept as standing capability.

## Gotchas
- EDR may block the client (it can run arbitrary VQL); allow-list the signed binary/hash.
- Proxy-only egress: set `Client.proxy` in client config.

## Verify
GUI shows expected client count online; run `Generic.Client.Info` as a test collection across
all clients and confirm results return.
