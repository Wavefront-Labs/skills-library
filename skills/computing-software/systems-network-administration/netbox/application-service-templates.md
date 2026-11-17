---
id: computing-software.systems-network-administration.netbox.application-service-templates
name: application-service-templates
category: computing-software
field: systems-network-administration
product: netbox
tags: [application-service, service-template, ports]
level: practitioner
status: docs-checked
description: "Create service templates and attach services to devices or VMs."
sources: ["https://netboxlabs.com/docs/netbox/features/ipam/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Application service mapping

Goal: catalogue which applications listen where.

NetBox models network applications as discrete **service** objects associated with devices and/or virtual machines, and optionally with specific IP addresses attached to those parents. They catalogue the applications running on your hosts.

**Method**

1. Create an application service template defining the name, protocol and port number(s) on which the service listens.
2. Instantiate the template to attach new services to a device or VM.
3. Optionally limit the service to particular IP addresses on that parent.

Services can also be created by hand without a template, but that is tedious. Using a template means the name, protocol and ports are defined once and reused.

**Checklist**

1. Build templates for standard services.
2. Attach to the right parent.
3. Scope to IP addresses where it matters.

## Checked

Method: docs-checked 2026-11-09 against https://netboxlabs.com/docs/netbox/features/ipam/ (downloaded; read the Application Service Mapping section). Dropped unconfirmed notes about multiple ports per service, prefix parentage and REST API availability.
