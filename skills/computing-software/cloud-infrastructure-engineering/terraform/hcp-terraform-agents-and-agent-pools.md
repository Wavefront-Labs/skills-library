---
id: computing-software.cloud-infrastructure-engineering.terraform.hcp-terraform-agents-and-agent-pools
name: hcp-terraform-agents-and-agent-pools
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, tfc-agent, hcp-agents, hcp-terraform, agent-pools, private-networking, terraform-enterprise, kubernetes-operator]
level: advanced
status: docs-checked
description: "Run HCP Terraform runs on self-hosted tfc-agent workers: agent pools, tokens, workspace execution mode, custom images, hooks, scaling and network requirements."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/agents", "https://developer.hashicorp.com/terraform/cloud-docs/agents/agents", "https://developer.hashicorp.com/terraform/cloud-docs/agents/hooks", "https://developer.hashicorp.com/terraform/cloud-docs/integrations/kubernetes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HCP Terraform agents

Agents let HCP Terraform (or TFE) run plans and applies on your machines, so runs can
reach private APIs (on-prem vSphere, private EKS endpoints, internal Vault) and use
instance identity instead of static cloud keys. The agent needs outbound connections to
HCP Terraform (see Networking below); HashiCorp's requirements page lists no inbound ports.

## 1. Pool and token
Organisation settings, Agents, create pool, generate a token (shown once). As code:
```hcl
resource "tfe_agent_pool" "dc1" {
  organization        = "acme"
  name                = "dc1"
  organization_scoped = false          # restrict to allowed workspaces/projects
}
resource "tfe_agent_pool_allowed_workspaces" "dc1" {
  agent_pool_id         = tfe_agent_pool.dc1.id
  allowed_workspace_ids = [tfe_workspace.vsphere.id]
}
resource "tfe_agent_token" "dc1" {
  agent_pool_id = tfe_agent_pool.dc1.id
  description   = "dc1 runners"
}
resource "tfe_workspace_settings" "vsphere" {
  workspace_id   = tfe_workspace.vsphere.id
  execution_mode = "agent"
  agent_pool_id  = tfe_agent_pool.dc1.id
}
```

## 2. Run an agent
```bash
export TFC_AGENT_TOKEN=<token>
export TFC_AGENT_NAME=dc1-agent-1      # for your reference only
docker run -e TFC_AGENT_TOKEN -e TFC_AGENT_NAME hashicorp/tfc-agent:latest
```
Useful variables: `TFC_ADDRESS` (HCP Terraform API address; default `https://app.terraform.io`),
`TFC_AGENT_SINGLE=true` (handle at most one job then exit, for ephemeral workers),
`TFC_AGENT_AUTO_UPDATE` (`minor`, `patch` or `disabled`), `TFC_AGENT_LOG_LEVEL` (default `info`).
Outbound access (agent requirements page): `app.terraform.io` tcp/443, `registry.terraform.io`
tcp/443, `releases.hashicorp.com` tcp/443 (agent updates and Terraform binaries),
`archivist.terraform.io` tcp/443, and `agents.terraform.io` tcp/7146 (request forwarding),
plus any provider APIs your code calls. Agents run on x86_64 or ARM64 Linux (or the
official Docker image); keep at least 4GB free disk and 2GB memory.

## 3. Capacity
Each agent process runs a single Terraform run at a time; several agent processes can
run on one instance, license limit permitting, so size the pool to peak concurrency. On
Kubernetes, the HCP Terraform Operator's `AgentPool` resource manages the pool and agent
tokens and supports agent autoscaling through `.spec.autoscaling`. Agents in the Idle,
Busy or Unknown state count towards the organization's purchased agent capacity.

## 4. Custom images and hooks
The official image runs the agent as the non-root `tfc-agent` user; build your own image
when a workflow needs extra software or hooks. HashiCorp's hooks page builds one from
`FROM hashicorp/tfc-agent:latest` by creating the `.tfc-agent` directory in the `tfc-agent`
user's home and adding a `hooks` directory there with `ADD --chown=tfc-agent:tfc-agent`.
Hooks are executable files in `~/.tfc-agent/hooks/` (the agent data directory) named
`terraform-pre-plan`, `terraform-post-plan`, `terraform-pre-apply`, `terraform-post-apply`;
only one of each type per agent. Use them to fetch short-lived credentials or emit audit
events. Hook stdout and stderr appear in the run output, so never echo secrets. A non-zero
exit fails the run; the default timeout is 60 seconds (max 10 minutes), set with
`TFC_AGENT_HOOK_TIMEOUT` or `TFC_AGENT_HOOK_<NAME>_TIMEOUT`. A hook can write `KEY=value`
lines to the file at `$TFC_AGENT_ENV` to set variables for the current operation.

## 5. Credentials
The point of agents is usually ambient identity: the runs execute on your host, so the
provider can use that host's identity instead of static keys. Leave provider credential
variables unset in the workspace so the provider falls back to it. Scope pools per
trust boundary; every workspace allowed on a pool runs with the same host identity.
Agents do not guarantee a clean environment per run; HashiCorp suggests stateless,
idempotent code and optionally single-execution mode.

## Gotchas
- An organisation-scoped pool lets any workspace pick it and inherit its cloud identity.
- `organization_scoped` defaults to `true`; set it to `false` and use
  `tfe_agent_pool_allowed_workspaces` to limit which workspaces can use a pool.
- Revoking an agent token makes agents using it exit; create and roll out a new token
  first, and let active runs finish.

## Verify
- [ ] Agent shows as Idle in the pool after start.
- [ ] A run in the workspace reaches a private-only endpoint successfully.
- [ ] Workspaces outside the allowed list cannot select the pool.

## Checked
- 2026-10-28. Confirmed against the HCP Terraform agent pages (agents, agent pools, requirements, hooks), the Kubernetes Operator overview and the `tfe` provider docs for `tfe_agent_pool` (`organization_scoped` defaults to true), `tfe_agent_pool_allowed_workspaces`, `tfe_agent_token` and `tfe_workspace_settings` (`execution_mode = "agent"` with `agent_pool_id`): token shown once, Docker run command and variables, single-execution mode, hostnames and ports, hook names, directory, timeouts and `$TFC_AGENT_ENV`, one run per agent process, Idle/Busy status and capacity counting.
- Removed: `--restart unless-stopped`, the CA-certificate Dockerfile, named cloud identity types, the provider-cache and queue-forever claims (not in the fetched docs).
Method: documentation only; no commands were run.
