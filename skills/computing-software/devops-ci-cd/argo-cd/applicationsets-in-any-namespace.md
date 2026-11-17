---
id: computing-software.devops-ci-cd.argo-cd.applicationsets-in-any-namespace
name: applicationsets-in-any-namespace
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, applicationset-in-any-namespace, applicationset-namespaces, scm-provider-allowlist, tenant-applicationsets]
level: advanced
status: docs-checked
description: "Let tenants own ApplicationSets in their namespaces: controller namespace flags, apps-in-any-namespace prerequisites, project sourceNamespaces, and SCM provider allowlists."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Appset-Any-Namespace/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/app-any-namespace/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ApplicationSets in any namespace

## 1. Enable
`argocd-cmd-params-cm`:
```yaml
data:
  application.namespaces: "team-*"                       # apps in any namespace (prerequisite)
  applicationsetcontroller.namespaces: "team-*"          # appsets in these namespaces
  applicationsetcontroller.enable.scm.providers: "false" # or restrict, see below
  applicationsetcontroller.allowed.scm.providers: "https://github.com/,https://gitlab.example.com/"
```
Restart `argocd-server`, `argocd-application-controller`, `argocd-applicationset-controller`.
The ApplicationSet controller must be a cluster-wide installation (the feature does not work with a namespace-scoped Argo CD install); the list of namespaces must match the App in any namespace list.
Restart the ApplicationSet workload after changing `argocd-cmd-params-cm` (`kubectl rollout restart -n argocd deployment argocd-applicationset-controller`).

## 2. Projects
Generated Applications are created in the ApplicationSet's namespace. Outside `argocd`, their project must list that namespace:
```yaml
kind: AppProject
spec:
  sourceNamespaces: [team-payments]
```
Because `sourceNamespaces` is checked for every Application outside `argocd`, templating `project:` is safe: an Application generated in `team-one-cd` that names another team's project is rejected.

## 3. Why the SCM restrictions
SCM provider and PR generators accept an API URL and a `tokenRef`. A tenant could point them at a
server they control and make the controller send a token read from a secret in the tenant's
namespace — or reference secrets they should not read. Allow-list SCM URLs (the URL in the AppSet `api` field must match the allow-list entry including the protocol), disable SCM
generators entirely, and consider `applicationsetcontroller.enable.tokenref.strict.mode: "true"` (the referenced secret must then carry the label `argocd.argoproj.io/secret-type: scm-creds`). The allow-list only covers providers where a custom `api` can be set.

## 4. Gotchas
- The CLI and UI refer to applications as `<namespace>/<name>`; Argo CD RBAC policies for Applications use `<project>/<namespace>/<application>`.

## Verify
- [ ] An ApplicationSet in `team-payments` generates apps visible as `team-payments/<name>`; one referencing another team's project fails.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: ApplicationSet in any namespace available from 2.8, `applicationsetcontroller.namespaces`, `enable.scm.providers`, `allowed.scm.providers`, `enable.tokenref.strict.mode` keys, cluster-wide controller prerequisite, `sourceNamespaces` check and safe project templating, `<namespace>/<name>` and RBAC format. Removed unconfirmed claims about unique names and Kubernetes RBAC for tenants. The old claim that `project:` must not be templated was wrong.

Method: documentation only; no commands were run.
