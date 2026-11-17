---
id: computing-software.cloud-infrastructure-engineering.google-cloud.shared-vpc-host-and-service-projects
name: shared-vpc-host-and-service-projects
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc, shared-vpc, shared-vpc-host-project, shared-vpc-service-project, xpn, network-user, subnet-level-iam]
level: practitioner
status: docs-checked
description: "Set up Shared VPC: enable a host project, attach service projects, grant networkUser at subnet level, special grants for GKE, and liens against deleting the host."
sources: ["https://cloud.google.com/vpc/docs/provisioning-shared-vpc", "https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-shared-vpc", "https://cloud.google.com/vpc/docs/shared-vpc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared VPC host and service projects

## Enable and attach
Requires `roles/compute.xpnAdmin` (Shared VPC Admin) at the organization or a folder (with `roles/resourcemanager.projectIamAdmin` for granting roles).
```bash
gcloud compute shared-vpc enable net-host-prod
gcloud compute shared-vpc associated-projects add app-a-prod --host-project=net-host-prod
gcloud compute shared-vpc list-associated-resources net-host-prod
gcloud compute shared-vpc get-host-project app-a-prod
```

## Grant subnet access (least privilege)
```bash
gcloud compute networks subnets add-iam-policy-binding app-a-ew2 --region=europe-west2 --project=net-host-prod \
  --member=group:app-a-deployers@example.com --role=roles/compute.networkUser
```
Also grant `compute.networkUser` on the subnet to the service project's service accounts that create resources there:
- The Google APIs service account `<PROJECT_NUMBER>@cloudservices.gserviceaccount.com` (it creates resources such as managed instance group VMs).
- GKE: the GKE service agent `service-<PROJECT_NUMBER>@container-engine-robot.iam.gserviceaccount.com` gets `compute.networkUser` on the subnet and `roles/container.hostServiceAgentUser` on the host project. For GKE-created firewall rules, grant it a role (or a custom role with `compute.networks.updatePolicy` and `compute.firewalls.*`) on the host project, or pre-create the rules.

## Protect
When a project becomes a Shared VPC host Google places a lien on it, which stops accidental deletion; it is removed automatically when the project stops being a host. By default a project owner can remove the lien, so enforce `constraints/compute.restrictXpnProjectLienRemoval` at the organization: only principals with `roles/owner` or `roles/resourcemanager.lienModifier` at the organization (or a custom role with `resourcemanager.projects.get` and `resourcemanager.projects.updateLiens`) can then remove it.
By default service-project principals can use any host subnet they hold IAM on; limit this with `constraints/compute.restrictSharedVpcSubnetworks`, and limit which host projects non-host projects can attach to with `constraints/compute.restrictSharedVpcHostProjects`.

## Gotchas
- Firewall rules and the network resources live in the host project; Security Admins (`compute.securityAdmin`) manage firewall rules there.
- Host projects are subject to the standard per-project VPC quotas.
- A project cannot be both a host project and a service project.

## Verify
- [ ] Service project deploys a VM/GKE node in its subnet; attempting another team's subnet fails with permission denied.

## Checked
2026-10-31. Confirmed against the Shared VPC overview, "Set up Shared VPC" and the GKE Shared VPC pages: xpnAdmin and projectIamAdmin roles, `compute.networkUser` for the cloudservices and container-engine-robot accounts, `roles/container.hostServiceAgentUser` on the host, the lien and its removal roles, the three constraints, host/service exclusivity. gcloud commands checked against the reference. Removed: the Cloud Run/serverless robot grant, the lien-name detail and the vague firewall delegation remark (not on the pages read).
Method: documentation only; no commands were run.
