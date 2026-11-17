---
id: computing-software.devops-ci-cd.spinnaker.halyard-install
name: halyard-install
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [halyard, install, hal, docker, debian, ubuntu, macos]
level: intro
status: docs-checked
description: "Install Halyard on Debian/Ubuntu or in Docker, check it with hal -v, update and uninstall it without losing the .hal configuration by accident. The page marks Halyard deprecated."
sources:
  - https://spinnaker.io/docs/setup/install/halyard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page is headed "Deprecated - Halyard": Halyard is no longer supported and the page is kept for historical purposes. Halyard is the command-line tool that writes and validates your Spinnaker configuration, deploys each microservice and updates the deployment. The page recommends installing it on a machine with at least 12GB of RAM.

**Local install** (Ubuntu 18.04 or higher, Debian 10 or higher): `curl -O https://raw.githubusercontent.com/spinnaker/halyard/master/install/debian/InstallHalyard.sh`, run `sudo bash InstallHalyard.sh` (default answers are usually suitable), then check with `hal -v`. If that fails, make sure `hal` is on the PATH and check `/var/log/spinnaker/halyard/halyard.log`. Run `. ~/.bashrc` for command completion; append `-h` to any hal command for help. Update with `sudo apt-get update` then `sudo apt --only-upgrade install spinnaker-halyard`; the page says this works only with Halyard v1.45.0 and higher.

**Docker install:** create a local `.hal` directory, then run the Halyard image `us-docker.pkg.dev/spinnaker-community/docker/halyard:stable` with `-p 8084:8084 -p 9000:9000`, `--name halyard --rm`, `-it`, and `-v ~/.hal` mounted at the spinnaker user's `.hal` directory in the container. Fix permissions on the mounted directory yourself. Any secret or kubeconfig Halyard needs must be mounted in `~/.hal` or another directory added with `-v`. Replacing `-it` with `-d` runs detached, but the daemon logs are not persisted. Open a shell with `docker exec -it halyard bash`. To update, pull the image, `docker stop halyard` and re-run it. To uninstall, `docker rm halyard`.

**Uninstall warning:** uninstalling Halyard on Debian/Ubuntu (`sudo ~/.hal/uninstall.sh`) deletes the entire `~/.hal` directory. Run `hal deploy clean` first only if you want to purge the deployment too.

## Checked

2026-11-04. Platforms, 12GB recommendation, install and update commands, Docker run options and the uninstall warning were confirmed on the Install Halyard page. Removed: macOS support, older Ubuntu/Debian versions, the Java 11 requirement and `update-halyard` (none on the current page).

Method: documentation only; no commands were run.
