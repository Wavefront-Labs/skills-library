---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeconfig-contexts-and-exec-credential-plugins
name: kubeconfig-contexts-and-exec-credential-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeconfig, kubeconfig-contexts, kubectl-config, exec-credential-plugin, kubeconfig-merging, cka]
level: practitioner
status: docs-checked
description: "Manage kubeconfig files: KUBECONFIG merging, contexts and namespaces, kubectl config subcommands, and client-go exec credential plugins."
sources: ["https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_config/", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/#client-go-credential-plugins"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubeconfig contexts and exec credential plugins

## Structure
`clusters` (server + CA), `users` (credentials), `contexts` (cluster + user + namespace),
`current-context`. A context is just a named triple.

## Merging rules
`KUBECONFIG=a:b:c` (`;` on Windows) merges files: **the first file to set a particular value or
map key wins**, so `current-context` comes from the first file that sets it, and if two files
define `red-user` only the first file's `red-user` is used. If `--kubeconfig` is set, only that
file is used with no merging. With neither, `$HOME/.kube/config` is used. File and path
references inside a kubeconfig are relative to that file's location.
```bash
export KUBECONFIG=~/.kube/config:~/.kube/prod.yaml
kubectl config view --flatten > <merged-file>   # then review it and move it into place
```

## Everyday commands
```bash
kubectl config get-contexts
kubectl config current-context
kubectl config use-context prod-admin
kubectl config set-context --current --namespace=payments
kubectl config rename-context <old-name> prod
kubectl config delete-context old; kubectl config delete-cluster old; kubectl config delete-user old
kubectl config view --minify --raw          # just the current context, with secrets
kubectl --context=staging get pods          # one-off without switching
```
kubectx/kubens (krew `ctx`, `ns`) make switching fast; put the context in your prompt.

## Exec credential plugins
client-go (and so kubectl and kubelet) can run an external command that returns user
credentials as an `ExecCredential` object (stable since v1.22). It is configured under
`user.exec`:
```yaml
users:
- name: my-user
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1   # must match what the plugin returns
      command: example-client-go-exec-plugin
      args: [arg1, arg2]
      env: [{name: FOO, value: bar}]
      interactiveMode: Never        # required in v1: Never, IfAvailable or Always
      provideClusterInfo: false     # true passes cluster info via KUBERNETES_EXEC_INFO
      installHint: "example-client-go-exec-plugin is required"
```
Cloud providers ship their own tools that generate such entries (AWS, GKE and AKS CLIs);
follow your provider's documentation for the exact command. Most plugin designs also need a
server-side webhook token authenticator to interpret the credential.

## Gotchas
- `client.authentication.k8s.io/v1alpha1` ExecCredential was removed in Kubernetes 1.24;
  kubeconfigs that still use it must be regenerated or migrated to `v1` (`v1beta1` is still
  present in the client-go source). `interactiveMode` is optional in `v1beta1` and required in `v1`.
- The `apiVersion` the plugin returns must match the one in the kubeconfig.
- If the plugin executable is not found, kubectl shows the optional `installHint`.
- `--namespace` on the context is just a default; it does not restrict access.
- Only use kubeconfig files from trusted sources; a crafted file can lead to code execution
  (it can name a command to run) or file exposure.

## Verify
- [ ] `kubectl config get-contexts` shows clean names; `kubectl auth whoami` works per context.
- [ ] CI kubeconfigs use exec plugins or short-lived tokens, not long-lived embedded admin certs.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Organizing Cluster Access Using kubeconfig
Files", "Authenticating" (client-go credential plugins) and "Configure Access to Multiple
Clusters", plus the kubectl `config` command source (latest release v1.37.1). Confirmed: first
file wins merge rule and `;` Windows separator, `--kubeconfig` no-merge rule, relative paths,
`config view` flags `--flatten`, `--minify`, `--raw`, the delete/rename subcommands, exec plugin
fields and `v1` requirements, v1alpha1 removal in 1.24 (release notes). Removed unconfirmed claims
(cloud CLI commands, error message text, file permission warning, update-target rule).
Method: documentation only; no commands were run.
