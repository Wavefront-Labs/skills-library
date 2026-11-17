---
id: computing-software.cloud-infrastructure-engineering.google-cloud.installing-gcloud-and-managing-components
name: installing-gcloud-and-managing-components
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gcloud, gcloud-install, gcloud-components, gcloud-init, google-cloud-sdk, gke-gcloud-auth-plugin, gcloud-update, apt-cloud-sdk, gcloud-version-pinning, ci-gcloud]
level: practitioner
status: docs-checked
description: "Install the gcloud CLI per platform (tarball installer, apt, Windows installer), add components like gke-gcloud-auth-plugin, pin or roll back versions and run gcloud init."
sources: ["https://cloud.google.com/sdk/docs/install", "https://cloud.google.com/sdk/docs/components", "https://cloud.google.com/sdk/docs/initializing", "https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing gcloud and managing components

**Goal:** a gcloud that updates cleanly on laptops and is reproducible in CI, with the extra components
(`kubectl`, `gke-gcloud-auth-plugin`, `beta`) installed where needed.

## 1. Pick the install method by how you will update it
| Method | Updates via | Notes |
|---|---|---|
| Archive plus `install.sh` (Linux, macOS) | `gcloud components update` | `*.tar.gz` from the downloads URL on the install page |
| Windows installer (`GoogleCloudSDKInstaller.exe`) | `gcloud components` | bundles Python 3 unless you untick the option |
| apt or yum package `google-cloud-cli` | the package manager | the component manager is disabled for package installs |

```bash
# archive, Linux x86_64
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh        # prompts: add to PATH, command completion, usage statistics
./google-cloud-sdk/install.sh --help # flags for non-interactive installs
# Debian/Ubuntu (newer distributions)
sudo apt-get install ca-certificates gnupg curl
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install google-cloud-cli
```
To replace an archive install, delete the existing `google-cloud-sdk` directory and extract the new archive
there. The apt package holds gcloud, alpha, beta, gsutil and bq only; it does not include `kubectl` or the
App Engine extensions, so install those separately. In resource-constrained VMs, container images and CI
runners, `CLOUDSDK_SKIP_PY_COMPILATION=1` during install skips Python byte-compilation (faster install, slightly
slower interactive commands). The install page lists the supported Python range (3.10 to 3.15 at the time of
reading); Linux x86_64 and Arm packages bundle their own interpreter.

## 2. Components
```bash
gcloud components list                         # status, name, ID, size
gcloud components install kubectl
gcloud components install gke-gcloud-auth-plugin
gcloud components install beta                 # alpha, beta, preview are separate components
gcloud components update                       # all installed components to latest
gcloud components update --version VERSION     # revert to a known good version (non-package installs)
gcloud components remove COMPONENT-ID
```
The default components are `gcloud` (GA commands only), `bq`, `gsutil` and `core`. Run component commands from outside
the `google-cloud-cli` install directory; on Windows an All Users install needs an Administrator terminal.
With apt or yum the components are separate packages, for example `apt-get install google-cloud-cli-gke-gcloud-auth-plugin`
(`yum install` for the same name). Downgrading a package install uses the package manager's version syntax.

`kubectl` and other Kubernetes clients need `gke-gcloud-auth-plugin` to authenticate to GKE; the GKE page says that
before Kubernetes 1.26 gcloud starts to require the binary, and without it existing kubectl installations stop
working. Verify with `gke-gcloud-auth-plugin --version`.

## 3. Initialise
```bash
gcloud init --console-only          # --console-only prints the auth URL instead of opening a browser
gcloud config list                  # properties set by init: account, project, region/zone
```
`gcloud init` authenticates (as does `gcloud auth login`) and creates or re-initializes a configuration; on a new
installation it creates a configuration named `default`. If you only have access to one project it selects it;
the default Compute Engine zone step is skipped if the Compute Engine API is not enabled or a project default
exists. CI usually skips `init` and sets properties explicitly (`gcloud config set project <PROJECT_ID>`).

## Gotchas
- Mixing an archive install with an apt install leaves two gclouds on PATH with different component managers; `command -v gcloud` shows which one runs.
- Pin the version in CI (the `--version` form above, or the package manager's version syntax) so flag changes between releases do not break pipelines.
- Corporate proxies: see the proxy-settings skill (`proxy/type`, `proxy/address`, `proxy/port`, `core/custom_ca_certs_file`).

## Verify
- [ ] `gcloud components list` (archive installs) shows the components you need as Installed.
- [ ] `gke-gcloud-auth-plugin --version` runs if GKE is used.
- [ ] `command -v gcloud` shows exactly the binary you expect.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the install page (archive URL, `install.sh` prompts, apt steps and package contents,
`CLOUDSDK_SKIP_PY_COMPILATION`, Windows installer and bundled Python), the components page (list, install, update,
`--version`, remove, default components, package-manager caveat) and the initialising page (`--console-only`,
`default` configuration, project and zone behaviour), and the GKE kubectl page (`gke-gcloud-auth-plugin`, package names).
Removed: Homebrew and Docker image rows, image tags, the GitHub Action snippet, pinned version numbers, `%APPDATA%` and
`~/.config` locations, `CLOUDSDK_PYTHON`, the `gcloud version` claims and the exact kubectl error message.
