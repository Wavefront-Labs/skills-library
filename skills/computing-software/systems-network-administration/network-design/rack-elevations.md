---
id: computing-software.systems-network-administration.network-design.rack-elevations
name: rack-elevations
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, documentation, rack-elevation, dcim, rack-diagram, netbox]
level: practitioner
status: docs-checked
description: "Produce and maintain rack elevation diagrams: front/rear views, U positions, power and airflow annotations, DCIM tools like NetBox, and audit against reality."
sources:
  - https://docs.netbox.dev/en/stable/models/dcim/rack/
  - https://www.comptia.org/certifications/network
  - https://tiaonline.org/products-and-services/tia942certification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rack elevations

## What an elevation shows
- Front and rear views of each rack with every device at its U position and height.
- Device name, model, asset tag/serial, owner, PSU count and which PDU (A/B) each feeds.
- Patch panels and cable managers, blanking panels, shelves.
- Rack metadata: site, room, row/position, rack height, power capacity (kW), weight limit.
- Airflow direction per device for cooling audits.

## Tools
- **NetBox**: racks with a height in U (commonly 42U to 48U), an ascending or descending unit order, and mounting depth fields; check NetBox's rack and device documentation for elevation views and reservations.
- Visio/draw.io stencils for one-off documents; generate from NetBox/DCIM to avoid drift.
- Commercial DCIM products for large sites with live power/environment data.

## Practices
- Be explicit about U numbering (NetBox can count rack units ascending from the ground up, or descending); record full vs half depth so rear-mounted gear does not
  collide.
- Reserve space for planned growth and mark it.
- Include elevation snapshots in change tickets for installs/removals.
- Audit: walk the room annually (or with each major change) comparing the elevation to reality;
  photos of front and rear are cheap evidence.

## Verify
- [ ] Physical audit of a rack matches the elevation for every device and position; power capacity used vs rated is shown.

## Checked

- Date: 2026-10-28
- Confirmed: NetBox rack documentation: racks commonly 42U to 48U, ascending or descending unit order toggle, U height, starting unit, descending units and mounting depth fields.
- Removed: elevation API URL, device-type attribute list, DCIM vendor names, TIA/EIA-310 numbering claim.
Method: documentation only; no commands were run.
