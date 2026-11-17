---
id: computing-software.devops-ci-cd.jenkins.removing-deprecated-plugins
name: removing-deprecated-plugins
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, plugin-management, plugin-removal, deprecated-plugins, adopt-this-plugin, plugin-usage, old-data-monitor, blue-ocean-deprecation, plugin-hygiene, attack-surface]
level: advanced
status: docs-checked
description: "Find and safely remove unused or deprecated Jenkins plugins: deprecation and Plugin Usage checks, dependency order, Old Data cleanup and rollback."
sources: ["https://www.jenkins.io/doc/book/managing/plugins/#uninstalling-plugins", "https://www.jenkins.io/doc/developer/plugin-governance/deprecating-or-removing-plugin/", "https://plugins.jenkins.io/plugin-usage-plugin/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removing deprecated plugins

Every plugin is attack surface, startup time and upgrade risk.

## 1. Find candidates
- *Manage Jenkins -> Plugins -> Installed*: **Deprecated** badge (plugin marked
  deprecated in the UC, often with a suggested replacement) and *up for adoption*
  (unmaintained). The *Manage Jenkins* page also shows a deprecation monitor.
- **Plugin Usage** plugin: lists, per plugin, the jobs whose config uses its classes.
  Plugins used by no job, not in JCasC and not a dependency of anything are removable.
- Script console (admin) for dependents:
  ```groovy
  def pm = Jenkins.instance.pluginManager
  pm.plugins.findAll { !it.isDeleted() }.each { p ->
    def users = pm.plugins.findAll { it.dependencies.any { d -> d.shortName == p.shortName } }*.shortName
    println "${p.shortName}\t${p.version}\t${users}"
  }
  ```
- Pipeline usage doesn't show in job XML: grep Jenkinsfiles and shared libraries for the
  plugin's step names .

## 2. Remove in order
1. Replace usage (e.g. deprecated plugin -> its successor), deploy, observe a week.
2. Remove leaf plugins first (nothing depends on them), then their now-orphan deps.
3. Image-managed: delete it from the plugin list your image build installs from, rebuild.
   UI-managed: *Uninstall* (disabled until no installed plugin depends on it), restart.
4. Restart and check the log for plugin load errors.

## 3. Clean leftover data
Jobs configured with a removed plugin keep unknown XML; *Manage Jenkins -> Manage Old Data*
lets you review and remove configuration left behind by uninstalled plugins: purge it only after
you're sure you won't roll back.

## Rollback
Keep the previous image tag or a copy of the `.jpi` files and reinstall the exact version if needed.
Re-installing a plugin brings back configuration values that were left behind, until you remove old data.

## Gotchas
- Uninstall greyed out = something depends on it; disable first to test impact (*Disable*
  is reversible and keeps data).
- Detached plugins re-appear because older plugins implicitly depend on them; upgrade
  those plugins.

## Verify
Plugin count dropped, no plugin load errors on start, Old Data monitor empty, and a sample
of pipelines across teams still pass.

## Checked

2026-10-28. Confirmed from the Jenkins plugin-management page (uninstalling: only plugins that are not dependencies of others are offered for uninstall; disabling as a softer retirement; Manage Old Data purges configuration left behind; re-installing restores left-over values; implied dependencies on detached features) and the Plugin Usage plugin page. Removed (not found in the pages): the 30-50% figure, Deprecated badge and adoption monitor details, example step names, `plugins-top.txt` and `plugins.txt`, exception names, Discard Unreadable Data, the Blue Ocean umbrella gotcha. The script-console snippet and grep advice are procedure, not documented claims.

Method: documentation only; no commands were run.
