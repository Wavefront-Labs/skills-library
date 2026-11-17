---
id: computing-software.software-engineering.java.versions-maven-plugin-and-release-process
name: versions-maven-plugin-and-release-process
category: computing-software
field: software-engineering
product: java
tags: [java, java-maven, versions-maven-plugin, maven-release-plugin, revision-property, flatten-maven-plugin, semantic-versioning]
level: practitioner
status: docs-checked
description: "Maintain and release Maven versions: versions-maven-plugin display and set goals, CI-friendly ${revision} with the flatten plugin, and maven-release-plugin."
sources: ["https://www.mojohaus.org/versions/versions-maven-plugin/", "https://maven.apache.org/maven-ci-friendly.html", "https://maven.apache.org/maven-release/maven-release-plugin/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# versions-maven-plugin and release process

## Finding and applying updates
```bash
mvn versions:display-dependency-updates         # report of dependencies with newer versions
mvn versions:display-plugin-updates             # same for plugins (respects Maven prerequisites)
mvn versions:display-property-updates           # version-controlling properties with newer versions
mvn versions:use-latest-releases                # edits pom.xml: replaces release versions with the latest release
mvn versions:set -DnewVersion=2.3.0             # set the project version from the command line
mvn versions:commit        # removes pom.xml.versionsBackup files; versions:revert restores from them
```
The edit goals back up each pom as `pom.xml.versionsBackup`; review the diff and commit separately. `versions:resolve-ranges` replaces version ranges with the specific version in use, and `versions:update-child-modules` re-syncs child parent versions. The plugin also supports ignoring versions through rules; see its site for the rules file mechanism.

## CI-friendly versions (Maven 3.5.0-beta-1 and later)
```xml
<version>${revision}</version>
<properties><revision>1.0.0-SNAPSHOT</revision></properties>
```
`${revision}`, `${sha1}` and `${changelist}` can be placeholders for the version. Override on the command line with `mvn -Drevision=1.4.0 clean package`. To install or deploy with this setup you must use the Flatten Maven Plugin, otherwise the artifacts in the repository will not be consumable by Maven. Where dependencies refer to sibling modules, use `${project.version}`; using `${revision}` there fails the build.

## Release flow
The Maven Release Plugin releases in two steps, `release:prepare` (prepare for a release in SCM) and `release:perform` (perform the release from SCM). Other goals include `release:rollback`, `release:branch` and `release:update-versions`. A tag-driven CI release with `-Drevision` is an alternative to the plugin's commit-and-tag flow.

## Checked

Method: docs-checked 2026-11-09 against the versions-maven-plugin site index (goal list), the Maven CI Friendly Versions page (placeholders, -Drevision, flatten requirement, project.version note) and the maven-release-plugin index (prepare and perform). Dropped unconfirmed claims (allowMajorUpdates and generateBackupPoms flags, rules.xml property, flattenMode value, enforcer requireReleaseDeps, Central signing, Dependabot and Renovate comparison, version-range and updateMatchingVersions notes).
