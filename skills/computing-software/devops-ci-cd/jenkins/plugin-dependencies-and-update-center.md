---
id: computing-software.devops-ci-cd.jenkins.plugin-dependencies-and-update-center
name: plugin-dependencies-and-update-center
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, plugin-management, plugin-dependencies, update-center, update-site, jenkins-plugin-cli, transitive-dependencies, optional-dependencies, minimum-jenkins-version, plugin-manager-tool, dependency-hell]
level: practitioner
status: docs-checked
description: "Understand Jenkins plugin dependency resolution: update center JSON, required vs optional dependencies, minimum core versions, resolving with jenkins-plugin-cli, upgrades."
sources: ["https://www.jenkins.io/doc/book/managing/plugins/", "https://github.com/jenkinsci/plugin-installation-manager-tool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin dependencies and the update center

## How resolution works
- The **update center** (`https://updates.jenkins.io/update-center.json?version=<core>`)
  publishes plugin metadata including each plugin's `requiredCore` and `dependencies`
  (each with a name, version and `optional` flag). Plugins are downloaded with their dependencies from it.
- The plugin tool takes dependency versions from update-center metadata, or the plugin's MANIFEST.MF if that is
  unavailable; `--latest false` downloads the minimum required version of each dependency.
- **Implied dependencies**: plugins that do not raise their minimum core version keep dependencies on plugins that were
  split out of core, because core cannot tell whether the old APIs are needed. The plugin manager shows them when you hover
  over *Uninstall*; a new plugin release with a newer minimum core removes them.

## Resolve offline, deterministically
```bash
jenkins-plugin-cli --jenkins-version 2.462.3 \
  --plugin-file plugins.txt --plugin-download-directory ./plugins \
  --list --view-all-security-warnings
```
`--list` prints installed, bundled, to-be-downloaded and effective plugin sets;
`--available-updates` shows newer versions; `--view-all-security-warnings` shows every plugin with warnings. In the official image:
`RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt`.

## Reading failures
When a plugin fails to load, find the dependency it names (too old or missing), fix that first, then its dependents.
Removing a `.jpi` file by hand leaves dependents broken after restart; reinstall via `plugins.txt`.

## Upgrade discipline
- Upgrade core first within LTS, then plugins via the update center for *that* core, so
  the UC gives versions known to work with it.
- Upgrade all plugins together from a resolved set, not one at a time from the UI; mixed
  ages are the usual cause of dependency failures.
- Check the *Installed* tab of the plugin manager after each change.

## Verify
Every plugin is enabled in the plugin manager and the startup log shows no plugin load failures.

## Checked
2026-10-31. Confirmed against the plugin-installation-manager-tool README (`--list`, `--available-updates`, `--latest`, `--view-all-security-warnings`, dependency source), the Jenkins plugin-management page (implied dependencies) and the live update-center JSON (`requiredCore`, `dependencies`, `optional`). Corrected: `--view-security-warnings` does not exist (`--view-all-security-warnings`). Removed: `default.json` path, detached-plugin examples, error-message strings, custom update-site UI path, the `pluginManager/api/json` check.
Method: documentation only; no commands were run.
