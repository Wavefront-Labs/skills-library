---
id: computing-software.devops-ci-cd.jenkins.pinning-plugin-versions
name: pinning-plugin-versions
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, plugin-management, plugin-pinning, plugins-txt, jenkins-plugin-cli, immutable-controller-image, renovate-jenkins, plugin-lockfile, reproducible-jenkins, custom-jenkins-image]
level: practitioner
status: docs-checked
description: "Pin every Jenkins plugin (including transitive ones) in plugins.txt baked into an image, generate the lock set, update via PRs, and stop UI upgrades drifting the controller."
sources: ["https://github.com/jenkinsci/plugin-installation-manager-tool", "https://github.com/jenkinsci/docker/blob/master/README.md", "https://docs.renovatebot.com/modules/manager/jenkins/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pinning plugin versions

## Goal
The controller's plugin set is fully determined by a file in git; rebuilding the image
in six months yields byte-identical plugins.

## 1. Pin everything, not just top-level
In `plugins.txt` a plugin with no version, or `:latest`, resolves to the latest version at build time, and
dependencies are taken from update-center metadata (or the plugin's MANIFEST.MF) unless you use `--latest`/`--latest-specified`
options. To see exactly what a list resolves to without downloading:
```bash
jenkins-plugin-cli --jenkins-version 2.462.3 --plugin-file plugins.txt --no-download --list
```
`--list` prints installed, bundled, to-be-downloaded and the effective plugin set (highest version of each).
Copy the effective set into `plugins.txt` as `artifactId:version`, one per line (`#` comments allowed), and re-resolve
whenever you change the list or the core version.

## 2. Bake into the image
```dockerfile
FROM jenkins/jenkins:2.462.3-lts-jdk21
COPY --chown=jenkins:jenkins plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt --verbose
COPY casc/ /var/jenkins_home/casc_configs/
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/casc_configs
```
Files under `/usr/share/jenkins/ref` seed `$JENKINS_HOME` and do not overwrite existing files unless
the reference file name ends in `.override`. To force upgrades of plugins that were upgraded manually, run the image
with `-e PLUGINS_FORCE_UPGRADE=true`.

## 3. Updates via PR
Renovate's `jenkins` manager matches `plugins.txt`/`plugins.yaml` files and reads versions from the main
Jenkins update center; or run a scheduled job:
`jenkins-plugin-cli -f plugins.txt --available-updates --output txt` (the Jenkins Docker README uses this to write a new
`plugins.txt`) and open a PR. CI boots the image with the JCasC and runs a smoke pipeline before merge.

## 4. Lock the UI
Remove `Overall/Administer` from people who'd click *Update all*, or accept that UI
installs vanish at next deploy (with ephemeral HOME).

## Gotchas
- `:latest` or no version anywhere in the file = drift.
- Security advisories: pinned does not mean frozen; subscribe to the advisories feed and
  patch within days.
- `experimental` and `incrementals;...` versions come from the experimental update center
  (`--jenkins-experimental-update-center` / `JENKINS_UC_EXPERIMENTAL`) and the incrementals repo
  (`--jenkins-incrementals-repo-mirror`); avoid in production.
- With `--latest`, a mirror can list a plugin version whose file is not yet published and fail the download;
  pin versions to avoid it.

## Verify
Two image builds a week apart produce identical `/usr/share/jenkins/ref/plugins` hashes, and the
plugin versions shown on the running controller match `plugins.txt`.

## Checked
2026-10-31. Confirmed against the plugin-installation-manager-tool README (`--list`, `--no-download`, `--available-updates`, `--output`, `--jenkins-version`, version syntax, mirror options), the Jenkins Docker README (ref directory, `.override`, `PLUGINS_FORCE_UPGRADE`) and the Renovate Jenkins manager page. Removed: the awk lock recipe and `Resolved plugins` heading, Helm chart values, `pluginManager/api/json`.
Method: documentation only; no commands were run.
