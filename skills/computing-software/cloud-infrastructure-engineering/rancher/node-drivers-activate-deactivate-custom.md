---
id: computing-software.cloud-infrastructure-engineering.rancher.node-drivers-activate-deactivate-custom
name: node-drivers-activate-deactivate-custom
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [node-drivers, drivers, docker-machine, deactivate, cluster-management, manage-node-drivers]
level: practitioner
status: docs-checked
description: "Manage Rancher node drivers: which are active by default, how to add a custom driver, and why deactivating one can leave existing clusters inaccessible."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/about-provisioning-drivers/manage-node-drivers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A node driver is the same thing as a Docker Machine driver. Rancher uses node drivers to provision hosts, then launches and manages Kubernetes on them. Many drivers are packaged, and only **Active** ones are shown when users create node templates. By default Rancher activates drivers for the most popular providers such as Amazon EC2, Azure, DigitalOcean, Linode and vSphere.

To create, edit or delete drivers you need the Administrator global permission, or custom global permissions including **Manage Node Drivers**.

Manage them under **Cluster Management > Drivers > Node Drivers**: choose the driver and use **Activate** or **Deactivate** from its menu.

The page has a danger box: **deactivating or deleting a driver is not just hiding it**. Any nodes deployed with that driver become inaccessible. In its example, deactivating the vSphere driver to hide it from the UI, while a vSphere cluster built with it exists, makes that cluster's initial node fail, the whole cluster inaccessible, and deletion attempts leave nodes stuck in `Removing`. Before deactivating, check the **Provider** column on the **Clusters** page for clusters using that platform.

To use a provider Rancher does not support out of the box, choose **Add Node Driver** on the same tab and complete the form. Node drivers are implemented with Rancher Machine, a fork of Docker Machine, which is no longer under active development; for writing your own driver the page points to the original Docker Machine documentation.

## Checked

2026-11-09. Read in full the Rancher Manager Node Drivers page (about-provisioning-drivers/manage-node-drivers). Corrected the custom-driver developer guidance.

Method: documentation only; no commands were run.
