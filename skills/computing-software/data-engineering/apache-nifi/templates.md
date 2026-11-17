---
id: computing-software.data-engineering.apache-nifi.templates
name: templates
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, templates, export, import, flow-sharing]
level: intro
status: docs-checked
description: "Create, upload, instantiate, download and delete NiFi templates, and the caveats on sensitive properties and dropped connections."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Templates

- Create: select components and click the Create Template button in the Operate Palette; with nothing selected the template holds the whole current Process Group (on the root group, the entire flow). You supply a name (must be unique) and an optional description.
- Upload: the Upload Template button in the Operate Palette, into any Process Group you are authorised for.
- Instantiate: drag the Template icon from the Components Toolbar onto the canvas, choose the template and click Add.
- Manage: Templates in the Global Menu lists templates with a Filter, Download (exports XML) and Delete (asks for confirmation).
- The administration guide lists `nifi.templates.directory` (default `./conf/templates`) as kept for backward compatibility only; templates are stored in flow.json.gz from NiFi 1.0, and files in that directory can be bulk-imported at startup.

Caveats from the user guide:
- Sensitive property values (such as passwords) are not included, so instantiated processors may be invalid until the values are re-entered.
- A selected connection is not included if its source or destination is not also in the template.

Verify: the instantiated flow validates after you re-enter sensitive values.

## Checked

Confirmed against the NiFi user guide (Templates section) and the administration guide (nifi.templates.directory). Removed the claim that referenced controller services are copied on each add, which the pages do not state.

Method: docs-only read of cited pages, 2026-11-08
