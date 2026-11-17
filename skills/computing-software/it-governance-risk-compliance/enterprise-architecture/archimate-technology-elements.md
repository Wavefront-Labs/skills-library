---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-technology-elements
name: archimate-technology-elements
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-technology-elements, archimate-technology-layer, node, device, system software, communication network, path, artifact, technology service, technology interface, technology collaboration, enterprise-architecture]
level: practitioner
status: draft
description: "Model technology structure and behaviour: node, device, system software, technology collaboration, interface, path, communication network, artifact, function, process, service."
sources:
  - https://pubs.opengroup.org/togaf-standard/
  - https://pubs.opengroup.org/architecture/archimate32-doc/
  - https://www.zachman.com/about-the-zachman-framework
  - https://www.businessarchitectureguild.org/
  - https://www.dodcio.defense.gov/Library/DoD-Architecture-Framework/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nodes, devices, system software, networks, artifacts and technology services

Goal: model infrastructure that hosts applications.

- Node is a computational or physical resource; device is a physical computer; system software provides an environment for hosting.
- Communication network connects nodes; path is a link between nodes.
- Artifact is a physical piece of data such as a file or executable; it realizes application components or data objects.
- Technology service exposes infrastructure functionality.
- Assign artifacts to nodes to show deployment.

Gotchas:
- Model logical deployment units, not every VM, unless the question needs it.

Verify: each application component is realized by at least one artifact deployed on a node.
