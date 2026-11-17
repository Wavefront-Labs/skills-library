---
id: computing-software.devops-ci-cd.build-systems.maven-settings-xml-mirrors
name: maven-settings-xml-mirrors
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, maven-mirror, settings-xml, mirror-of, artifactory, nexus, dependency-proxy]
level: practitioner
status: docs-checked
description: "Route all Maven dependency downloads through a repository manager with settings.xml mirrors: mirrorOf patterns, credentials, CI settings, blocked HTTP repos, debugging."
sources: ["https://maven.apache.org/guides/mini/guide-mirror-settings.html", "https://maven.apache.org/settings.html", "https://maven.apache.org/guides/mini/guide-encryption.html", "https://github.com/apache/maven/blob/master/apache-maven/src/assembly/maven/conf/settings.xml", "https://github.com/actions/setup-java"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Maven settings.xml mirrors

A mirror redirects requests for one or more repositories to your repository manager (Nexus, Artifactory, AWS CodeArtifact, GitHub Packages proxy), giving caching, availability, licence/security policy and audit.

## settings.xml
```xml
<settings>
  <mirrors>
    <mirror>
      <id>corp</id>
      <name>Corporate proxy</name>
      <url>https://repo.example.com/repository/maven-public/</url>
      <mirrorOf>*</mirrorOf>            <!-- everything, including repos declared in POMs -->
    </mirror>
  </mirrors>
  <servers>
    <server>
      <id>corp</id>                      <!-- must equal the mirror id -->
      <username>${env.REPO_USER}</username>
      <password>${env.REPO_TOKEN}</password>
    </server>
  </servers>
</settings>
```
`mirrorOf` patterns:
- `*` all repositories (Maven 2.0.5+).
- `external:*` everything not on localhost and not file based.
- `*,!internal-snapshots` all except one (that repo id is fetched directly).
- `central` only Maven Central.
- `external:http:*` any repository not on localhost using HTTP (since Maven 3.8.0).
Wildcards defer to explicit includes and excludes. Maven first looks for a mirror whose `mirrorOf` exactly matches the repository id, then takes the first declared mirror that matches, so order matters. There can be at most one mirror per repository; Maven does not aggregate several mirrors (use a repository manager group for that).

## Location and CI
- User: `${user.home}/.m2/settings.xml`; global: `${maven.home}/conf/settings.xml`; per-run: `mvn -s ci-settings.xml`.
- Commit a `ci-settings.xml` that reads credentials from environment variables.
- GitHub Actions: `actions/setup-java` with `server-id`, `server-username` and `server-password` (the names of environment variables holding the credentials) generates a settings.xml; CodeArtifact needs a short-lived token.
- Maven 3.x encrypts server passwords with `mvn --encrypt-password` and a master password in `settings-security.xml`; Maven's guide describes this as obfuscation-grade, so prefer your CI secret store and restrictive file permissions.

## HTTP repositories are blocked
Maven's shipped `conf/settings.xml` defines a mirror `maven-default-http-blocker` with `mirrorOf` `external:http:*` and `<blocked>true</blocked>`, so builds that pull from `http://` repositories fail (the reaction to CVE-2021-26291). Fix the POM to use HTTPS or proxy that repository through the repository manager; don't remove the blocker.

## Debugging
```bash
mvn help:effective-settings                  # which mirrors/servers are active
mvn -X dependency:resolve                    # debug log shows mirror selection and download URLs
mvn dependency:tree -U                       # -U forces update checks of snapshots / cached failures
```
Resolver failures are cached in the local repository as `*.lastUpdated` files; `-U` forces a re-check.
- `401 Unauthorized`: the server id does not match the mirror id, or the token expired.
- `Could not find artifact` only via the mirror: the proxy repository group does not include the upstream (for example a vendor repository) - add it to the group on the manager rather than bypassing the mirror.

## Verify
- [ ] `mvn -X` shows every download coming from the mirror URL; the build works with direct internet egress blocked.
- [ ] No credentials committed; CI settings use environment variables or generated files.

## Checked
Date: 2026-10-25. Documentation: Maven site sources (apache/maven-site: `guide-mirror-settings.md`, `settings.md`, `guide-encryption.md`), Maven source (apache/maven: `conf/settings.xml` assembly file, `MavenRepositorySystem.java`), actions/setup-java `action.yml`, maven-help-plugin `EffectiveSettingsMojo`.
Confirmed: mirror `id`/`url`/`mirrorOf` syntax; `*`, `external:*`, `*,!repo`, repository-id lists; `external:http:*` since 3.8.0; first-match and exact-match ordering and the one-mirror limit; settings file locations; server id matching; the shipped `maven-default-http-blocker` mirror; `mvn --encrypt-password` and `settings-security.xml` and the obfuscation-grade caveat; setup-java inputs; `help:effective-settings`.
Removed: the "3.8.1+" gate on the blocker (the pattern is 3.8.0; the blocker ships in current default settings), `.mvn/maven.config` with `-s`, the `grep` pipeline, and the `rm -rf` cache-clearing command (the cached-failure behaviour is stated without it).
Method: documentation only; no commands were run.
