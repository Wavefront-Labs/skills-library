---
id: computing-software.devops-ci-cd.dagger.install-dagger-cli
name: install-dagger-cli
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, install, cli, upgrade, telemetry, container-runtime, faq]
level: practitioner
status: docs-checked
description: "Install or upgrade the Dagger CLI on macOS, Linux or Windows, pin a version, use package managers, and handle telemetry, privileged-engine and Cloud trace FAQs."
sources: [https://docs.dagger.io/0.21/getting-started/installation, https://docs.dagger.io/0.21/faq]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install the Dagger CLI

Goal: get a working `dagger` CLI at a chosen version (Dagger 0.21 docs).

## Prerequisite

A container runtime. Docker works out of the box; Podman, nerdctl and Apple Container also work.

## Install script (pins a version via DAGGER_VERSION)

macOS:
```shell
curl -fsSL https://dl.dagger.io/dagger/install.sh | DAGGER_VERSION=<version> BIN_DIR=/usr/local/bin sh
```
If the user cannot write to `/usr/local/bin`, run the script with `sudo -E sh`.

Linux (user-level; make sure `$HOME/.local/bin` is on `PATH`):
```shell
curl -fsSL https://dl.dagger.io/dagger/install.sh | DAGGER_VERSION=<version> BIN_DIR=$HOME/.local/bin sh
```
System-wide: `BIN_DIR=/usr/local/bin` with `sudo -E sh`.

Windows, PowerShell 7 or later:
```powershell
iwr -useb https://dl.dagger.io/dagger/install.ps1 | iex; Install-Dagger -DaggerVersion <version> -AddToPath
```
This installs `dagger.exe` in the user profile `dagger` folder and adds it to the user `PATH`.

Verify: `dagger version` prints `version: v<version>`. To upgrade or switch versions, re-run the install with the desired version.

## Package managers

`brew install dagger/tap/dagger` (macOS) or `winget install Dagger.Cli` (Windows) carry only the latest stable release. To run a specific release from a package-managed CLI, set `DAGGER_X_RELEASE=v<version>` for the shell session or pass `--x-release=v<version>` per command; the CLI builds and caches that release on first use. Unset the variable to return to the installed version.

## FAQ points worth knowing

- Telemetry: the CLI sends anonymized telemetry (Dagger version, platform, command run, anonymous device ID). Disable it with `DO_NOT_TRACK=1`.
- The Engine must run in a privileged container (rootless limits overlayfs and network performance); secure it like Docker or Kubernetes, with the host as the boundary.
- Building Windows containers is not supported right now (Dagger runs on BuildKit, where Windows container support is still experimental).
- Registry login from an SDK: use the `withRegistryAuth` API method, or run `docker login` on the host.
- Dagger Cloud is bring-your-own-compute. Traces from CI with incomplete Git metadata are "orphaned"; in GitHub Actions run the `checkout` action in the step that calls Dagger. Setting `CI=true` forces traces from an unsupported CI.
- `dagger functions` appears in the local trace list because module introspection needs engine initialization.

Next: `computing-software.devops-ci-cd.dagger.ci-workflow-quickstart`.

## Checked

2026-11-07

Read getting-started/installation.mdx and introduction/faq.mdx in full (live slugs /getting-started/installation and /faq; the old /introduction/faq URL returned 404, fixed in sources). Confirmed the container-runtime prerequisite, the three install-script variants with DAGGER_VERSION and BIN_DIR, sudo -E, the Windows PowerShell 7 command, version verification, the Homebrew and winget commands, DAGGER_X_RELEASE and --x-release behaviour, and the FAQ items on telemetry (four data points, DO_NOT_TRACK=1), the privileged engine, registry login, bring-your-own-compute, orphaned traces, CI=true and dagger functions. Dropped the getting-started index page from sources because no claim relied on it and it was not read. Reworded the Windows containers line, which the FAQ phrases as not supported right now.

Method: documentation only; no commands were run.
