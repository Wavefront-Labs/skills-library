---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.shapefile-isoxml-and-geotiff-handling
name: shapefile-isoxml-and-geotiff-handling
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, isoxml-files, shapefile, geotiff, taskdata-xml, file-conversion, coordinate-reference-system, gdal, ogr2ogr, farm-data-management]
level: practitioner
status: gated
description: "Handle farm geodata files: shapefile limits, ISOXML task data, GeoTIFF rasters, coordinate reference systems, conversion with GDAL and common failures."
sources:
  - "ESRI Shapefile Technical Description (https://www.esri.com/content/dam/esrisites/sitecore-archive/Files/Pdfs/library/whitepapers/pdfs/shapefile.pdf)"
  - "GDAL ESRI Shapefile driver (https://gdal.org/en/stable/drivers/vector/shapefile.html)"
  - "ISO standards catalogue (https://www.iso.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shapefile, ISOXML and GeoTIFF handling

**Goal:** move field boundaries, prescriptions and as-applied data between systems without loss.

## Formats
- Shapefile: a set of files (.shp, .shx, .dbf and a .prj with the coordinate system); keep all together. Limits: 10-character field names, about 2 GB per file (a compatibility limit; GDAL notes files may exceed it), one shape type per file (ESRI shapefile white paper). Most monitors and software import and export it, often with specific attribute names for rate; check the monitor's guide.
- ISOXML (ISO 11783-10): the task data exchange format of ISOBUS, delivered as a folder with TASKDATA.XML plus binary or grid files (structure from ISO 11783-10 (gated: unconfirmed, source is paywalled or blocked)), used for fields, boundaries, guidance lines, prescription grids and logged data. Versions and optional elements differ between terminals, so test one field export-import before a full season.
- GeoTIFF: a georeferenced raster for imagery, yield rasters and elevation; check the CRS, cell size and nodata value; compress large rasters.
- GeoJSON and GeoPackage are modern alternatives for exchange between software.

## Coordinate reference systems
Machines usually work in WGS 84 latitude and longitude (EPSG:4326); area and distance calculations need a projected system (UTM or an equal-area projection). Use a consistent CRS and record it; reproject, do not just relabel.

## Tools
GDAL and OGR (ogr2ogr, gdal_translate, gdalwarp) and QGIS, which can read and write shapefile, GeoTIFF and GeoPackage; for ISOXML conversion use farm management software or specialised converters. Typical command: ogr2ogr -t_srs EPSG:4326 output.shp input.gpkg to reproject a vector file.

## Failure modes
Missing .prj; wrong attribute name for rate; mixed units (kg versus lb per ha or ac); shapefile attributes truncated to 10 characters; ISOXML version mismatch; polygons with holes or self-intersections; the monitor ignoring the file because the field name or ID does not match.

## Verify
- [ ] Open the exported file in a second program and compare areas and extents.
- [ ] Test a prescription on the monitor with the machine stationary before field use.
- Unconfirmed: monitor-specific attribute names; use the manufacturer's guide.
