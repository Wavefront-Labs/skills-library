---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-plugins-and-krew
name: kubectl-plugins-and-krew
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, krew, kubectl-plugins, kubectl, cli, developer-experience]
level: practitioner
status: docs-checked
description: "Extend kubectl with plugins: how plugin discovery and naming work, installing and pinning plugins with krew and custom indexes, a useful plugin set, and writing your own."
sources: ["https://kubernetes.io/docs/tasks/extend-kubectl/kubectl-plugins/", "https://krew.sigs.k8s.io/docs/user-guide/", "https://github.com/kubernetes-sigs/krew/blob/master/site/content/docs/user-guide/using-custom-indexes.md", "https://github.com/kubernetes-sigs/krew/blob/master/site/content/docs/developer-guide/installing-locally.md", "https://krew.sigs.k8s.io/plugins/", "https://github.com/kubernetes-sigs/krew-index"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl plugins and krew

## How plugins work
Any executable on `PATH` named `kubectl-<name>` becomes `kubectl <name>`.
- Dashes in the file name become subcommands: `kubectl-foo-bar` runs as `kubectl foo bar`.
- An underscore in the file name gives a dashed command: `kubectl-foo_bar` runs as
  `kubectl foo-bar` (or `kubectl foo_bar`). kubectl picks the longest matching file name.
- Plugins cannot override existing commands (`kubectl-version` is never run) or extend commands
  other than `create` (`kubectl-create-something` works).
- They inherit kubectl's environment (`KUBECONFIG`) and receive all args and flags as-is; the
  plugin parses its own flags.
```bash
kubectl plugin list          # also warns about shadowed/unexecutable plugins
```

## Krew
Install per the krew docs, add `${KREW_ROOT:-$HOME/.krew}/bin` to `PATH`, then:
```bash
kubectl krew update
kubectl krew search secret
kubectl krew install ctx ns neat tree who-can view-secret stern df-pv
kubectl krew list
kubectl krew upgrade
```
Useful set: `ctx`/`ns` (context switching), `neat` (strip managed fields from YAML),
`tree` (ownerReference hierarchy), `who-can` (RBAC reverse lookup), `view-secret` (decode),
`stern` (multi-pod logs), `df-pv` (PV usage), `rbac-tool`, `node-shell` (use carefully),
`pv-migrate`.

## Teams: pin and distribute
For reproducible tooling:
- Install from a manifest: `kubectl krew install --manifest=foo.yaml --archive=foo.tar.gz`
  in a toolbox image (`--archive` replaces the manifest's download `uri`).
- Host a **custom index** (git repo of plugin manifests):
```bash
kubectl krew index add corp https://git.example.com/platform/krew-index.git
kubectl krew install corp/platform-login
```
- Or skip krew and ship plugins in the devcontainer / toolbox image.

## Writing a plugin
```bash
cat > ~/bin/kubectl-podimages <<'EOF'
#!/usr/bin/env bash
# kubectl podimages [-n ns]: unique images running in a namespace
kubectl get pods "$@" -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | sort -u
EOF
chmod +x ~/bin/kubectl-podimages && kubectl podimages -n kube-system
```
For Go plugins use the `k8s.io/cli-runtime` libraries, which provide helpers for kubeconfig
parsing and the standard kubectl flags.

## Security
The krew index is community-curated and not audited for security. Plugins run with your credentials;
review the source of anything touching secrets or nodes, and prefer a curated custom index
in regulated environments.

## Verify
- [ ] `kubectl plugin list` shows no warnings; the plugin respects `--context`/`-n`.

## Checked
2026-10-27, against the Kubernetes docs page "Extend kubectl with plugins" (kubernetes/website main, v1.38 dev tree), the krew site docs (kubernetes-sigs/krew `site/content/docs`) and the krew-index plugin list. Confirmed: dash and underscore naming, longest-name matching, no overriding of existing commands with the `create` exception, inherited environment, `kubectl plugin list` warnings, `kubectl krew index add` and `INDEX/PLUGIN` installs, `install --manifest --archive`, cli-runtime, the not-audited caution, and that every named plugin is in krew-index.
Method: documentation only; no commands were run.
