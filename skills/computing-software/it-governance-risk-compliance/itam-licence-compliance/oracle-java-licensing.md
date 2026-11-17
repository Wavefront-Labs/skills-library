---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.oracle-java-licensing
name: oracle-java-licensing
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [oracle-java-licensing, oracle-licensing, oracle java, java se subscription, openjdk, per employee, jdk, temurin, itam-licence-compliance]
level: advanced
status: draft
description: "Assess Java SE subscription exposure under Oracle's per-employee model and consider OpenJDK alternatives."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oracle Java SE licensing

Goal: understand and reduce Java licensing exposure.

Facts to confirm: Oracle changed Java SE licensing in 2019 (Java SE Subscription by Processor/Named User Plus) and again in January 2023 (Java SE Universal Subscription priced per employee). Oracle JDK builds have licence terms that differ by version (NFTC for some releases; confirm each).
Method:
1. Inventory every Java runtime/JDK by vendor (java -version output, vendor string, registry, package manager).
2. Classify: Oracle JDK/JRE, OpenJDK builds (Eclipse Temurin, Amazon Corretto, Microsoft Build, Azul Zulu), embedded Java in products.
3. For Oracle runtimes, check licence for that version and use case.
4. Plan migration to OpenJDK builds and test applications.

Gotchas:
- Bundled Java in third-party apps follows the app vendor terms.
- Oracle contact campaigns often target download logs.

Verify: remaining Oracle Java count is zero or covered.
