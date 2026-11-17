---
id: computing-software.software-engineering.uv.uv-installation-methods
name: uv-installation-methods
category: computing-software
field: software-engineering
product: uv
tags: [uv, install, standalone-installer, homebrew, self-update, shell-completion, installation]
level: practitioner
status: docs-checked
description: "Install uv with the standalone installer, pip, Homebrew, WinGet, Scoop or Cargo, update it, enable shell completion, and uninstall it cleanly."
sources: [https://docs.astral.sh/uv/getting-started/installation/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing and updating uv

Goal: get uv onto a machine by the method that suits it, keep it current, and remove it when needed.

## Method

Standalone installer (macOS and Linux):

```console
$ curl -LsSf https://astral.sh/uv/install.sh | sh
$ wget -qO- https://astral.sh/uv/install.sh | sh
$ curl -LsSf https://astral.sh/uv/0.13.7/install.sh | sh
```

The wget form is for systems without curl; the last form pins a version in the URL. Inspect the script first with `curl -LsSf https://astral.sh/uv/install.sh | less`.

Windows:

```pwsh-session
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Put a version in the URL (`https://astral.sh/uv/0.13.7/install.ps1`) to pin it.

Package managers:

- PyPI: `pipx install uv` (recommended, isolated) or `pip install uv`. If no wheel exists for the platform, uv builds from source and needs a Rust toolchain.
- Homebrew: `brew install uv`
- MacPorts: `sudo port install uv`
- WinGet: `winget install --id=astral-sh.uv  -e`
- Scoop: `scoop install main/uv`
- Cargo: `cargo install --locked uv` (builds from source)
- Docker image: `ghcr.io/astral-sh/uv`
- Binaries: GitHub Releases

Upgrade: `uv self update` works only when uv came from the standalone installer. Otherwise use the package manager, e.g. `pip install --upgrade uv`. Updating re-runs the installer and may change shell profiles; set `UV_NO_MODIFY_PATH=1` to prevent that.

Shell completion (restart the shell afterwards):

```bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc
```

The page also gives fish, Elvish and PowerShell variants; uvx completion uses `uvx --generate-shell-completion <shell>`.

Uninstall: optionally run `uv cache clean`, then remove `"$(uv python dir)"` and `"$(uv tool dir)"`, then delete the `uv` and `uvx` binaries from `~/.local/bin` (also `uvw` on Windows).

## Gotchas

- Before 0.5.0 uv installed into `~/.cargo/bin`; upgrading does not remove those old binaries.
- Windows execution-policy bypass is what lets the internet script run.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (getting-started/installation). Removed or changed: removed an invented Verify step.

Method: documentation only; no commands were run.
