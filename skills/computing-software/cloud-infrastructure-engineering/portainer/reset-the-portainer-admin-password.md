---
id: computing-software.cloud-infrastructure-engineering.portainer.reset-the-portainer-admin-password
name: reset-the-portainer-admin-password
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [admin-password, helper-reset-password, recovery, swarm, kubernetes]
level: practitioner
status: docs-checked
description: "Recover admin access by running the Portainer reset-password helper against the data volume, for Docker, Swarm or Kubernetes."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/reset-admin.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/troubleshooting/access-and-authentication/how-do-i-reset-my-portainer-password.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three methods exist, depending on how Portainer is deployed. All use the `portainer/helper-reset-password` image against the Portainer data.

Container (Docker Standalone): stop the Portainer container, then run the helper with the data volume mounted:

```
docker stop <portainer-container-id>
docker pull portainer/helper-reset-password
docker run --rm -v portainer_data:/data portainer/helper-reset-password
```

Adjust the mount if your volume has another name or is a bind mount. The helper prints a new random password for `admin`. If it cannot find an admin user it creates one, naming it `admin-` plus a random string if `admin` is taken. Then start Portainer again and log in.

Stack or service (Swarm): scale the service to zero with `docker service scale portainer_portainer=0`, run the helper with the stack's data volume (for example `portainer_portainer_data:/data`), then scale back to 1.

Kubernetes: scale the deployment to zero (`kubectl scale deploy portainer --replicas=0 -n portainer`), run a pod from the helper image with the Portainer data volume claim mounted at `/data`, read the new password from the pod logs, then scale back to 1 and delete the pod.

The helper also accepts `--password` (plaintext, bcrypt-hashed before storage), `--password-hash` (precomputed bcrypt hash; mutually exclusive with `--password`) and `--data-path` (default `/data`); without a password flag it generates a random one.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed the unconfirmed LDAP/OAuth line; added the Kubernetes steps and helper arguments.

Method: documentation only; no commands were run.
