---
id: computing-software.cloud-infrastructure-engineering.harbor.replication-endpoints
name: replication-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [replication-endpoint, registry-endpoint, access-secret, verify-remote-cert, harbor]
level: practitioner
status: docs-checked
description: "Create registry endpoints for replication or proxy cache, with credential formats for ECR, GCR and Quay and the rule that blocks deletion."
sources:
  - https://goharbor.io/docs/main/administration/configuring-replication/create-replication-endpoints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replication needs an endpoint for each remote registry. Go to **Registries**, **+ New Endpoint**, choose a **Provider**, then enter name, description, the full URL (for Harbor, `https://harbor_instance_address:443`) and the Access ID and Access Secret. The remote registry must already be running. Untick **Verify Remote Cert** for self-signed certificates, click **Test Connection**, then **OK**.

Non-Harbor providers: Alibaba Cloud Container Registry, AWS ECR, Azure Container Registry, Docker Hub, Docker registry, GitHub Container Registry, Google Container Registry and Artifact Registry, Huawei SWR, JFrog Artifactory, Tencent Container Registry and VolcEngine Container Registry. Proxy cache supports only a subset of these.

Credential rules:
- AWS ECR: use access keys with sufficient permissions such as storage, not username and password.
- Google GCR: use the entire service-account JSON key; the namespace starts with the project ID.
- Quay: leave both empty for no authorization. Otherwise Access ID defaults to `json_file` and the secret is JSON with `account_name`, `docker_cli_password` and optional `oauth2_token` (needed only to auto-create organizations). Avoid robot accounts as `account_name`. Quay.io cloud cannot auto-create organizations. Harbor does not support manifest schema1 in Quay.

Used in a proxy cache project, the account lets that project pull everything the account can pull. Registries are managed under Administration, Registries, and only registries not referenced by any rule can be deleted.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Creating Replication Endpoints.
Method: documentation only; no commands were run.
