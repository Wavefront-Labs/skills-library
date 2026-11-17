---
id: computing-software.devops-ci-cd.argocd-image-updater.run-locally-and-cli-commands
name: run-locally-and-cli-commands
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, run-locally, once, kubeconfig, warmup-cache, cli, shell-completion]
level: intro
status: docs-checked
description: "Run argocd-image-updater from a workstation for one update pass with --once, and generate shell completions for bash, zsh, fish or PowerShell."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/installation.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/completion.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running locally and the CLI commands

Binary subcommands covered by the docs: `run` (reconciliation loop), `webhook` (webhook server only), `test` (shows which tag an image would update to) and `completion` (shell autocompletion).

One-shot local run, with your kubeconfig pointing at the right cluster:

```bash
./argocd-image-updater run \
  --kubeconfig ~/.kube/config \
  --once
```

`--once` is a shortcut for `--interval 0 --health-probe-bind-address 0 --warmUpCache=true`: the tool does one update cycle and exits. When running locally, `--leader-election-namespace` must be set if leader election is on. The supported way to run continuously is the in-cluster controller.

`--kubeconfig` uses the currently active context. `argocd-image-updater --help` lists all flags.

Shell completion: `argocd-image-updater completion <bash|zsh|fish|powershell>`; each takes `--no-descriptions`.

- bash, current session: `source <(argocd-image-updater completion bash)`; Linux permanent: write to `/etc/bash_completion.d/argocd-image-updater` (needs the bash-completion package)
- zsh: run `echo "autoload -U compinit; compinit" >> ~/.zshrc` once, then `source <(argocd-image-updater completion zsh)`
- fish: `argocd-image-updater completion fish | source`
- PowerShell: `argocd-image-updater completion powershell | Out-String | Invoke-Expression`

## Checked

2026-11-08. Read in full: docs/install/installation.md, docs/install/cmd/run.md, docs/install/cmd/completion.md and docs/install/cmd/test.md. Confirmed the --once shortcut, the kubeconfig note, the leader election namespace note, the in-cluster controller as the supported continuous mode, and the completion commands and flags for each shell. Removed: the template subcommand, which none of the cited pages document.

Method: documentation only; no commands were run.
