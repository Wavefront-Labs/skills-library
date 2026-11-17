---
id: computing-software.devops-ci-cd.spinnaker.service-dependencies-and-ports
name: service-dependencies-and-ports
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [architecture, ports, dependencies, gate, orca, clouddriver, networking]
level: practitioner
status: docs-checked
description: "Use the Spinnaker service dependency graph and default port table to plan firewall rules, health checks and which services must be reachable from which."
sources:
  - https://spinnaker.io/docs/reference/architecture/microservices-overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Architecture page publishes a dependency graph and a default port table. Use both when writing network policy or debugging connection refused errors between services.

**Default ports:** Clouddriver 7002, Deck 9000, Echo 8089, Fiat 7003, Front50 8080, Gate 8084, Igor 8088, Kayenta 8090, Orca 8083, Rosco 8087, Keel 7010. The current page's table does not list Halyard.

**Who depends on whom (from the graph):**
- Deck and any custom script or API caller depend only on Gate.
- Gate depends on Kayenta, Orca, Clouddriver, Rosco, Front50, Fiat, Echo, Igor and Keel.
- Orca depends on Clouddriver, Front50, Rosco, Kayenta and Fiat.
- Clouddriver and Front50 each depend on Fiat.
- Echo depends on Orca and Front50; Igor depends on Echo.
- Keel depends on Clouddriver, Orca, Front50, Fiat, Echo and Igor.

Because each service can run in its own server group, the page notes that services typically resolve dependencies through load balancers or discovery systems such as Eureka or Consul. Practical consequence: Fiat sits under Gate, Orca, Clouddriver and Front50, so a Fiat outage surfaces as failures in all of them.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Spinnaker Architecture Overview page (reference/architecture/microservices-overview). Confirmed the dependency edges and the port table; corrected Keel to 7010 and removed Halyard's port and the Halyard daemon sentence, which the page no longer carries. The Fiat consequence is derived from the graph.
