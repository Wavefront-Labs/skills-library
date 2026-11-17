---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-fleet-registration-and-fleet-default-config
name: gke-fleet-registration-and-fleet-default-config
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, fleets, fleet-registration, fleet-memberships, fleet-default-config, config-sync, policy-controller, attached-clusters]
level: advanced
status: docs-checked
description: "Register GKE and attached clusters to a fleet, choose the fleet host project, and set fleet-level default configs so every new member gets Config Sync, Policy Controller and mesh."
sources: ["https://docs.cloud.google.com/kubernetes-engine/fleet-management/docs/fleet-creation", "https://docs.cloud.google.com/kubernetes-engine/fleet-management/docs/register/gke", "https://docs.cloud.google.com/kubernetes-engine/fleet-management/docs/manage-features", "https://docs.cloud.google.com/sdk/gcloud/reference/container/clusters/create-auto"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fleet registration and fleet default configuration

## 1. Pick the fleet host project
A project can have at most one fleet. Group clusters that should share features and defaults
(for example one fleet for prod, one for non-prod). An empty fleet can be created with
`gcloud container fleet create --display-name=<NAME> --project=<FLEET_P>`.

## 2. Register
```bash
# new Autopilot cluster, registered to its own project's fleet
gcloud container clusters create-auto c1 --region=<R> --enable-fleet
# new Autopilot cluster, registered to a fleet in another project
gcloud container clusters create-auto c1 --region=<R> --fleet-project=<FLEET_P>
# new Standard cluster with Workload Identity Federation for GKE
gcloud container clusters create c1 --region=<R> --enable-fleet --workload-pool=<P>.svc.id.goog
# existing cluster
gcloud container clusters update c1 --region=<R> --enable-fleet
gcloud container clusters update c1 --region=<R> --fleet-project=<FLEET_P>
```
Cross-project registration needs extra permissions; follow the prerequisites in the registration guide.
`--membership-type=LIGHTWEIGHT` registers a lightweight membership and
`gcloud container clusters update c1 --unset-membership-type` converts it to a regular one.
Clusters outside Google Cloud (EKS, AKS and others) are attached through the GKE Multi-Cloud API;
see the attached-clusters guides.

## 3. Fleet-level defaults
Features that support a fleet default configuration: Cloud Service Mesh, Config Sync, Policy Controller,
Security posture, GKE Identity Service (command line only) and Continuous validation for Binary
Authorization (preview, command line only). Any GKE cluster registered during cluster creation is
automatically configured with the fleet-level settings.
```bash
gcloud container fleet mesh enable --fleet-default-member-config mesh.yaml
```
Config Sync and Policy Controller defaults are set through their own feature guides (or Terraform,
using a `fleet_default_member_config` block in a `google_gke_hub_feature` resource).

## Gotchas
- Fleet default settings are not automatically applied to existing fleet member clusters; the docs describe syncing them to the defaults from the Google Cloud console.
- Only registrations made after the defaults are set pick them up.

## Verify
- [ ] The cluster appears as a fleet membership (Google Cloud console fleet view, or the fleet membership gcloud commands).
- [ ] A cluster created after the default is set shows the fleet-level configuration.

## Checked

2026-10-24, GKE fleet creation, GKE cluster registration and fleet feature-management pages on docs.cloud.google.com, plus the create-auto reference. Confirmed: one fleet per project, `gcloud container fleet create`, `--enable-fleet`, `--fleet-project`, `--membership-type=LIGHTWEIGHT`, `--unset-membership-type`, `--workload-pool`, the list of features supporting fleet defaults, the `fleet mesh enable --fleet-default-member-config` command, and that defaults are not applied to existing members. Removed unconfirmed claims: the explicit `memberships register` command, the GKE Hub service agent role, Config Sync and Policy Controller YAML and command forms, the `--origin=FLEET` sync command, namespace-sameness and fleet-move statements.

Method: documentation only; no commands were run.
