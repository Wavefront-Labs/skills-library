---
id: computing-software.cloud-infrastructure-engineering.azure.web-app-migration-to-app-service-and-aks
name: web-app-migration-to-app-service-and-aks
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, migration, web-app-migration, app-service-migration-assistant, azure-migrate, app-containerization, aks-migration, iis-migration, java-tomcat-migration, net-framework, readiness-assessment, replatform]
level: practitioner
status: draft
description: "Migrate IIS/.NET and Java Tomcat web apps to App Service or AKS: Azure Migrate web app discovery/assessment, App Service Migration Assistant, containerization and cutover."
sources: ["https://learn.microsoft.com/en-us/azure/migrate/tutorial-modernize-asp-net-appservice-code", "https://learn.microsoft.com/en-us/azure/migrate/tutorial-assess-webapps", "https://learn.microsoft.com/en-us/azure/migrate/tutorial-app-containerization-aspnet-kubernetes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web app migration to App Service and AKS

**Goal:** move on-prem web apps (ASP.NET on IIS, Java on Tomcat) to PaaS or containers with an
assessment that predicts blockers, a repeatable migration, and a clean DNS cutover.

## 1. Discover and assess at scale (Azure Migrate)
- The Azure Migrate appliance (with guest credentials) discovers IIS sites and Tomcat apps on
  VMware/Hyper-V/physical servers.
- **Web app assessment** → targets *Azure App Service* (code or containers) and *AKS*; output:
  readiness per app (Ready / Ready with conditions / Not ready + reason), recommended plan SKU,
  cost, and how many apps can share a plan (app density).
- Typical blockers: Windows auth requiring domain join, GAC/COM dependencies, local file writes,
  registry, MSMQ, non-HTTP ports, `<location>`/machine.config changes, apps larger than plan limits.

## 2. Migrate to App Service
- **Azure Migrate web app migration** (at scale from the assessment) or the **App Service
  Migration Assistant**/PowerShell scripts (`Get-SiteReadiness`, `Get-SitePackage`,
  `Invoke-SiteMigration`) per server: packages the site, creates plan/app, deploys content, carries app settings/connection strings from `web.config` where possible.
- After migration: move secrets to Key Vault references, set **VNet integration** for on-prem/DB reach,
  managed identity for Azure resources, health check path, deployment slots, then put CI/CD in place —
  the assistant output is a starting point, not the delivery pipeline.
- Java/Tomcat: App Service Linux with Tomcat runtime or JBoss EAP; externalise `context.xml` JNDI to app settings.

## 3. Containerize for AKS (or App Service containers)
- **Azure Migrate App Containerization** tool (ASP.NET on Windows containers, Java on Linux): discovers app,
  parameterises config, builds image into ACR, generates Kubernetes YAML; deploy to AKS.
- Windows containers need Windows node pools; prefer modernising to .NET 8 on Linux where code changes are acceptable.
- Externalise state: sessions to Redis, files to Azure Files/Blob, config to App Configuration/Key Vault (CSI driver).

## 4. Cutover
1. Lower DNS TTL days before. 2. Freeze content changes; final sync. 3. Validate on the default hostname
(`*.azurewebsites.net`) with a hosts-file override for the real name. 4. Add custom domain + managed certificate
(or import), flip CNAME/A. 5. Keep the old site running read-only for rollback.

## Gotchas
- Apps that need Windows authentication need a code or architecture change (for example Microsoft Entra authentication); the App Containerization tool does not support Windows authentication (gMSA).
- Outbound IP changes break partner allow-lists; NAT gateway on the integration subnet gives a stable IP.
- File-system writes go to ephemeral/shared storage on App Service; scale-out exposes the bug.
- The assistant migrates one site at a time — use Azure Migrate's at-scale path for estates.

## Verify
- [ ] Assessment lists each app with readiness and a remediation item for every condition.
- [ ] Migrated app passes smoke tests on its default hostname with secrets from Key Vault and VNet connectivity to dependencies.
- [ ] Custom domain served with valid TLS; old server traffic drops to zero before decommission.
