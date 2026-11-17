---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-marketplace-deployments
name: cloud-marketplace-deployments
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-marketplace, marketplace, marketplace-vm, marketplace-kubernetes-app, marketplace-saas, private-offers, marketplace-procurement, commitment-drawdown, marketplace-iam, deployment-manager, marketplace-billing, third-party-licensing, vendor-images]
level: practitioner
status: draft
description: "Deploy and govern Cloud Marketplace products: VM, Kubernetes-app and SaaS listings, IAM to buy and deploy, private offers and commitment drawdown, and keeping vendor VMs patched."
sources: ["https://cloud.google.com/marketplace/docs/overview", "https://cloud.google.com/marketplace/docs/understanding-billing", "https://cloud.google.com/marketplace/docs/private-offers", "https://cloud.google.com/marketplace/docs/access-control", "https://cloud.google.com/marketplace/docs/deploy-kubernetes-app"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud Marketplace deployments

**Goal:** buy third-party software through the GCP bill when it makes commercial sense, deploy
it without handing Editor to the vendor, and know what you are responsible for afterwards.

## 1. Listing types and what they create
| Type | What you get | Ops responsibility |
|---|---|---|
| **VM solution** | a Compute Engine VM (or MIG) from a vendor image, deployed via Infrastructure Manager/Deployment Manager with a parameters form | you patch the OS unless the vendor's image includes auto-update; vendor licence billed per vCPU-hour alongside the VM |
| **Kubernetes app** | Helm/`Application` CRD into an existing GKE cluster (`gke-marketplace` namespace) | you upgrade; the app may need a metering agent (`ubbagent`) for usage billing |
| **SaaS** | subscription + redirect to the vendor; optionally a Google-managed integration (Datadog, Elastic, MongoDB Atlas …) | none infra-wise; IAM/SSO on the vendor side |
| **Datasets / models** | BigQuery dataset access or Vertex Model Garden entries | query/inference cost |

Deployment creates resources in *your* project under *your* service account — read the generated config
(`gcloud infra-manager deployments describe`) before clicking; many vendor templates default to external IPs and `0.0.0.0/0` firewall rules.

## 2. IAM to buy and deploy
- `roles/consumerprocurement.orderAdmin` on the **billing account** to accept paid offers; `roles/consumerprocurement.orderViewer` to see them.
- Deployer needs the roles the template uses (`compute.admin`, `iam.serviceAccountUser` …) — Marketplace runs as the deploying user, not a magic SA.
- Org policy `cloudmarketplace.restrictMarketplaceProducts`-style controls: use a **Marketplace restriction policy** in the Private Marketplace / procurement settings to allow-list vendors, and `compute.trustedImageProjects` to block arbitrary vendor images outside Marketplace.
- Deployment Manager is deprecated for new templates; Marketplace VM solutions now deploy through **Infrastructure Manager** (Terraform) — the deployer needs `roles/config.admin` and a SA with the resource roles.

## 3. Commercial: when it is worth it
- Marketplace spend **draws down your Google Cloud commitment** (most listings count 100 %) — a reason finance prefers it over a direct vendor contract.
- **Private offers**: vendor sends a custom price/term to your billing account; accept in console → Marketplace → Your orders. Negotiate there, not in the public listing.
- Usage-based Kubernetes apps meter through `ubbagent`; block egress to `servicecontrol.googleapis.com` and the app stops reporting (and sometimes stops working).
- Cancel a subscription in *Your orders*; deleting the resources does not cancel the plan.

## 4. Operating a vendor VM
- Treat as an appliance: vendor image, vendor update channel, your network/IAM. Document the vendor's patch SLA; you still own CVEs on the OS layer if the image is a stock OS + agent.
- Put it behind IAP/ILB, give it its own SA, label it `marketplace=<vendor>` so Asset Inventory can list them; include them in VM Manager inventory (see `vm-manager-and-os-patching`) even if you cannot patch.
- Rebuild from a newer listing version rather than in-place upgrade when the vendor publishes a new image; take a snapshot first.

## Gotchas
- "Free" listings still bill the underlying VM/GKE and may require accepting vendor EULAs that your legal team has not seen.
- Marketplace Kubernetes apps need `kubectl` auth to the cluster from the console; private clusters without a public endpoint need Connect gateway or deploy via `mpdev`/Helm manually.
- The listing's "Google-tested" badge covers the deployment template, not the software's security.
- Billing export shows Marketplace SKUs under the vendor's service name, not `Compute Engine` — FinOps filters miss them.

## Verify
- [ ] Deployed VM has no external IP and only the ports the vendor documents open to the ILB/IAP range.
- [ ] Billing export shows the vendor SKU and the commitment report shows the drawdown.
- [ ] Marketplace order appears under the billing account with the private-offer price if negotiated.
- [ ] A test cancellation in *Your orders* stops the subscription line by the next invoice.
