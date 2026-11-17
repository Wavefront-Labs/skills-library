---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-mesh-ingress-awxmeshingress-resource
name: awx-operator-mesh-ingress-awxmeshingress-resource
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, mesh-ingress, awxmeshingress, receptor, hop-node, execution-node, ssl-passthrough]
level: sme
status: docs-checked
description: "Enable the AWXMeshIngress resource so external execution and hop nodes can peer into the control plane, on OpenShift, NGINX, Traefik or a user-managed Ingress."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/mesh-ingress.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator mesh ingress awxmeshingress resource

Mesh ingress peers external execution and hop nodes into the AWX control plane. Requirements: AWX Operator newer than 2.11.0 and AWX newer than 23.8.0. It uses the AWX instance's `control_plane_ee_image` and `image_pull_policy` (defaults `quay.io/ansible/awx-ee:latest` and `Always`); no dedicated parameters exist.

Create an `AWXMeshIngress` (apiVersion `awx.ansible.com/v1alpha1`) in the AWX namespace with `spec.deployment_name: <awx instance name>`:
- OpenShift with an operator-managed Route: just `deployment_name`.
- Kubernetes with NGINX: `ingress_type: Ingress`, `ingress_controller: nginx`, `ingress_class_name: nginx`, `external_hostname`. SSL passthrough must be enabled on the controller; the operator sets `nginx.ingress.kubernetes.io/ssl-passthrough: "true"`.
- Kubernetes with Traefik: `ingress_type: IngressRouteTCP`, `ingress_controller: traefik`, `ingress_api_version: traefik.io/v1alpha1` (`traefik.containo.us` is deprecated), `external_hostname`; the generated IngressRouteTCP uses the `websecure` entry point.
- User-managed Ingress: `ingress_type: none` (the default on Kubernetes) with `external_hostname` still required because it generates the certificate used by Receptor.

A user-managed Ingress must support WebSocket, SSL/TLS passthrough, be reachable on port 443, use the same hostname as `external_hostname` and route to port 27199 of the Service named like the AWXMeshIngress.

Validate: a new Instance with the same name is registered to AWX and visible on the Instance UI page with at least two listener addresses, one internal (used for peering by all control nodes) and one external (exposed so external execution nodes can peer into it), and it is present as an option when selecting a peer for a new instance.

## Checked

2026-11-04. Confirmed against the AWX Operator "Mesh Ingress" page: prerequisites, image/pull-policy note, all four deployment variants and their fields, the user-managed Ingress requirements (including port 27199), the Traefik API-group note and the validation steps. Nothing removed.
Method: documentation only; no commands were run.
