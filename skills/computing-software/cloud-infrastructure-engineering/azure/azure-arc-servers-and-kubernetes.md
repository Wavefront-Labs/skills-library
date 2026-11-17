---
id: computing-software.cloud-infrastructure-engineering.azure.azure-arc-servers-and-kubernetes
name: azure-arc-servers-and-kubernetes
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-arc, arc-enabled-servers, arc-enabled-kubernetes, connected-machine-agent, azcmagent, hybrid-cloud, multicloud, arc-extensions, azure-monitor-agent, update-manager, defender-for-servers, azure-policy-guest-configuration, machine-configuration, arc-gateway, private-link-scope, extended-security-updates, esu, cluster-connect, gitops-flux]
level: practitioner
status: docs-checked
description: "Onboard on-prem/other-cloud machines and clusters to Azure Arc at scale: extensions (AMA, Update Manager, Defender), machine configuration, Arc gateway/Private Link, GitOps on Arc K8s."
sources: ["https://learn.microsoft.com/azure/azure-arc/servers/prerequisites", "https://learn.microsoft.com/azure/azure-arc/servers/onboard-service-principal", "https://learn.microsoft.com/azure/azure-arc/servers/azcmagent-connect", "https://learn.microsoft.com/azure/azure-arc/servers/arc-gateway", "https://learn.microsoft.com/azure/azure-arc/servers/private-link-security", "https://learn.microsoft.com/azure/azure-arc/servers/manage-agent-proxy-settings", "https://learn.microsoft.com/azure/azure-arc/servers/deliver-extended-security-updates", "https://learn.microsoft.com/azure/azure-arc/kubernetes/quickstart-connect-cluster", "https://learn.microsoft.com/azure/azure-arc/kubernetes/cluster-connect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Arc — manage servers and clusters you don't host in Azure as if you did

**Goal:** one inventory, one policy engine, one patch schedule and one security agent
across Azure VMs, VMware, bare metal, AWS and GCP.

## 1. Arc-enabled servers: onboarding
Prereqs: outbound HTTPS to the Arc endpoints (or the **Arc gateway**, which reduces the endpoints needed through an enterprise proxy to seven),
the `Microsoft.HybridCompute`, `Microsoft.GuestConfiguration` and `Microsoft.HybridConnectivity` resource providers registered, and
an identity with the **Azure Connected Machine Onboarding** role (or Contributor) on the target resource group.
```bash
az ad sp create-for-rbac --name sp-arc-onboard --role "Azure Connected Machine Onboarding" --scopes /subscriptions/<sub>
# on each machine, after installing the Connected Machine agent (portal "Add multiple servers" generates the script):
azcmagent connect --subscription-id <sub> --resource-group rg-arc --location uksouth \
  --service-principal-id <appId> --service-principal-secret <secret> --tenant-id <tenant> [--gateway-id <arc-gateway-resource-id>]
```
Alternatives to a service principal: `--use-device-code` and `--use-azcli`. The portal can generate scripts for single and multiple servers, and the documentation covers deployment through Ansible, Configuration Manager, Group Policy and Windows Admin Center. `azcmagent show` reports agent status; `azcmagent check` tests connectivity.
Do not install Arc on VMs hosted in Azure, Azure Stack Hub or Azure Stack Edge: they already have equivalent capabilities.

## 2. What you get once connected
- A `Microsoft.HybridCompute/machines` resource: tags, RBAC, Resource Graph.
- VM extensions managed by the extension agent (install, upgrade, remove), for example the Azure Monitor Agent (a separate agent that collects monitoring data; it does not replace the Connected Machine agent).
- Update management, Defender and machine configuration (policy) integrations, and SSH access without a public IP or open ports (see the SSH article for the `az ssh arc` workflow).
- A system-assigned managed identity reachable by local apps at `IDENTITY_ENDPOINT` (`http://localhost:40342/metadata/identity/oauth2/token`), so on-premises apps can call Azure services without secrets.
- Windows Server 2012 and 2012 R2 Extended Security Updates through Arc: the ESU period ended on 13 October 2026, and licences enabled through Arc deactivated at midnight UTC on 14 October 2026; linked servers are not eligible for later security updates. Licence resources stay visible in Azure.

## 3. Network design
- Default: outbound HTTPS to the endpoint list in the network requirements article; proxies are configured with `azcmagent config set proxy.url "http://ProxyServerFQDN:port"` (`config get` and `config clear` exist).
- **Arc gateway**: lets enterprise proxy rules allow only seven endpoints, and lets you view and audit agent traffic.
- **Azure Arc Private Link Scope** for private connectivity: private endpoints for Arc and the linked Azure Monitor resources over ExpressRoute or site-to-site VPN. Associate a machine with a scope using `azcmagent connect --private-link-scope`.

## 4. Arc-enabled Kubernetes
```bash
az extension add -n connectedk8s
az connectedk8s connect --name cluster01 --resource-group rg-arc   # from a kubeconfig context; location defaults to the resource group's
az connectedk8s proxy -n cluster01 -g rg-arc                         # cluster connect: kubectl through Azure with no inbound firewall port
```
Arc-enabled Kubernetes works with any CNCF-certified Kubernetes cluster, on-premises or on other clouds. Cluster extensions (`az k8s-extension`) and GitOps (Flux) build on the connected cluster; see the cluster extensions and GitOps articles for commands.

## Gotchas
- Do not Arc-enable Azure VMs (see section 1).
- The onboarding service principal secret ends up in your deployment tool: use the Onboarding role only and a short secret lifetime.
- Servers that stop sending heartbeats (sent every five minutes) for longer than 15 minutes may be offline or have a network problem; check the troubleshooting articles.

## Verify
- [ ] `azcmagent show` reports the agent as connected, and the machine appears as a `microsoft.hybridcompute/machines` resource in Resource Graph.
- [ ] `az connectedk8s show` for the Arc-enabled cluster reports it connected.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-management-docs `articles/azure-arc` (servers/prerequisites, onboard-service-principal, azcmagent-connect, arc-gateway, private-link-security, manage-agent-proxy-settings, agent-overview, deliver-extended-security-updates; kubernetes/quickstart-connect-cluster, cluster-connect, system-requirements; main branch).
- Confirmed: required resource providers; Azure Connected Machine Onboarding or Contributor role; `azcmagent connect` authentication options and `--gateway-id`; Arc gateway needing seven endpoints; proxy configuration commands; private link scope with ExpressRoute or VPN; `IDENTITY_ENDPOINT` value; heartbeat timing; Windows Server 2012 ESU end dates (13 and 14 October 2026); `az connectedk8s connect` and `proxy`; CNCF-certified clusters.
- Removed as unconfirmed: the agent install script URL, `--tags` on connect, 45-day expiry, clock-skew limit, extension and policy names, SQL Server and Defender plan details, `az connectedmachine` commands, the Flux command lines, and the claim that Arc blocks Azure VMs by default.
Method: documentation only; no commands were run.
