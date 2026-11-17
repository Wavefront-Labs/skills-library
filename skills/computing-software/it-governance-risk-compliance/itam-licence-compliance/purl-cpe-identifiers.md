---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.purl-cpe-identifiers
name: purl-cpe-identifiers
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [purl-cpe-identifiers, vex-and-vulnerability-linkage, purl, package url, cpe, cpe 2.3, identifier, swid tagid, ecosystem, namespace, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Construct purl and CPE identifiers correctly so SBOM components match vulnerability databases."
sources:
  - https://github.com/package-url/purl-spec
  - https://google.github.io/osv.dev/post-v1-query/
  - https://csrc.nist.gov/projects/security-content-automation-protocol/specifications/cpe
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/external-repository-identifiers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package URL and CPE identifiers

Goal: reliable component identity for matching.

purl format: pkg:type/namespace/name@version?qualifiers#subpath, for example pkg:maven/org.apache.logging.log4j/log4j-core@2.17.1, pkg:npm/%40angular/core@17.0.0, pkg:pypi/requests@2.31.0, pkg:deb/debian/openssl@3.0.11?arch=amd64.
CPE 2.3 (NIST's current published CPE version) formatted string: cpe:2.3:a:vendor:product:version:*:*:*:*:*:*:* (the SPDX 2.3 spec uses the same form in a SECURITY cpe23Type external reference).
Rules: the type is lowercase and namespace, name and version are percent-encoded. For OS packages the namespace is the vendor (e.g. debian, ubuntu) and the distro goes in a qualifier (distro=...).

Method: emit purl for every component; add CPE where a consumer matches on CPE; OSV can be queried by purl (package.purl in its query API).

Gotchas:
- Treat CPE matches as candidates and confirm them.
- Version strings should be literal from the package manager.

Verify: lookup 5 components in OSV by purl.

## Checked

2026-11-02. Checked against the purl-spec repository (scheme:type/namespace/name@version?qualifiers#subpath, how-to-build lowercase type and percent-encoding, deb namespace is the vendor with distro qualifier, npm %40 scope example, maven group id as namespace, pypi lowercase), the OSV query API page (package.purl), the NIST CPE page (CPE 2.3 current) and SPDX 2.3 Annex F. Removed: the NVD usage and backlog claims (NVD pages are not readable by script).

Method: documentation only; no commands were run.
