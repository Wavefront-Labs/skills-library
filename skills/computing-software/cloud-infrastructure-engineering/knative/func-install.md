---
id: computing-software.cloud-infrastructure-engineering.knative.func-install
name: func-install
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [func-cli, kn-func, install-func, homebrew, knative-functions]
level: intro
status: docs-checked
description: "Install the standalone func CLI or the kn func plugin for Knative Functions."
sources:
  - https://knative.dev/docs/functions/install-func/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get a working Knative Functions client.

You can install Knative Functions either with the standalone `func` CLI, or as the `kn func` plugin for the Knative `kn` CLI.

Standalone `func`:
- Homebrew: `brew tap knative-extensions/kn-plugins`, then `brew install func`. Use `brew upgrade` when upgrading. If `kn` was already installed with Homebrew, `func` is automatically recognized as a plugin, so `kn func` and `func` are interchangeable.
- Executable binary: download the binary for your system from the `func` release page, rename it to `func`, make it executable, move it to a directory on your PATH such as `/usr/local/bin`, and verify with `func version`.
- Go: check out the `func` client repository and build it from source with `make`.
- Container image: run `func` from the `ghcr.io/knative/func/func` image; nothing is placed on your PATH, so repeat this each time.

```bash
mv /path/to/func_linux_amd64 func
chmod +x func
mv func /usr/local/bin
func version
```

`kn func` plugin:
1. Download the same release binary.
2. Rename it to `kn-func` and make it executable.
3. Move it to a directory on your PATH.
4. Verify with `kn func version`.

The Functions docs show the create, build, run and deploy commands in both forms, `func <command>` and `kn func <command>`, so pick one install and use the matching spelling. Local build, run and deploy workflows also need a Docker daemon on your machine, which the Quickstart installation already provides.

## Checked

2026-11-04. Confirmed against the Installing Knative Functions page and the install snippets it includes (knative/docs source): standalone `func` or `kn func` plugin, the Homebrew tap and install commands, `brew upgrade`, automatic plugin recognition when `kn` came from Homebrew, the binary download, rename, `chmod +x`, move to a PATH directory and `func version`, the Go source build, the `kn-func` rename for the plugin and `kn func version`. The Docker daemon prerequisite comes from the Deploying and Building functions pages. Added the `make` step and the container-image option from the install snippet, and narrowed 'every command' to the commands the docs actually show in both forms.

Method: documentation only; no commands were run.
