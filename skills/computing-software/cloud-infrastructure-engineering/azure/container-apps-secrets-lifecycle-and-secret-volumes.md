---
id: computing-software.cloud-infrastructure-engineering.azure.container-apps-secrets-lifecycle-and-secret-volumes
name: container-apps-secrets-lifecycle-and-secret-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, container-apps, aca-secrets, container-app-secrets, secretref, secret-volumes, revisions]
level: practitioner
status: docs-checked
description: "Manage Azure Container Apps secrets: app-scoped secrets, secretref env vars, secrets mounted as files, rotation and why revisions need a restart to see new values."
sources: ["https://learn.microsoft.com/en-us/azure/container-apps/manage-secrets", "https://learn.microsoft.com/en-us/azure/container-apps/revisions", "https://learn.microsoft.com/en-us/cli/azure/containerapp/secret", "https://learn.microsoft.com/en-us/cli/azure/containerapp/revision"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container Apps secrets

**Goal:** no credentials in images or plain env vars, and rotations that actually reach running replicas.

## Model
- Secrets are defined at the **container app** level (shared by all revisions), referenced by containers.
- Values can be literal or Key Vault references (see the Key Vault references skill for that variant).

## Define and use
```bash
az containerapp secret set -g rg -n ca-orders --secrets "db-conn=Server=tcp:...;" "api-key=<value>"
az containerapp update -g rg -n ca-orders --set-env-vars "DB_CONN=secretref:db-conn" "API_KEY=secretref:api-key"
az containerapp secret list -g rg -n ca-orders -o table          # names only
az containerapp secret show -g rg -n ca-orders --secret-name api-key   # value (needs rights)
```

## Mount as files
```yaml
template:
  containers:
  - name: orders
    image: crcorp.azurecr.io/orders:1.8.0
    volumeMounts:
    - volumeName: secrets
      mountPath: /mnt/secrets
  volumes:
  - name: secrets
    storageType: Secret          # every secret appears as /mnt/secrets/<secret-name>
```
`az containerapp update -g rg -n ca-orders --yaml app.yaml`. Use `secrets:` under the volume to pick specific
secrets and file paths. Files suit certificates and apps that reload on file change.

## Rotation
- Adding, removing or changing a secret does **not** create a new revision, and an updated or deleted secret does not automatically affect existing revisions.
- After `secret set`, deploy a new revision or restart an existing revision:
```bash
az containerapp revision restart -g rg -n ca-orders --revision <revision-name>
```
- Before deleting a secret, deploy a new revision that no longer references it, then deactivate all revisions that reference it.

## Gotchas
- Registry passwords are also secrets (`--registry-password` creates one); switch to managed identity for ACR pulls.
- The `listSecrets` operations (container apps, jobs, Dapr components) return secret values in plain text, and several built-in roles with wildcard permissions grant them - check role definitions before assigning.
- Dapr components can reference secrets or a secret store; keep one source of truth.

## Verify
- [ ] `az containerapp show --query properties.template.containers[0].env` shows `secretRef` entries only; after rotation + restart the app uses the new value.

## Checked
Checked 2026-10-24 against azure-docs container-apps manage-secrets and the azure-docs-cli containerapp secret and revision references (secret set, list, show --secret-name; revision restart exist). Confirmed: secrets are app-level and shared by revisions; env var secretref syntax; secrets mounted as volume files; secret changes do not create revisions or affect existing revisions (deploy a new revision or restart); delete only after new revision stops referencing; listSecrets operations return plain-text values. Removed unconfirmed: secret name character rules.

Method: documentation only; no commands were run.
