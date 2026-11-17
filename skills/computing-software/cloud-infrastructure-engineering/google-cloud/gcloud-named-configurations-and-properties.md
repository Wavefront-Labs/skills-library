---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gcloud-named-configurations-and-properties
name: gcloud-named-configurations-and-properties
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gcloud, named-configurations, gcloud-properties, gcloud-config, cloudsdk-active-config-name, cloudsdk-core-project, gcloud-config-configurations, multi-account-gcloud, default-region-zone]
level: practitioner
status: docs-checked
description: "Keep several GCP accounts and projects straight with gcloud named configurations, the --configuration flag and CLOUDSDK_* environment variables for scripts and CI."
sources: ["https://cloud.google.com/sdk/docs/configurations", "https://cloud.google.com/sdk/docs/properties", "https://cloud.google.com/sdk/gcloud/reference/config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gcloud named configurations and properties

**Goal:** never run a destructive command against the wrong project because the "default"
config pointed somewhere else; switch customer/env contexts in one command.

## 1. Configurations
A configuration is a named set of properties (account, project, compute/region, compute/zone...).
gcloud starts with one configuration named `default`; it is not special.
```bash
gcloud config configurations list                 # NAME IS_ACTIVE ACCOUNT PROJECT ...
gcloud config configurations create acme-prod
gcloud config configurations activate acme-prod   # only one is active at a time
gcloud config set account me@acme.example
gcloud config set project <PROJECT_ID>
gcloud config set compute/region europe-west1 ; gcloud config set compute/zone europe-west1-b
gcloud config configurations describe acme-prod
gcloud config list                                # properties of the active configuration
gcloud config configurations delete acme-old      # the active configuration cannot be deleted
```
Properties outside the `core` section need the section prefix (`compute/zone`). The config
directory is `~/.config/gcloud` on Linux and macOS and `%APPDATA%\gcloud` on Windows; find it with
`gcloud info --format='value(config.paths.global_config_dir)'`. Set `CLOUDSDK_CONFIG` to relocate
it (the directory must be writable).

## 2. Environment variables
- Any property has an environment variable named `CLOUDSDK_<SECTION>_<PROPERTY>`, for example
  `CLOUDSDK_CORE_PROJECT` and `CLOUDSDK_COMPUTE_ZONE`.
- Environment variable values take precedence over properties set with `gcloud config set`.
- `CLOUDSDK_ACTIVE_CONFIG_NAME` selects the active configuration for the current terminal.

## 3. Per-terminal context without switching globally
```bash
export CLOUDSDK_ACTIVE_CONFIG_NAME=acme-prod     # this shell only
# or run one command under another config
gcloud auth list --configuration=acme-dev
```
Tools such as direnv and ondir can set `CLOUDSDK_ACTIVE_CONFIG_NAME` per project directory.

## 4. Useful properties
```bash
gcloud config set disable_prompts true            # scripting: no prompts
gcloud config unset compute/zone
```
`gcloud topic configurations` lists every property and its section; `gcloud config set --help` has an
Available Properties section. In Cloud Shell, preferences are kept in a temporary folder for the current tab only.

## Gotchas
- Check `gcloud config list` for the account and project before destructive commands.
- A script that must target one project should set `CLOUDSDK_CORE_PROJECT` or pass `--project` explicitly rather than rely on the active configuration.

## Verify
- [ ] `gcloud config list` in each configuration shows the intended account and project.
- [ ] `gcloud config list --configuration=<other>` shows the other configuration without changing the active one.
- [ ] A script run with `CLOUDSDK_CORE_PROJECT=x` targets `x` regardless of the active configuration.

## Checked

2026-10-28. Confirmed against: the gcloud CLI "Managing configurations" and "Managing properties" pages (default configuration, create/activate/list/describe/delete, active configuration cannot be deleted, config directory locations and `CLOUDSDK_CONFIG`, `CLOUDSDK_ACTIVE_CONFIG_NAME`, `CLOUDSDK_SECTION_NAME_PROPERTY_NAME` naming, environment variables take precedence over `gcloud config set`, `--configuration` flag, direnv and ondir, `gcloud topic configurations`).

Removed: the flag-above-environment-above-config four-step precedence list (only environment over config is documented), the file name pattern, `core/log_http`, `auth/impersonate_service_account`, `billing/quota_project`, container and compute properties, the prompt-caching timing, and the `gcloud init`, `auth login`, zone and client-library gotchas.

Method: documentation only; no commands were run.
