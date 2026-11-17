---
id: computing-software.devops-ci-cd.jenkins.offline-plugin-installation-and-mirrors
name: offline-plugin-installation-and-mirrors
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, plugin-management, plugin-mirror, offline-plugins, air-gapped, jenkins-uc, update-center-mirror, artifactory-jenkins-mirror, jenkins-plugin-cli, hpi-upload, proxy]
level: advanced
status: docs-checked
description: "Install and update Jenkins plugins without internet: pre-download with jenkins-plugin-cli, update-center and download-URL mirror settings, and manual .hpi upload."
sources: ["https://github.com/jenkinsci/plugin-installation-manager-tool", "https://www.jenkins.io/doc/book/managing/plugins/#advanced-installation", "https://www.jenkins.io/doc/book/installing/offline/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline plugins and mirrors

## Option A: build the plugin set where internet exists, ship artifacts
```bash
jenkins-plugin-cli --jenkins-version 2.462.3 --plugin-file plugins.txt \
  --plugin-download-directory ./plugins --verbose
tar czf jenkins-plugins-2.462.3.tgz plugins/
```
Carry the tarball (or a Docker image built with it) across the air gap. Copy into
`$JENKINS_HOME/plugins/` (name files with the `.jpi` suffix), or bake into
`/usr/share/jenkins/ref/plugins/` (the tool's default download directory on Linux; note it deletes and recreates the
directory). The Plugin Installation Manager Tool downloads the listed plugins and all their dependencies, which is why
the docs recommend it for offline installs.

## Option B: internal mirror of the update site
Point `jenkins-plugin-cli` at a mirror of updates.jenkins.io. The update-center JSON is fetched from the mirror but the
URLs inside it still point at updates.jenkins.io, so also set the download URL (no path segment is added for you):
```bash
jenkins-plugin-cli --plugin-file plugins.txt --latest false \
  --jenkins-update-center "https://mirror.example.com/<updates-path>/update-center.actual.json" \
  --jenkins-plugin-info "https://mirror.example.com/<updates-path>/current/plugin-versions.json" \
  --jenkins-update-center-download-url "https://mirror.example.com/<updates-path>/download/plugins"
```
Environment equivalents: `JENKINS_UC`, `JENKINS_PLUGIN_INFO`, `JENKINS_UC_DOWNLOAD_URL` (`JENKINS_UC_DOWNLOAD` is
deprecated). Add `--jenkins-experimental-update-center` / `--jenkins-incrementals-repo-mirror` only if you install
experimental or incrementals plugins. `--credentials` (or `JENKINS_UC_CREDENTIALS`) supplies basic auth per host.

## Option C: manual upload
Plugin manager Advanced tab, *Deploy Plugin* section: choose a `.hpi` file or enter a URL; or copy the file into
`JENKINS_HOME/plugins` named with a `.jpi` suffix. Transferring individual plugins means you must fetch all their
dependencies too. Fine for one hotfix, unmanageable at scale.

## Gotchas
- On first start of an offline controller the setup wizard cannot download plugins: choose *Select plugins to install*, then *None*, then *Install*, and
  add plugins with one of the methods above.
- Pass `--jenkins-version` (or `--war`) so plugins are resolved for the core you run.

## Verify
The isolated controller's plugin list matches the resolved list and the startup log shows no plugin load failures.

## Checked
2026-10-31. Confirmed against the plugin-installation-manager-tool README (mirror flags, environment variables, deprecation of `JENKINS_UC_DOWNLOAD`, default download directory, `--credentials`), the Jenkins plugin-management page (`.hpi`/`.jpi`, Deploy Plugin) and the Offline Installations page (recommended tool, setup wizard steps). Removed: signed-UC and `update-center2` advice, `noSignatureCheck`, proxy settings, checksum, security-feed and warning claims.
Method: documentation only; no commands were run.
