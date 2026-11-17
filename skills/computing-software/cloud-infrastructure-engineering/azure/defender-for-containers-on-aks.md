---
id: computing-software.cloud-infrastructure-engineering.azure.defender-for-containers-on-aks
name: defender-for-containers-on-aks
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, defender-containers, aks-defender, defender-for-containers, runtime-protection, vulnerability-assessment, defender-sensor]
level: practitioner
status: docs-checked
description: "Enable Defender for Containers for AKS and ACR: plan components (sensor, agentless discovery, vulnerability assessment), deploy at scale, triage alerts and recommendations."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/defender-for-containers-introduction", "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-containers-deployment-overview", "https://learn.microsoft.com/azure/aks/outbound-rules-control-egress"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defender for Containers on AKS

**Goal:** runtime threat detection on nodes and pods, vulnerability findings for images in ACR
and running in clusters, and Kubernetes posture checks — enabled everywhere by policy.

## Components
| Component | What it does | Deployment |
|---|---|---|
| Defender sensor | Sensor-based run-time threat protection on nodes and workloads: antimalware, DNS detection, binary drift detection and blocking | Deployed to clusters through Azure-managed integration (AKS), Arc extension (Arc-enabled Kubernetes) or Helm |
| Agentless discovery for Kubernetes | Zero-footprint, API-based discovery of clusters, configuration and deployments; feeds inventory and security explorer | No agent |
| Agentless vulnerability assessment | Scans container registry images (ACR, ECR, GAR, GCR), running containers and supported nodes with daily re-scans | No agent |
| Azure Policy for Kubernetes | Data plane hardening: recommendations and enforcement of best practices on API server requests | AKS add-on |
| Kubernetes audit log analysis | Control-plane based threat detection | On AKS, collected through the Azure-managed control plane integration, with no audit logging setup in the cluster |

## Enable
Turn on the **Containers** plan for the subscription in Microsoft Defender for Cloud (Environment settings), where the individual components above can be switched on or off. On a single AKS cluster the sensor can be deployed or removed with:
```bash
az aks update -g rg -n aks1 --enable-defender --defender-config defender.json
az aks update -g rg -n aks1 --disable-defender
```
`--defender-config` takes the path to a JSON file with the Defender profile configuration (for example the Log Analytics workspace to use); see the Defender for Cloud documentation for its schema.
Arc-enabled Kubernetes uses Azure Arc extensions; EKS and GKE use multicloud connectors (GKE clusters are also connected to Azure Arc).

## Triage
- Alerts appear in Defender for Cloud and can be investigated in Microsoft Defender XDR; they are mapped to MITRE ATT&CK for Containers. Examples of monitored events: exposed Kubernetes dashboards, exposed `LoadBalancer` services, creation of high-privileged roles, sensitive mounts. Alerts are only raised for activity after the plan is enabled.
- Recommendations come from control-plane hardening (type "Control plane"), vulnerability assessment of registry and running images, and Azure Policy for Kubernetes.
- Vulnerability findings are also attached to the image in the registry and feed the cloud security graph, attack paths and security explorer queries.

## Gotchas
- Sensor-based features (antimalware, drift, DNS detection) need the sensor; agentless features do not. Check coverage in the Defender for Cloud coverage workbook.
- Clusters behind restrictive egress need the Defender endpoints allowed; take the list from the AKS outbound rules article section on Microsoft Defender for Containers.
- Defender runs Microsoft-maintained images from `mcr.microsoft.com` (for example `low-level-collector`, `pod-collector`, `security-publisher`); allow MCR and do not patch these images yourself. AKS add-on updates arrive with the AKS release lifecycle, Helm deployments through updated chart versions within 30 days.
- Pricing depends on the enabled components and protected resources; see the Defender for Cloud pricing page.

## Verify
- [ ] Defender for Cloud Environment settings show the Containers plan on with the intended components.
- [ ] The coverage workbook shows the cluster as covered, and Defender for Cloud lists the cluster's recommendations.

## Checked
Date: 2026-10-24. Checked against the Defender for Containers introduction (updated 2026-08-10) and deployment overview (updated 2026-06-17) pages on Microsoft Learn, the AKS outbound rules article (MicrosoftDocs/azure-aks-docs) and the Azure CLI `acs` help for `--enable-defender`, `--disable-defender` and `--defender-config`.
- Confirmed: component list and what each does; AKS audit logs via the Azure-managed control plane; MCR image names and update paths; alerting scope; coverage workbook; CLI flags.
- Removed as unconfirmed (the detailed Defender configuration pages are not in a public repository and were not read): the `az security pricing` extension names, DaemonSet names and resource requests, specific Defender endpoints, the sample Resource Graph query, example alert and recommendation titles, and the 30-day rescan behaviour.
Method: documentation only; no commands were run.
