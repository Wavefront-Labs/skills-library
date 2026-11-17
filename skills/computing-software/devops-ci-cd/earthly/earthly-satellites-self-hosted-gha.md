---
id: computing-software.devops-ci-cd.earthly.earthly-satellites-self-hosted-gha
name: earthly-satellites-self-hosted-gha
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, satellites, self-hosted, earthly-satellite-image, gha-runner, earthly-gha-add, satellite-host, kubernetes]
level: advanced
status: docs-checked
description: "Run self-hosted Earthly satellites with the earthly/satellite image (env vars, EC2, Kubernetes, debugging) and use them as GitHub Actions runners via earthly gha add."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/self-hosted.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/gha-runners.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Self-hosted satellites and GitHub Actions runners

## Start a self-hosted satellite (beta)
```bash
docker run --privileged \
    -v satellite-cache:/tmp/earthly:rw \
    -p 8372:8372 \
    -e EARTHLY_TOKEN=<earthly_token> \
    -e EARTHLY_ORG=my-org \
    -e SATELLITE_NAME=my-satellite \
    -e SATELLITE_HOST=153.65.8.0 \
  earthly/satellite:v0.8.13
```
Required env vars: `EARTHLY_TOKEN` (from `earthly account create-token <token-name>`), `EARTHLY_ORG`, `SATELLITE_NAME`, `SATELLITE_HOST` (hostname or IP the CLI connects to; `localhost` and `127.0.0.1` are rejected). Earthly Cloud never connects to the satellite; it registers itself. `--privileged` is currently required. Leaving `SATELLITE_HOST` unset tries auto-discovery (experimental, cloud-init environments such as EC2). CLI `v0.8.0`+ is needed.

Use it: `earthly sat select my-satellite` or `earthly --sat my-satellite +my-target`. `earthly sat ls` shows size `self-hosted` and state `operational` or `offline`; remove offline ones with `satellite rm` (`earthly sat rm --force` if it still shows operational after an ungraceful stop).

Optional env vars: `SATELLITE_PORT`, `CACHE_SIZE_PCT` (1-100), `BUILDKIT_MAX_PARALLELISM`, `BUILDKIT_SESSION_TIMEOUT` (default 24h), `CACHE_KEEP_DURATION` (seconds), `RUNNER_DISABLE_TLS`, `LOG_LEVEL` (default INFO), `BUILDKIT_DEBUG`, `EARTHLY_ADDITIONAL_BUILDKIT_CONFIG` (TOML). The cache dir is `/tmp/earthly`; mount a volume there.

EC2: use Amazon Linux 2023 and a cloud-init `runcmd` that installs docker, enables the service, then runs `sudo docker run -d --privileged --restart always --name satellite -p 8372:8372 -v /earthly-cache:/tmp/earthly:rw -e EARTHLY_TOKEN=... -e EARTHLY_ORG=my-org -e SATELLITE_NAME=my-satellite earthly/satellite:v0.8.13`. Kubernetes: privileged pod, port 8372, `/tmp/earthly` volume, `SATELLITE_HOST` from `status.podIP` via the Downward API.

Local test: add `127.0.0.1	earthly.local` to /etc/hosts and set `SATELLITE_HOST=earthly.local`.

Debugging: a log containing `SATELLITE IS NOT REGISTERED` means bad run-command values. A log line `running server on [::]:9372` is BuildKit's; the exposed port is still 8372.

## GitHub Actions runners (experimental)
1. Create a non-expiring GitHub classic token with scopes `admin:org`,`admin:org_hook` (org) or `repo`,`admin:repo_hook` (repo).
2. `earthly gha add --org <earthly_organization> --gh-org <github_organization> [--gh-repo <github_repo>] --gh-token <github_token>`.
3. Enable at satellite creation: `earthly satellite launch --feature-flag enable-gha-runner <satellite-name>`; self-hosted: `-e RUNNER_GHA_ENABLED=true` plus `-v /var/run/docker.sock:/var/run/docker.sock` and `earthly/satellite:v0.8.13` or newer. Expect the log `starting GitHub Actions job polling loop`.
4. In the workflow: `runs-on: [earthly-satellite#<satellite-name>]`, with `EARTHLY_TOKEN` from secrets in the job env.

Manage with `earthly gha ls --org <earthly_organization>` and `earthly gha remove --org ... --gh-org ... [--gh-repo ...]`.

## Checked

2026-11-07. Read in full against the Earthly docs pages self-hosted.md and gha-runners.md: docker run command with --privileged and port 8372, the required and optional environment variables, localhost/127.0.0.1 rejection, cloud-init auto-discovery limits, the v0.8.0 CLI requirement, offline-satellite resolution, the EC2 and Kubernetes guides, and the GitHub Actions runner steps all match. Nothing removed.
Method: documentation only; no commands were run.
