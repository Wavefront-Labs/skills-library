---
id: computing-software.devops-ci-cd.gitlab-ci.agent-for-kubernetes-ci-access-and-gitops
name: agent-for-kubernetes-ci-access-and-gitops
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, gitlab-agent, agentk, kas, kubernetes-agent, ci-access, kubecontext, agent-config-yaml, gitlab-gitops, flux-integration, agent-authorization, agent-token, agent-helm-install, impersonation, ci-job-impersonation, agent-rbac, certificate-based-cluster-deprecated]
level: practitioner
status: docs-checked
description: "Connect clusters to GitLab with the agent for Kubernetes: Helm install, config.yaml ci_access authorisation, kubectl contexts in $KUBECONFIG, impersonation RBAC, Flux GitOps."
sources: ["https://docs.gitlab.com/user/clusters/agent/", "https://docs.gitlab.com/user/clusters/agent/ci_cd_workflow/", "https://docs.gitlab.com/user/clusters/agent/install/", "https://docs.gitlab.com/user/clusters/agent/gitops/", "https://docs.gitlab.com/user/clusters/agent/user_access/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Agent for Kubernetes: CI access and GitOps

**Goal:** CI jobs run `kubectl`/`helm` against clusters through the GitLab agent with no
kubeconfig secrets in variables; optionally, Flux handles GitOps.

## 1. How it works
`agentk` runs in the cluster; the agent server (KAS) is `wss://kas.gitlab.com` (or
`grpcs://kas.gitlab.com`) on GitLab.com, and on self-managed an administrator must set it up (by
default `grpcs://<gitlab-host>`, or `wss://<gitlab-host>/-/kubernetes-agent/` without HTTPS or with
a relative URL root). Runners must be registered with GitLab but need not be in the cluster.
Each agent has its own kubecontext. Certificate-based cluster connections are deprecated.

## 2. Register and install
Register the agent in the UI, which gives you a token and a command of this form:
```bash
helm repo add gitlab https://charts.gitlab.io
helm repo update
helm upgrade --install my-agent gitlab/gitlab-agent \
  --set config.token=<AGENT_TOKEN> \
  --set config.kasAddress=<KAS_ADDRESS>
```
GitLab recommends bootstrapping with the GitLab CLI and Flux (`glab cluster agent bootstrap`;
its `--manifest-path` must match the `--path` you gave `flux bootstrap`). Store the token securely:
it can reach the agent configuration project's source and public projects on the instance. Chart
options: `serviceAccount.create=false` with `serviceAccount.name`, `rbac.useExistingRole`,
`rbac.create=false` (then create the ClusterRoleBinding yourself), `config.secretName` to bring
your own token secret.

## 3. Authorise projects and groups (config.yaml)
```yaml
ci_access:
  projects:
    - id: path/to/project
      environments: [staging, "review/*"]     # optional restriction
      protected_branches_only: true            # optional
  groups:
    - id: path/to/group/subgroup
  instance: {}                                  # self-managed 17.11+, needs admin setting
```
- Edit `config.yaml` in the agent's configuration project. Propagation takes one or two minutes.
- Authorised projects and groups must share the top-level group or user namespace of the
  configuration project unless instance-level authorisation is enabled (groups from different
  top-level groups are allowed from 18.1). Up to 500 projects and 500 groups.
- If a project has several matching configurations, the most specific one applies.
- `protected_branches_only` defaults to false (GA in 17.10).
- By default a job inherits the permissions of the agent's service account. Impersonation
  (Premium and Ultimate) restricts that with `access_as`: the agent (default), `ci_job: {}`, or a
  static `impersonate` identity (`username` required; `uid`, `groups`, `extra`).
- With `ci_job`, the Kubernetes username is `gitlab:ci_job:<job id>` and groups include
  `gitlab:ci_job`, `gitlab:group:<id>`, `gitlab:group_env_tier:<id>:<tier>`, `gitlab:project:<id>`,
  `gitlab:project_env:<id>:<env slug>` and `gitlab:project_env_tier:<id>:<tier>`. Bind RBAC to
  those groups, for example a ClusterRoleBinding of the `view` role to group `gitlab:ci_job`.

## 4. Use it in jobs
Every job in an authorised project gets a kubeconfig with one context per shared agent connection,
at `$KUBECONFIG`. Context name format is `<path/to/agent/project>:<agent-name>`:
```yaml
deploy:
  image: <image with kubectl>
  script:
    - kubectl config get-contexts
    - kubectl config use-context path/to/agent/project:agent-name
    - kubectl get pods
```
- Auto DevOps needs `KUBE_CONTEXT` set to the agent context (use environment-scoped variables
  for different agents per environment).
- If an environment has both a deprecated certificate-based cluster and an agent, the context
  `gitlab-deploy` is selected by default; pick the agent context explicitly.
- Self-signed KAS certificate: set `SSL_CERT_FILE`, use `--certificate-authority`, or bake the CA
  into the image (`--insecure-skip-tls-verify` is not recommended).
- Make `~/.kube/cache` writable in the job image; kubectl 1.27.0 and 1.27.1 return a 426
  validation error. Self-managed GitLab needs TLS for kubectl access.

## 5. GitOps with Flux
GitLab integrates Flux; use Flux and agentk together. Flux keeps cluster state in sync, agentk
simplifies Flux setup, manages cluster access and shows state in the GitLab UI. GitLab recommends
OCI images (GitLab container registry) over a Git repository as Flux's source. The agent
detects Flux `GitRepository` objects pointing at GitLab projects and configures a Receiver, so a
git push triggers reconciliation; its default URL is
`http://webhook-receiver.flux-system.svc.cluster.local`, overridable with
`flux.webhook_receiver_url`. Every agent with the Flux module enabled triggers reconciliations,
so disable it on agents that do not use it.

## Verify
- [ ] `kubectl config get-contexts` in an authorised job lists the agent context.
- [ ] A job from an unauthorised project has no such context.
- [ ] With `ci_job` impersonation, RBAC denies writes outside the intended namespace.

## Checked
2026-10-31. Confirmed on the agent overview, CI/CD workflow, install and GitOps pages: KAS
addresses, ci_access keys and limits, propagation, impersonation names and groups, kubeconfig
contexts, KUBE_CONTEXT, gitlab-deploy, chart RBAC options, Flux Receiver and webhook URL.
Removed as unconfirmed: removal of certificate clusters in 18.0, `replicas` and namespace
flags, example RBAC for production environments, tool image tags, version-skew and token-count
rules, observability flags, self-managed KAS toggle names, log-message meanings.
Method: documentation only; no commands were run.
