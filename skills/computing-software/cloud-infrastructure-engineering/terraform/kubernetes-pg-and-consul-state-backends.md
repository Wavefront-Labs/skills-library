---
id: computing-software.cloud-infrastructure-engineering.terraform.kubernetes-pg-and-consul-state-backends
name: kubernetes-pg-and-consul-state-backends
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, kubernetes-backend, pg-backend, consul-backend, remote-state, state-locking, self-hosted-state]
level: practitioner
status: docs-checked
description: "Configure the kubernetes, pg and consul state backends for self-hosted state: locking model, credentials and workspace mapping for each."
sources: ["https://developer.hashicorp.com/terraform/language/backend/kubernetes", "https://developer.hashicorp.com/terraform/language/backend/pg", "https://developer.hashicorp.com/terraform/language/backend/consul", "https://opentofu.org/docs/language/settings/backends/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# kubernetes, pg and consul backends

**Use when** there is no cloud object store to hand (on-prem, air-gapped, or a platform team that already runs Kubernetes/Postgres/Consul) and state must still be shared and locked.

## kubernetes
```hcl
terraform {
  backend "kubernetes" {
    secret_suffix = "network"          # Secret name: tfstate-<workspace>-network
    namespace     = "terraform-state"
    config_path   = "~/.kube/config"   # or in_cluster_config = true inside a pod
  }
}
```
- State is stored in a Secret named `tfstate-{workspace}-{secret_suffix}`; locking uses a `Lease` resource. The backend may chunk a large state into several Secrets named `tfstate-{workspace}-{secret_suffix}-{index}`.
- The account running Terraform needs permission to read and write Secrets (and the lease) in the namespace. Anyone who can read the Secret reads every sensitive value.
- Authenticate with `config_path` / `config_paths` (kubeconfig) or `in_cluster_config` (service account inside a pod); the env vars `KUBE_CONFIG_PATH`, `KUBE_CONFIG_PATHS`, `KUBE_IN_CLUSTER_CONFIG` and `KUBE_NAMESPACE` can supply them. If several are set, `config_path` wins.
- Workspaces map to the `{workspace}` part of the Secret name.

## pg (PostgreSQL)
```hcl
terraform {
  backend "pg" {
    schema_name = "tf_network"   # default terraform_remote_state; one schema per state set
  }
}
```
```bash
export PG_CONN_STR="postgres://tf:${PGPASSWORD}@db.internal/terraform_backend?sslmode=verify-full"
terraform init
```
- Creates one table `states` in the managed schema, keyed by workspace name (`default` when workspaces are unused). It holds a serial `id` (used for advisory locks), the workspace name (unique index) and the state as text.
- `skip_schema_creation = true` means the schema must already exist; `skip_table_creation = true` means the table must already exist (both for roles that cannot create objects).
- Locking uses Postgres **advisory locks**, which release automatically when the session aborts or the connection fails. `terraform force-unlock` is not supported; inspect locks with the `pg_locks` view.

## consul
```hcl
terraform {
  backend "consul" {
    address = "consul.internal:8500"
    scheme  = "https"
    path    = "terraform/network"     # KV path
    lock    = true
  }
}
```
- `path` is required; the access token is required too and comes from `access_token` or `CONSUL_HTTP_TOKEN`. Prefer the environment variable.
- Locking (default on) needs Consul session permissions and at least KV write on `$path/.lock`.
- `gzip = true` compresses the state before storing it (default false).

## Common gotchas
- Put credentials in env vars, not in the committed block: values in `-backend-config` or the block end up in the `.terraform` directory and in plan files.
- Back up the store itself with that system's own tools (etcd, `pg_dump`, `consul snapshot save`).

## Verify
- [ ] `terraform init` configures the backend without error.
- [ ] Two concurrent `terraform plan` runs: the second waits or fails with a lock error.
- [ ] The backing object exists (`kubectl get secret tfstate-default-network`, the `states` table, `consul kv get terraform/network`).

## Checked
2026-10-28. Confirmed against the Terraform kubernetes, pg and consul backend pages: secret naming and chunking, lease locking, kubeconfig and in-cluster auth and env vars, `schema_name` default, `skip_schema_creation`, `skip_table_creation`, `states` table columns, advisory locks and no force-unlock, consul `path`, `access_token`/`CONSUL_HTTP_TOKEN`, `lock` default and permissions, `gzip` default, credentials-in-plan-files warning.
Corrected: "Secrets cap at 1 MiB ... `Request entity too large`" (the backend chunks large states into several Secrets); "split automatically only when gzip = true helps enough" (gzip just compresses); the consul ACL `key_prefix` wording (docs name session permissions and KV write on `$path/.lock`).
Removed: the gzip-compressed Secret claim, exact RBAC verbs, the `-env:<name>` workspace path suffix, the 512 KiB limit, the PgBouncer claim, and `init -reconfigure` / `-migrate-state` advice (none in the fetched pages).
Method: documentation only; no commands were run.
