---
id: computing-software.devops-ci-cd.gitlab-ci.secrets-keyword-vault-azure-gcp
name: secrets-keyword-vault-azure-gcp
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, secrets-keyword, vault-secrets-keyword, azure-key-vault-secrets, gcp-secret-manager-secrets, file-secrets]
level: advanced
status: docs-checked
description: "Fetch external secrets at job start with the secrets keyword from HashiCorp Vault, Azure Key Vault or GCP Secret Manager using ID tokens; file vs variable delivery."
sources: ["https://docs.gitlab.com/ci/yaml/#secrets", "https://docs.gitlab.com/ci/secrets/hashicorp_vault/", "https://docs.gitlab.com/ci/secrets/azure_key_vault/", "https://docs.gitlab.com/ci/secrets/gcp_secret_manager/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The `secrets` keyword (Premium)

The runner fetches the secret before the script starts; the value never lives in GitLab.

## 1. HashiCorp Vault
CI/CD variables: `VAULT_SERVER_URL`, `VAULT_AUTH_ROLE`, `VAULT_AUTH_PATH` (default `jwt`),
optional `VAULT_NAMESPACE`.
```yaml
deploy:
  id_tokens:
    VAULT_ID_TOKEN: { aud: https://vault.example.com }
  secrets:
    DB_PASSWORD:
      vault: production/db/password@ops      # <path>/<field>@<engine mount>
      token: $VAULT_ID_TOKEN
      file: false                             # value in the variable, not a file path
    TLS_KEY:
      vault: { engine: { name: kv-v2, path: ops }, path: production/tls, field: key }
      token: $VAULT_ID_TOKEN
  script:
    - ./deploy.sh                            # $DB_PASSWORD = value, $TLS_KEY = path to a temp file
```
Default is `file: true`: the variable holds a **path** to a file containing the secret — ideal for
keys/certs, a surprise for passwords (a client that expects the password gets a file path). Set `file: false` to put the value in the variable.

## 2. Azure Key Vault
Variables: `AZURE_KEY_VAULT_SERVER_URL`, `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`.
```yaml
  id_tokens: { AZURE_JWT: { aud: https://gitlab.com } }
  secrets:
    API_KEY:
      azure_key_vault: { name: api-key, version: "<secret version GUID>" }
      token: $AZURE_JWT
```
`aud` must match the audience of the federated identity credential on the Azure app. The value arrives as a file path by default, like file-type variables. With RBAC on the vault, grant the app the *Key Vault Secrets User* role.

## 3. GCP Secret Manager
Variables: `GCP_PROJECT_NUMBER`, `GCP_WORKLOAD_IDENTITY_FEDERATION_POOL_ID`, `GCP_WORKLOAD_IDENTITY_FEDERATION_PROVIDER_ID`.
```yaml
  id_tokens:
    GCP_ID_TOKEN: { aud: "https://iam.googleapis.com/projects/${GCP_PROJECT_NUMBER}/locations/global/workloadIdentityPools/${GCP_WORKLOAD_IDENTITY_FEDERATION_POOL_ID}/providers/${GCP_WORKLOAD_IDENTITY_FEDERATION_PROVIDER_ID}" }
  secrets:
    SA_JSON: { gcp_secret_manager: { name: deploy-sa, version: latest }, token: $GCP_ID_TOKEN }
```

## 4. Gotchas
- The `secrets:` integrations are Premium and Ultimate only.
- Always restrict the Vault role to a project or namespace with bound claims such as `project_id` or `namespace_id`; the docs' example also binds `ref_protected`, `ref_type` and `ref` so only protected release tags can read production paths.
- GCP: the mapped `google.subject` attribute is limited to 127 bytes, so long `sub` values (deep subgroups, long branch names) fail the token exchange; `version` is optional and defaults to `latest`. For a secret in another GCP project use the name `projects/<project-number>/secrets/<secret-name>` (GitLab 17.0+).
- If a job fails with "The secrets provider can not be found", one of the required provider variables above is undefined.

## Verify
- [ ] The production job succeeds and a feature-branch run is denied by Vault.

## Checked
2026-10-31. Confirmed against the GitLab docs pages for HashiCorp Vault, Azure Key Vault and GCP Secret Manager secrets: tier, variable names, `VAULT_AUTH_PATH` default `jwt`, file-by-default behaviour and `file: false`, `vault: path/field@mount` form, kv-v2 default engine, Azure `aud` rule, GCP `latest` default and 127-byte limit.
Removed: the manual-login command, the multi-line masking claim, the `environment` bound claim, the empty Azure `version`, the log-line check.
Method: documentation only; no commands were run.
