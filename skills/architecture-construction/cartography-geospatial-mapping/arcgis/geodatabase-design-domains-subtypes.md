---
id: architecture-construction.cartography-geospatial-mapping.arcgis.geodatabase-design-domains-subtypes
name: geodatabase-design-domains-subtypes
category: architecture-construction
field: cartography-geospatial-mapping
product: arcgis
tags: [arcgis, arcgis-pro, esri, geodatabase, file-geodatabase, gdb, enterprise-geodatabase, feature-dataset, feature-class, schema-design, attribute-domains, coded-value-domain, range-domain, subtypes, contingent-values, topology, geodatabase-topology, attribute-rules, relationship-classes, spatial-reference, xy-tolerance, xy-resolution, editor-tracking, global-ids, fields, field-aliases, data-quality, arcpy, xray, schema-documentation]
level: practitioner
status: draft
description: "Design an ArcGIS Pro geodatabase that keeps data clean: spatial reference, fields, coded-value and range domains, subtypes, topology rules, attribute rules and editor tracking."
sources: ["Esri ArcGIS Pro documentation: geodatabases, domains, subtypes, topology, attribute rules", "Esri geodatabase design best practice papers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Geodatabase design with domains, subtypes and topology (ArcGIS Pro)

**Goal:** a geodatabase schema where editors physically cannot enter most bad data —
invalid codes, impossible values, overlapping parcels, dangling roads — so map
production and analysis don't start with a cleaning project.

## 1. Model before you click
Write a schema table first: feature class, geometry type, fields (name, type, length,
alias, nullable, domain), subtypes, relationships, rules. Have the map's users review it.
For repeatable builds, script it with ArcPy or keep an XML workspace document
(*Export XML Workspace Document* — schema only) under version control.

## 2. Spatial reference and tolerance
- Choose a **projected** coordinate system suited to the area (national grid, UTM zone,
  state plane) for measurement-heavy data; store the exact datum/realisation.
- A **feature dataset** forces all its feature classes to share a spatial reference —
  required for topology, networks and parcel fabrics; don't use feature datasets merely
  as folders.
- Keep the default **XY tolerance / resolution** unless you understand the effect;
  tolerance controls when vertices are treated as coincident in topology and overlay.
  Set it consistently across datasets that must line up.

## 3. Fields
- Short, stable field names (no spaces, avoid reserved words); readable **aliases** for users.
- Pick types deliberately: integer codes over free text; dates as Date; avoid storing
  numbers as text.
- Add **Global IDs** if data will sync, replicate or be related robustly; enable
  **editor tracking** (created/edited user and date) for accountability.

## 4. Domains
- **Coded-value domain**: a pick list (`1 = Asphalt`, `2 = Gravel`, `3 = Unsealed`).
  Store the code, show the description. Share one domain across feature classes.
- **Range domain**: numeric limits (`SPEED_LIMIT` 10–130).
- Domains are enforced in the editing UI, but **existing or loaded data is not
  automatically validated** — run *Validate* (Edit › Manage Edits › Validate / in older
  workflows the attribute validation tool) after loads.

## 5. Subtypes
A subtype splits a feature class into categories sharing geometry and fields, each with
its own default values and domains (e.g. `ROADS` subtypes Motorway / Arterial / Local, each
with a different speed-limit range domain). Use subtypes when categories share a schema;
use separate feature classes when they don't. **Contingent values** constrain combinations
of field values (e.g. material only valid for certain pipe classes).

## 6. Topology
Inside a feature dataset, add a geodatabase topology with rules such as:
- Polygons: *Must Not Overlap*, *Must Not Have Gaps* (parcels, zoning).
- Lines: *Must Not Have Dangles*, *Must Not Self-Overlap* (roads, streams).
- Between classes: *Must Be Covered By*, *Must Be Inside*.
Set **ranks** so more accurate data doesn't move during validation. Validate, then fix
or mark legitimate cases as exceptions (e.g. a real dead-end road dangle).

## 7. Attribute rules
Arcade expressions that **calculate** (auto-populate an ID, area, or nearest street name),
**constrain** (reject edits breaking a condition) or **validate** (flag errors in batch).
They run at edit time and travel with the data — *availability and behaviour depend on the
geodatabase type and ArcGIS Pro version; confirm for yours.*

## Gotchas
- Loading data with Append into a domain-constrained class doesn't stop bad codes —
  validate afterwards.
- Renaming fields later breaks layer files, maps, scripts and services.
- Shapefiles can't hold domains, subtypes, long field names or nulls well; avoid them as
  the master format.

## Verify
- [ ] Schema table matches the built geodatabase (field types, domains, aliases).
- [ ] All related feature classes share one spatial reference and tolerance.
- [ ] Domain validation run after every bulk load; error count zero or explained.
- [ ] Topology validated; remaining errors are documented exceptions.
- [ ] Editor tracking and Global IDs enabled where needed.
