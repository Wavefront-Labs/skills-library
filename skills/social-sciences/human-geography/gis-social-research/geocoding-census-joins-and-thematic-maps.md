---
id: social-sciences.human-geography.gis-social-research.geocoding-census-joins-and-thematic-maps
name: geocoding-census-joins-and-thematic-maps
category: social-sciences
field: human-geography
product: gis-social-research
tags: [gis-social-research, gis, qgis, arcgis, arcgis-pro, geocoding, address-matching, mmqgis, nominatim, census-geography, tiger-line, acs, american-community-survey, geoid, output-areas, lsoa, statistical-areas, table-join, spatial-join, join-attributes-by-location, count-points-in-polygon, crs, projection, epsg, reproject, choropleth, thematic-mapping, normalisation, rates, geopackage, shapefile, privacy, geomasking]
level: practitioner
status: docs-checked
description: "QGIS/ArcGIS Pro workflow for social data: geocode addresses, join census tables by GEOID, spatial-join points to areas, normalise and map rates."
sources:
  - "https://operations.osmfoundation.org/policies/nominatim/"
  - "https://geocoding.geo.census.gov/geocoder/"
  - "https://www.census.gov/programs-surveys/geography/about/glossary.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geocoding, census joins and thematic maps

**Goal:** turn a spreadsheet of addresses (clinics, evictions, survey respondents)
plus census tables into area-level rates you can map and analyse.

## 1. Get boundaries and tables that match
- US: TIGER/Line shapefiles (tracts, block groups, counties) + ACS tables from
  data.census.gov. UK: ONS Open Geography boundaries (OAs, LSOAs/MSOAs) + Census
  tables via Nomis. Other countries: national statistics office.
- **Same vintage:** census tracts can be updated before each decennial census (Census Bureau
  glossary), so match the boundary vintage to the table vintage.
- Prefer an open single-file format such as GeoPackage over shapefile.

## 2. Geocode addresses
- OpenStreetMap's public Nominatim server allows an absolute maximum of 1 request per second
  and does not encourage bulk geocoding of larger amounts of data (OSMF usage policy);
  use another provider or a self-hosted instance for bulk jobs. US addresses: the Census
  Bureau geocoder offers batch address processing.
- ArcGIS Pro: use a geocoding tool with a locator; check Esri's pricing page for credit costs.
- Clean first: split street/city/postcode columns, standardise abbreviations.
- Check the **match rate and match quality** (rooftop vs street interpolation vs
  postcode centroid). Unmatched addresses are rarely random — often rural, informal
  or new housing. Report the rate; set your own acceptable threshold.
- **Privacy:** geocoded individual data is identifying. Keep it on secure storage and
  publish only aggregated or geomasked results.

## 3. Coordinate reference systems
Reproject everything to a projected CRS suited to
your region (e.g. a state plane or UTM zone, or your national grid)
before measuring distances or areas.
Gotcha: on-the-fly reprojection makes layers *look* aligned while analyses use the
native CRS.

## 4. Join census tables (attribute join)
- Key field is the area code (US **GEOID**, UK OA/LSOA code).
- **Leading-zero trap:** Excel turns GEOID `06037...` into a number and drops the 0.
  Import codes as text; in QGIS use a CSV with a `.csvt` file or set field types
  in the import dialog.
- Use your GIS package's attribute join, then export to make it permanent.
- Check how many rows failed to join.

## 5. Spatial join points to areas
- Use the point-in-polygon count or spatial-join tools of your GIS package.

## 6. Normalise, then map
Never map raw counts on areas of different populations — compute **rates** (events per
1,000 residents) or percentages. Small populations produce unstable rates; suppress or
flag areas below a threshold, or use smoothing. ACS estimates carry margins of error:
check reliability before ranking tracts. For map design see
social-sciences.human-geography.cartographic-communication.honest-choropleth-design.

## Verify
- [ ] Boundary and table vintages match.
- [ ] Geocoding match rate and match types reported; individual data kept secure.
- [ ] All layers in one projected CRS before distance/area work.
- [ ] Join key imported as text; unmatched rows counted.
- [ ] Mapped variable is a rate/percentage with small-population handling.

## Checked

Date: 2026-11-01. Jurisdictions: OpenStreetMap public service; United States (Census Bureau).

Confirmed: Nominatim public server 1 request per second maximum and bulk geocoding not encouraged (OSMF policy); Census geocoder lists batch address processing; census tracts can be updated before each decennial census (Census glossary). Removed as unconfirmed: EPSG codes, shapefile field-name limit, 90% match rule, menu paths, ArcGIS credit claim, tool-specific names, GEOID definition detail.

Method: documentation only; no commands were run.
