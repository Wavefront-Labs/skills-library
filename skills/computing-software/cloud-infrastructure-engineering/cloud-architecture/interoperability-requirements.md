---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.interoperability-requirements
name: interoperability-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, opportunities-and-solutions, interoperability-requirements, togaf-phase-e, integration-standards, data-exchange, interoperability-levels]
level: practitioner
status: draft
description: "Define interoperability requirements for target cloud solutions: information, application and technical interoperability, standards, data formats and degrees of integration."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap06.html", "https://pubs.opengroup.org/togaf-standard/adm-techniques/chap06.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interoperability requirements

## TOGAF degrees (adapt)
- **Information interoperability**: shared meaning of data (common definitions, formats).
- **Application interoperability**: applications exchange and use services/messages.
- **Technical interoperability**: common network, protocols, identity.
Plus degrees from "documents exchanged manually" up to "seamless shared data and services".

## Steps
1. List system pairs that must interact in the target state (from interface catalogue).
2. For each pair, agree required degree and qualities: latency, volume, consistency, security.
3. Choose standards: protocol (HTTPS/REST, gRPC, AMQP, Kafka), payload (JSON Schema, Avro,
   Protobuf, industry standards like FHIR, ISO 20022), identity (OIDC, mTLS), time format (RFC 3339).
4. Data semantics: shared glossary and canonical identifiers; avoid a single giant canonical
   model, prefer bounded contexts with translation.
5. Document requirements per interface; include versioning and error contracts.
6. Check vendor products against them in build/buy decisions.

## Gotchas
- Assuming "has an API" equals interoperable; check semantics, rate limits and auth.
- Timezone and character encoding mismatches in files.
- Multi-cloud identity federation not planned for service-to-service calls.

## Verify
- [ ] Each target interface has a degree, standard and owner.
- [ ] Vendor shortlist checked against the requirements.
