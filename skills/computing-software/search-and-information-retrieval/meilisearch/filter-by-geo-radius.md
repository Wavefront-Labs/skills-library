---
id: computing-software.search-and-information-retrieval.meilisearch.filter-by-geo-radius
name: filter-by-geo-radius
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [geo-radius, geo-filter, geo-distance, meilisearch]
level: practitioner
status: docs-checked
description: "Filter Meilisearch documents within a circle using _geoRadius(lat, lng, distanceInMeters), read _geoDistance and combine with other filters."
sources: ["https://www.meilisearch.com/docs/capabilities/geo_search/how_to/filter_by_geo_radius"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filter by geo radius

`_geoRadius(lat, lng, distanceInMeters)` in the `filter` parameter returns documents whose `_geo` location lies inside a circle. Parameters: latitude (float), longitude (float) and radius as an integer in meters, so 2000 is 2 km. Typical radii from the docs: 1000 walking, 5000 short drive, 15000 city-wide, 50000 regional.

Example: restaurants within 2 km of central Milan, `_geoRadius(45.472735, 9.184019, 2000)`.

## _geoDistance

Results include a computed `_geoDistance` field, the distance in meters from the circle centre to the document. It exists only in results; it is not stored and cannot be used in a filter.

## Combining

Join with AND/OR: `_geoRadius(45.472735, 9.184019, 2000) AND type = pizza` returns only pizzerias in range. Documents carry a `_geo` object with `lat` and `lng`.

## Checked

Method: docs-checked 2026-11-09 against the Filter by geo radius page (raw mdx of github.com/meilisearch/documentation, read in full). Dropped the unconfirmed filterable-attribute claim.