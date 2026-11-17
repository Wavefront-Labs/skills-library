---
id: computing-software.software-engineering.java.dependency-scanning-with-owasp-and-cyclonedx-sbom
name: dependency-scanning-with-owasp-and-cyclonedx-sbom
category: computing-software
field: software-engineering
product: java
tags: [java, java-dependency-hygiene, owasp-dependency-check, cyclonedx-sbom, sbom, vulnerability-scanning]
level: practitioner
status: docs-checked
description: "Scan Maven dependencies for known CVEs with OWASP Dependency-Check and generate a CycloneDX SBOM with the CycloneDX Maven plugin: goals, thresholds, suppressions."
sources: ["https://jeremylong.github.io/DependencyCheck/dependency-check-maven/", "https://github.com/CycloneDX/cyclonedx-maven-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OWASP Dependency-Check and CycloneDX SBOM (Maven)

## Dependency-Check
The Maven plugin (`org.owasp:dependency-check-maven`) needs Maven 3.1 or higher. The first run can take 20 minutes or more while it downloads and processes the National Vulnerability Database (NVD) data; if it runs at least once every seven days later updates take seconds. So keep the data directory between CI runs rather than starting cold.

By default the plugin is tied to the `verify` phase (as a build plugin) or `site` (as a reporting plugin). Configure the `check` goal in an execution:
```xml
<plugin>
  <groupId>org.owasp</groupId>
  <artifactId>dependency-check-maven</artifactId>
  <version>${dependency-check.version}</version>
  <configuration>
    <failBuildOnCVSS>8</failBuildOnCVSS>
    <skipProvidedScope>true</skipProvidedScope>
  </configuration>
  <executions><execution><goals><goal>check</goal></goals></execution></executions>
</plugin>
```
- Output: `dependency-check-report.html` in the target directory.
- `failBuildOnCVSS` fails the build at or above that CVSS score.
- `skipProvidedScope` skips artifacts not bundled in the distribution.
- The `aggregate` report in a `<reporting>` reportSet builds one report for a multi-module site.
- The `update-only` goal refreshes the local NVD cache without analysing dependencies (useful as a separate CI step).
- `nvdDatafeedUrl` points at an internal mirror of the NVD JSON feed (the META files must be mirrored too).
- `suppressionFiles` takes several files, for example a company-wide one (URL) plus a project one, to suppress false positives.

## CycloneDX SBOM
The CycloneDX Maven plugin (`org.cyclonedx:cyclonedx-maven-plugin`) creates an SBOM of all direct and transitive dependencies. Goals:
- `makeBom`: one BOM per module.
- `makeAggregateBom`: an aggregate BOM at the build root covering the whole multi-module build (and optionally a BOM per module).
- `makePackageBom`: a BOM per module with `war` or `ear` packaging.

Bind `makeAggregateBom` to the `package` phase for the default setup. Defaults include `outputFormat` all (XML and JSON), `outputName` bom, test scope excluded, and a schema version tied to the plugin version (2.10.x writes CycloneDX 1.7, 2.9.x writes 1.6). Use the latest plugin release compatible with what the consuming system supports. BOMs are attached to the build as additional artifacts with the `cyclonedx` classifier on `install` or `deploy`; switch that off with `cyclonedx.skipAttach`, or skip a goal with `cyclonedx.skip`. With `makeAggregateBom`, exclude modules via `-DexcludeTestProject`, `-DexcludeArtifactId` or `-DexcludeGroupId`.

## Gotchas
- Scanner output is a lead, not a verdict: check whether the vulnerable code is reachable and then upgrade or suppress with a recorded reason.
- An SBOM lists components; it does not prove they are safe.

## Verify
Add a known-vulnerable version on a scratch branch and confirm the build fails at your threshold; confirm the generated `bom.json` and `bom.xml` exist in the target directory.

## Checked
Read the Dependency-Check Maven usage page in full and the CycloneDX Maven plugin README in full. Removed as unconfirmed: the NVD API key requirement and `-DnvdApiKey` flag, CPE and hash matching description, the Gradle commands and CycloneDX Gradle plugin (source not read), cache path, report formats list, suppression-file expiry syntax, and the Spring Boot Actuator sbom endpoint, Dependency-Track and Grype advice.
Method: docs-checked 2026-11-09 against the Dependency-Check Maven usage page and the CycloneDX Maven plugin README.
