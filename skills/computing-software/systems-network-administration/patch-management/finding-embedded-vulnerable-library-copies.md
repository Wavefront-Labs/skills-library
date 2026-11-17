---
id: computing-software.systems-network-administration.patch-management.finding-embedded-vulnerable-library-copies
name: finding-embedded-vulnerable-library-copies
category: computing-software
field: systems-network-administration
product: patch-management
tags: [embedded-library-search, exposure-assessment, log4j, sbom-inventory, emergency-patching, syft]
level: advanced
status: draft
description: "Find vulnerable libraries bundled inside applications (Log4Shell-style): filesystem and archive scans, nested JARs, SBOM generation with syft, and vendor-bundled copies."
sources:
  - https://github.com/anchore/syft
  - https://www.cisa.gov/news-events/news/apache-log4j-vulnerability-guidance
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finding embedded vulnerable library copies

OS package managers don't know about libraries shipped **inside** applications: JARs in
WARs/EARs, Python wheels in virtualenvs, DLLs in vendor apps, OpenSSL statically linked,
node_modules. Log4Shell (2021) showed most estates couldn't answer "where is log4j-core?".

## Quick filesystem sweeps
Linux, including nested archives (JARs are zips):
```sh
find / -xdev -type f \( -name '*.jar' -o -name '*.war' -o -name '*.ear' \) 2>/dev/null > /tmp/jars.txt
while read f; do unzip -l "$f" 2>/dev/null | grep -q 'org/apache/logging/log4j/core/' && echo "HIT $f"; done < /tmp/jars.txt
```
Version from `META-INF/maven/org.apache.logging.log4j/log4j-core/pom.properties` inside the
archive (`unzip -p "$f" META-INF/maven/*/log4j-core/pom.properties`). Shaded/fat JARs nest
JARs in JARs (`BOOT-INF/lib/`): extract recursively or use a tool.
Windows:
```powershell
Get-PSDrive -PSProvider FileSystem | ForEach-Object { Get-ChildItem "$($_.Root)" -Recurse -Include *.jar,*.war,*.ear -EA 0 } |
  Select-String -Pattern 'JndiLookup.class' -SimpleMatch -List | Select Path
```

## SBOM-based (better, reusable)
```sh
syft dir:/opt -o cyclonedx-json > opt.cdx.json        # catalogues Java, Python, Node, Go, Rust, .NET, binaries
syft registry.example/app:2.3 -o spdx-json > app.spdx.json
grype sbom:opt.cdx.json --only-fixed                   # match against vulnerability DBs
```
Keep SBOMs per host/image so the next "where is X?" is a query, not a scan.

## Other places to look
- Container images (registry scan) and running images in clusters.
- Vendor appliances and commercial software: vendor advisories are the only reliable
  source; track vendor statements per product.
- CI caches and artefact repositories (Artifactory/Nexus search by component).
- Statically linked binaries (Go, Rust, OpenSSL in vendor binaries): syft/grype detect many
  via embedded build info.

## Remediation
Upgrade the application (preferred), replace the bundled library only with vendor
approval, or mitigate (remove vulnerable class, config flag) per advisory.

## Verify
Sweep results reconciled with SBOM inventory; every hit has an owner, action and status;
rerun after remediation shows no vulnerable versions.
