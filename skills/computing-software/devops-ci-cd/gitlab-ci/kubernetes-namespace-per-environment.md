---
id: computing-software.devops-ci-cd.gitlab-ci.kubernetes-namespace-per-environment
name: kubernetes-namespace-per-environment
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, environment-kubernetes-namespace, review-namespace, environment-kubernetes-agent, namespace-teardown]
level: advanced
status: docs-checked
description: "Give each review environment its own Kubernetes namespace via the agent: slug naming, creation, environment:kubernetes for the dashboard, and teardown."
sources: ["https://docs.gitlab.com/ci/environments/kubernetes_dashboard/", "https://docs.gitlab.com/ci/yaml/#environmentkubernetes", "https://docs.gitlab.com/user/clusters/agent/ci_cd_workflow/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes namespace per environment

## 1. Deploy job
```yaml
deploy-review:
  image: { name: bitnami/kubectl:1.31, entrypoint: [""] }
  variables:
    KUBE_NS: review-$CI_ENVIRONMENT_SLUG
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_ENVIRONMENT_SLUG.review.example.com
    on_stop: stop-review
    kubernetes:
      agent: platform/agents:review          # <project path>:<agent name>
      dashboard:
        namespace: review-$CI_ENVIRONMENT_SLUG   # `namespace` directly under kubernetes: is deprecated since GitLab 18.4
  script:
    - kubectl config use-context platform/agents:review
    - kubectl create namespace "$KUBE_NS" --dry-run=client -o yaml | kubectl apply -f -
    - kubectl label namespace "$KUBE_NS" gitlab.com/environment=review --overwrite
    - helm upgrade --install app ./chart -n "$KUBE_NS" --set ingress.host="$CI_ENVIRONMENT_SLUG.review.example.com" --wait
```
`environment:kubernetes` links the environment to the agent/namespace so the **Kubernetes dashboard**
on the environment page shows pods and status (it does not create the namespace).

## 2. Naming
`CI_ENVIRONMENT_SLUG` is a DNS-safe, shortened form of the environment name (see the predefined variables page for the exact rules), so it suits namespace names (Kubernetes limit 63 chars) and DNS labels. Do not use `CI_COMMIT_REF_NAME` (slashes, uppercase).

## 3. Teardown
```yaml
stop-review:
  extends: deploy-review
  environment: { name: review/$CI_COMMIT_REF_SLUG, action: stop }
  variables: { GIT_STRATEGY: none }
  when: manual
  script:
    - kubectl config use-context platform/agents:review
    - kubectl delete namespace "$KUBE_NS" --wait=false --ignore-not-found
```

## 4. Guard rails
- Agent `ci_access` should authorize only the review project/groups, and impersonate a service
  account with RBAC limited to `review-*` namespaces (cannot touch prod namespaces in the same cluster).
- Apply a ResourceQuota + LimitRange per namespace (template it in the deploy job) so a bad MR cannot eat the cluster.
- Wildcard DNS `*.review.example.com` + one wildcard TLS cert.

## Verify
- [ ] Environment page dashboard shows the namespace's workloads.
- [ ] After MR merge, the namespace is gone (`kubectl get ns -l gitlab.com/environment=review`).

## Checked

2026-11-02. Confirmed against the GitLab `environment:kubernetes` reference and Kubernetes dashboard page: `agent` format path/to/agent/project:agent-name (17.6), `namespace` deprecated in 18.4 in favour of `dashboard:namespace`, dashboard needs the agent installed with `user_access` configured. Confirmed against the agent CI/CD workflow page: `ci_access` projects/groups, kubeconfig contexts in format <agent project path>:<agent name>, impersonation as the hardening option. Fixed: deprecated `namespace` keyword. Removed: the exact slug length figure (not on fetched pages).

Method: documentation only; no commands were run.
