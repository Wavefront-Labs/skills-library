---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-shell-editor-and-customisation
name: cloud-shell-editor-and-customisation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-shell, cloud-shell-editor, cloud-shell-customization, customize-environment, cloudshell-open, web-preview, cloud-shell-limits, persistent-home, cloud-shell-tutorials]
level: intro
status: docs-checked
description: "Make Cloud Shell useful: persist tooling with .customize_environment, persist gcloud config, use Web Preview, open-in-Cloud-Shell links, and the home-disk limits."
sources: ["https://docs.cloud.google.com/shell/docs/how-cloud-shell-works", "https://docs.cloud.google.com/shell/docs/configuring-cloud-shell", "https://docs.cloud.google.com/shell/docs/using-web-preview", "https://docs.cloud.google.com/shell/docs/open-in-cloud-shell"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Shell editor and customisation

**Goal:** a Cloud Shell that has your tools, dotfiles and repos ready quickly, used for what it is
good at (already-authenticated gcloud, quick edits, demos) within its limits.

## 1. What you get and the limits
Each session is an ephemeral Debian-based Compute Engine VM owned by Google (it does not appear in
your projects); your environment is a Docker container on it. The session ends after an hour of
inactivity and the VM is discarded. **5 GB of free persistent disk is mounted as `$HOME`**, per user
and across projects, and cannot be expanded (Cloud Workstations offers more). If you delete `$HOME`
or do not use Cloud Shell for **120 days**, `$HOME` is deleted and unrecoverable (you get an email
first). Software installed outside `$HOME` is lost when the instance terminates. The container
image is updated weekly. Check the limitations guide for usage quotas.

## 2. Persist your tools
`$HOME/.customize_environment` runs **as root** once at VM boot (not per shell), as a background
process, so packages may appear a few moments after the prompt:
```bash
#!/bin/sh
apt-get update
apt-get -y install fzf ripgrep
```
Logs: `/var/log/customize_environment`; on success it touches `/google/devshell/customize_environment_done`.
`.bashrc` and other files in `$HOME` persist.

## 3. Persist gcloud configuration
By default gcloud preferences live in a temporary folder for the current tab only and do **not**
persist. Either append `gcloud config set ...` commands to `$HOME/.bashrc` (every tab inherits them
and can still change its own), or add `export CLOUDSDK_CONFIG=$HOME/.config/gcloud` to `.bashrc`
and create a named configuration with `gcloud config configurations create CONFIG_NAME`.
At start the console's active project is copied into gcloud config and `GOOGLE_CLOUD_PROJECT` is
set; `CLOUD_SHELL=true` marks the environment.

## 4. Web Preview
Run a web app listening on a port from 2000 to 65000 on the VM; the Web Preview button (top right
of the taskbar) opens it through the Cloud Shell proxy, restricted to your user over HTTPS. The
URL format is `https://$PORT-$WEB_HOST` (`WEB_HOST` is set in the terminal). Streamlit behind this
proxy needs `--browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false`.

## 5. Open-in-Cloud-Shell links
```
https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/<org>/<repo>&cloudshell_tutorial=README.md&cloudshell_workspace=.
```
Required: `cloudshell_git_repo` (only GitHub and Bitbucket permitted by default). Optional:
`cloudshell_git_branch` (default branch master), `cloudshell_image`, `cloudshell_open_in_editor`,
`cloudshell_print`, `cloudshell_tutorial`, `cloudshell_workspace` (`cloudshell_working_dir` is
deprecated), `ephemeral` (true/false), `show` (`ide`, `terminal`, `ide%2Cterminal`).
Only allow-listed repos owned by Google open in the default environment with your credentials;
all others use a temporary environment without access to your credentials. A `cloudshell_image`
must be hosted in Artifact Registry, publicly accessible, and based on the base Cloud Shell image;
it opens a temporary environment with a scratch home directory.

## Gotchas
- `.customize_environment` runs as root, so anything needing the user's `$HOME` must use the explicit path.
- Ephemeral mode has no persistent disk: faster start, all files lost at session end.
- A broken `.bashrc` or `.tmux.conf` closes the session on connect; open Safe Mode by appending `cloudshellsafemode=true` to the URL.

## Checked
2026-10-31. Confirmed against the Cloud Shell pages how-cloud-shell-works, configuring-cloud-shell, using-web-preview and open-in-cloud-shell: ephemeral VM, one-hour inactivity, 5 GB `$HOME`, 120-day deletion, weekly image update, `.customize_environment` behaviour and logs, gcloud config persistence, port range 2000-65000 and `WEB_HOST` URL form, all URL parameters and their constraints, safe mode. Removed: VM size and Boost mode, 50 hours/week quota, 20-minute idle timeout, Editor details, `gcloud cloud-shell ssh/scp` instructions, Docker/kubectl persistence claims, organisation-policy name, custom-image base image path.
Method: documentation only; no commands were run.

## Verify
- [ ] Open a new session; the packages from `.customize_environment` are present within a minute or two.
- [ ] Web Preview of a local server on port 8080 renders in the browser.
- [ ] An open-in-Cloud-Shell link clones the repo and shows the tutorial panel.
