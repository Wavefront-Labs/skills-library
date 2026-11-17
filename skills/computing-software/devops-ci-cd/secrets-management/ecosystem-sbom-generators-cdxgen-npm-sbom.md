---
id: computing-software.devops-ci-cd.secrets-management.ecosystem-sbom-generators-cdxgen-npm-sbom
name: ecosystem-sbom-generators-cdxgen-npm-sbom
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, cdxgen, npm-sbom, cyclonedx, spdx, cyclonedx-maven-plugin, sbom-generation]
level: practitioner
status: gated
description: "Generate accurate SBOMs from the package ecosystem itself: cdxgen, npm sbom, CycloneDX Maven/Gradle plugins, cargo-cyclonedx and dotnet tools, versus image scanners like syft."
sources:
  - https://cyclonedx.github.io/cdxgen/
  - https://docs.npmjs.com/cli/v10/commands/npm-sbom
  - https://github.com/CycloneDX/cyclonedx-maven-plugin
  - https://cyclonedx.org/tool-center/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ecosystem SBOM generators

Image/filesystem scanners (syft, trivy) infer components from installed files. Ecosystem generators read the lockfile and resolver graph, so they include dependency relationships, scopes (dev vs runtime) and exact resolved versions. Use ecosystem SBOMs for the source/build SBOM and an image scanner for the deployable.

## cdxgen (polyglot)
```bash
npm install -g @cyclonedx/cdxgen        # or docker run ghcr.io/cdxgen/cdxgen:master (README image name; not run, no Docker)
cdxgen -r -o bom.json .                  # -r (recurse) is already the default in the version run here; --no-recurse turns it off
cdxgen -t js -o bom.json --spec-version 1.6 .   # default spec is 1.7; choices 1.4-1.7 and 2 (run: 1.6 written)
cdxgen --required-only -o bom-runtime.json .   # exclude dev/test scopes where the ecosystem marks them
FETCH_LICENSE=true cdxgen -o bom.json .        # pull licence data from registries (docs: npm and golang)
```
Run on a 2-dependency npm lockfile: 2 components and a 3-node `dependencies` graph. Evidence comes from the separate `evinse` command (cdxgen docs), not a `--evinse` flag; for Java/Gradle it invokes the build tool, so the toolchain must be installed in CI.

## npm
```bash
npm sbom --sbom-format cyclonedx --omit dev > bom.cdx.json   # npm 9.5+; run on npm 10.8.2: CycloneDX 1.5; spdx gives SPDX-2.3
npm sbom --package-lock-only --sbom-format spdx > bom.spdx.json
```
Requires a valid lockfile; workspaces with `--workspace`.

## Maven / Gradle
```xml
<plugin>
  <groupId>org.cyclonedx</groupId><artifactId>cyclonedx-maven-plugin</artifactId><version>2.9.3</version>
  <executions><execution><phase>package</phase><goals><goal>makeAggregateBom</goal></goals></execution></executions>
  <configuration><includeTestScope>false</includeTestScope><outputFormat>json</outputFormat></configuration>
</plugin>
```
The Maven and Gradle plugins were checked against their READMEs and Maven Central metadata (2.9.3 latest), not run (gated: unconfirmed, no JDK/Gradle here).
Gradle: `id("org.cyclonedx.bom") version "3.5.1"` then `./gradlew cyclonedxBom` (output `build/reports/cyclonedx/bom.json`) (configure `includeConfigs = ["runtimeClasspath"]`).

## Others
- Python (`pip install cyclonedx-bom`, 7.5.0): `cyclonedx-py environment` (run: 35 components for a venv) or `cyclonedx-py requirements requirements.txt` (run: CycloneDX 1.6); `poetry` and `pipenv` subcommands exist.
- Go: `cyclonedx-gomod app -main ./cmd/server -json -output bom.json` (run: needs a git repository, else `failed to determine version of main module: no git repository found`).
- Rust: `cargo cyclonedx --format json` (gated: unconfirmed, not installed here).
- .NET: `dotnet CycloneDX MySolution.sln -o out -j` (gated: unconfirmed, not run).

## In CI
- Generate at build time from the exact commit, attach to the release and attest it (`cosign attest --type cyclonedx`).
- Validate: `cyclonedx validate --input-file bom.json` (cyclonedx-cli; it auto-detects the schema version) and check NTIA minimum elements.
- Feed to Dependency-Track or a scanner (`grype sbom:bom.json`) for continuous vulnerability matching.

## Pitfalls
- Running without a lockfile produces version ranges, not resolved versions: always lock.
- Vendored or copied code (C libraries, minified JS) is invisible to ecosystem tools; complement with file scanners.
- Merge per-service SBOMs with `cyclonedx merge` only when you really ship them together.

## Verify
- [ ] SBOM lists the same resolved versions as the lockfile and has a `dependencies` graph.
- [ ] SBOM is produced and attached for every release build.
