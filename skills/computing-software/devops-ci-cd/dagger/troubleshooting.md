---
id: computing-software.devops-ci-cd.dagger.troubleshooting
name: troubleshooting
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, troubleshooting, engine, buildkit, dns, cni, debug, interactive]
level: practitioner
status: docs-checked
description: "Fix common Dagger failures: unresponsive engine, DNS after network changes, CNI setup error, codegen errors with Rosetta on Mac, and debug with -i, --debug, logs."
sources: [https://docs.dagger.io/0.21/reference/troubleshooting]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting Dagger

Goal: recover from common engine problems. Dagger 0.21 docs.

## Unresponsive, BuildKit error

Symptoms: hang, `buildkit failed to respond` or `container state improper`. Stop and remove the engine container (adjust if custom-provisioned):

```shell
DAGGER_ENGINE_DOCKER_CONTAINER="$(docker container list --all --filter 'name=^dagger-engine-*' --format '{{.Names}}')"
docker container stop "$DAGGER_ENGINE_DOCKER_CONTAINER"
docker container rm "$DAGGER_ENGINE_DOCKER_CONTAINER"
```

Optionally `docker volume prune` and `docker system prune` (clears cache, so the next run is slow).

## DNS failures after network changes

Docker does not tell the engine when host networking changes (VPN, new network). Restart it: `docker restart "$DAGGER_ENGINE_DOCKER_CONTAINER"` using the variable above.

## "CNI setup error"

The engine needs the `iptable_nat` kernel module. Known affected: RHEL 8.x and 9.x, Podman Desktop on Mac. `sudo modprobe iptable_nat`; to load it at startup the page gives `echo iptable_nat | sudo tee -a /etc/modules-load.d/iptables_nat.conf` (its prose names a different file, `/etc/modules-load.d/modules`, so confirm which your distro reads).

## Code generation errors

Messages: `unable to start container process`, `failed to update codegen and runtime`, `failed to generate code`, `failed to get modified source directory for go module sdk codegen`. Cause per page: `DOCKER_DEFAULT_PLATFORM` set and/or Rosetta enabled in Docker Desktop for Mac. Unset the variable (and in shell rc files), disable Rosetta, then:

```shell
docker rm -fv $(docker ps --filter name="dagger-engine-*" -q) && docker rmi $(docker images -q --filter reference=registry.dagger.io/engine)
```

## Other techniques

- `dagger call -i` opens a terminal at the failure point (command via `--interactive-command`, default `/bin/sh`).
- `--debug` shows all output on any subcommand.
- Engine logs: `docker logs $DAGGER_ENGINE_DOCKER_CONTAINER`.
- Agents misbehaving: raise shell verbosity or read the Dagger Cloud trace, then adjust the prompt.
- Python SDK only: `from dagger.log import configure_logging` and `configure_logging(logging.DEBUG)`; use `--progress=plain` or `--debug` so output is not collapsed (e.g. `dagger call --debug echo --msg="hello"`).

Related: computing-software.devops-ci-cd.dagger.cli-running-functions, computing-software.devops-ci-cd.dagger.custom-runner-and-runtimes.

## Checked

2026-11-07

Read reference/troubleshooting.mdx in full (live slug /reference/troubleshooting matches the cited URL); it embeds no snippet files. Confirmed the BuildKit error symptoms and the stop/rm commands, the optional prune step and custom-provisioned note, the DNS restart advice, the CNI iptable_nat module and affected platforms, the four codegen error strings with DOCKER_DEFAULT_PLATFORM and Rosetta causes and the cleanup command, the agent advice, -i with --interactive-command and the /bin/sh default, --debug, engine logs, and the Python-only configure_logging(logging.DEBUG) with --progress=plain or --debug. Corrected the description, which said Apple silicon where the page says Docker Desktop for Mac with Rosetta, and flagged the page's own mismatch between the modules-load file named in prose and the one in its command.

Method: documentation only; no commands were run.
