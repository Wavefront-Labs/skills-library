---
id: architecture-construction.urban-regional-planning.transport-land-use-integration.transit-oriented-development-and-parking-policy
name: transit-oriented-development-and-parking-policy
category: architecture-construction
field: urban-regional-planning
product: transport-land-use-integration
tags: [transport-land-use-integration, transit-oriented-development, tod, station-precinct, walk-catchment, pedestrian-shed, 400m, 800m, network-catchment, accessibility-analysis, isochrones, corridor-planning, parking-policy, parking-maximums, parking-minimums, unbundled-parking, shared-parking, mixed-use, density-near-transit, first-last-mile, active-transport, urban-planning, transport-planning]
level: advanced
status: draft
description: "Plan land use and transport together: define real walk catchments around stations, set density and mix there, reform parking requirements, and measure accessibility to jobs and services."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transport and land-use integration — TOD, catchments and parking

**Goal:** put people and activities where good transport already is (or will be), and
stop land-use rules undermining the transport system.

## 1. Catchments that reflect reality
- Common planning rules of thumb: ~400 m (about 5 minutes' walk) for bus stops, ~800 m
  (about 10 minutes) for rail/rapid-transit stations. Many studies find people walk
  further to high-frequency rail — use local survey evidence where you have it.
- Use **network** distance along walkable paths, not circles. In a cul-de-sac suburb an
  800 m circle may contain only half the land actually within 800 m walk.
- Build network catchments with GIS network analysis (ArcGIS Network Analyst service
  areas, QGIS with a routing plugin or OSM-based tools). Map the **ped-shed ratio**
  (network area ÷ circle area) to show where connectivity is poor.
- Fixing links (a footbridge, a mid-block path, a station entrance on the other side)
  can enlarge a catchment more cheaply than rezoning.

## 2. Transit-oriented development (TOD) controls
Within the catchment:
- **Density gradient:** highest intensity closest to the station, tapering out.
- **Mix:** homes, jobs, shops and services so trips can be chained and the line carries
  people both ways and all day.
- **Active ground floors** on routes to the station; direct, safe, shaded walking routes.
- **Design for access, not storage:** station car parks occupy the most valuable land;
  consider staged replacement with development, keeping drop-off, bike and bus interchange.
- Protect against displacement: TOD raises land value; pair it with affordable housing
  tools where policy allows.

## 3. Parking policy
Parking rules are among the strongest land-use levers on travel:
- **Minimum parking requirements** raise housing costs (structured parking can cost
  tens of thousands per space) and make small infill sites infeasible. Many cities have
  reduced or removed minimums near transit.
- **Maximums** cap supply in well-served areas.
- **Unbundling** (selling/renting spaces separately from homes) lets non-drivers save.
- **Shared parking** between uses with different peaks (offices by day, residential
  by night) cuts total spaces.
- On-street: priced and managed parking with permit schemes prevents overspill when
  off-street minimums are cut.
- Require bicycle parking and car-share spaces as part of the package.

## 4. Corridor planning
Along a bus rapid transit or tram corridor: identify nodes at stops for intensification,
fix the street cross-section (transit lanes, footpaths, cycle lanes, trees) before
redevelopment so setbacks can deliver it, and coordinate rezoning with service
investment timing.

## 5. Measuring accessibility
- **Cumulative opportunities:** number of jobs reachable within 30/45 minutes by
  transit, walking, cycling, car (use GTFS timetables with tools such as r5/OpenTripPlanner-based
  analysis, or commercial equivalents).
- Compare scenarios: does a rezoning or a service change increase the jobs reachable
  for most people? This turns "integration" into a measurable objective.

## Gotchas
- Frequency matters more than the line on the map; low-frequency stops don't support TOD.
- Circular buffers overstate catchments and can mislead rezoning decisions.
- Cutting parking minimums without managing on-street parking causes neighbour backlash.

## Verify
- [ ] Catchments mapped on the walking network, not as circles.
- [ ] Density and mix controls graded around the station.
- [ ] Parking policy reviewed (minimums, maximums, unbundling, on-street management).
- [ ] Accessibility metric computed for options and reported.

*Uncertainty:* catchment distances and parking costs are commonly cited ranges;
validate locally.
