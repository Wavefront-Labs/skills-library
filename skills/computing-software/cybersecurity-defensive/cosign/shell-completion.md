---
id: computing-software.cybersecurity-defensive.cosign.shell-completion
name: shell-completion
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, completion, bash, zsh, fish, powershell]
level: intro
status: docs-checked
description: "Enable cosign tab completion for bash, zsh, fish and PowerShell with cosign completion."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_completion.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign completion

Syntax: `cosign completion [bash|zsh|fish|powershell]`.

Bash:
```
source <(cosign completion bash)
cosign completion bash > /etc/bash_completion.d/cosign                 # Linux, once
cosign completion bash > /usr/local/etc/bash_completion.d/cosign       # macOS, once
```

Zsh (enable compinit first if needed):
```
echo "autoload -U compinit; compinit" >> ~/.zshrc
cosign completion zsh > "${fpath[1]}/_cosign"
```
Start a new shell afterwards.

Fish:
```
cosign completion fish | source
cosign completion fish > ~/.config/fish/completions/cosign.fish
```

PowerShell:
```
cosign completion powershell | Out-String | Invoke-Expression
cosign completion powershell > cosign.ps1
```
Then source that file from your PowerShell profile.

## Checked

2026-11-04. Confirmed against the cosign docs page cosign_completion: syntax and every command in the bash, zsh, fish and PowerShell sections. Removed: the closing statement that completion is a quick way to see which flags your version supports (not on the page).
Method: documentation only; no commands were run.
