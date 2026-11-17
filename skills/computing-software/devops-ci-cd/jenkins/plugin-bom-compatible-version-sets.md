---
id: computing-software.devops-ci-cd.jenkins.plugin-bom-compatible-version-sets
name: plugin-bom-compatible-version-sets
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, plugin-bom, plugin-management, plugin-pinning]
level: advanced
status: docs-checked
description: "Use the Jenkins plugin BOM to choose mutually compatible plugin versions per LTS line, both for plugin development and for pinning controller plugins.txt."
sources: ["https://github.com/jenkinsci/bom", "https://www.jenkins.io/doc/developer/plugin-development/dependency-management/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin BOM compatible version sets

`jenkinsci/bom` publishes Maven BOMs (`io.jenkins.tools.bom:bom-<lts>.x`, e.g. `bom-2.504.x`, plus a
`bom-weekly` line that follows weekly core) to manage plugin dependency versions for your plugin's LTS baseline.

## Plugin development (pom.xml)
```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>io.jenkins.tools.bom</groupId>
      <artifactId>bom-${jenkins.baseline}.x</artifactId>
      <version>LATEST-VERSION-FOR-THAT-LINE</version>
      <scope>import</scope>
      <type>pom</type>
    </dependency>
  </dependencies>
</dependencyManagement>
```
Then declare plugin dependencies without versions. Take the current version for your line from the table in the jenkinsci/bom README (it lists e.g. `bom-2.504.x` with its own `NNNN.v...` version; the BOM version is not the core version).

## Controller pinning
The BOM is for builds, but its version set is a good basis for `plugins.txt`:
1. Pick the BOM matching your LTS line.
2. Resolve your plugin list against it (e.g. a small Maven project importing the BOM and
   `mvn dependency:list`), emit `name:version` lines.
3. `jenkins-plugin-cli --plugin-file plugins.txt --jenkins-version <your LTS> --list` to see the
   resulting plugin set before building the image.
Plugins not in the BOM: pin explicitly and test in staging.

## Gotchas
- `jenkins-plugin-cli --latest false` downloads the minimum required version of all dependencies instead of the latest.
- Use the `bom-weekly` line only when you track weekly core releases.

## Verify
- [ ] `jenkins-plugin-cli ... --list` shows no unexpected versions; the staging controller boots with all plugins loaded.

## Checked
2026-11-02. Confirmed against the jenkinsci/bom README (BOM artifact naming bom-<baseline>.x, bom-weekly, version table) and the plugin-installation-manager-tool README (--plugin-file, --jenkins-version, --list, --latest false). Corrected: version 5054.v620b_5d2b_d5e6 belongs to bom-2.479.x, not bom-2.504.x. Removed: PCT description, Dependabot/Renovate claim, LTS-drop and weekly-mixing claims, error message strings.
Method: documentation only; no commands were run.
