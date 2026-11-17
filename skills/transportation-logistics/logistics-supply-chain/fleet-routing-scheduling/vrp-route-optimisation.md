---
id: transportation-logistics.logistics-supply-chain.fleet-routing-scheduling.vrp-route-optimisation
name: vrp-route-optimisation
category: transportation-logistics
field: logistics-supply-chain
product: fleet-routing-scheduling
tags: [fleet-routing-scheduling, logistics-supply-chain, route-optimisation, route-optimization, vrp, vrptw, cvrp, vehicle-routing-problem, time-windows, or-tools, google-or-tools, vroom, osrm, distance-matrix, stop-sequencing, driver-assignment, dynamic-re-routing, last-mile, delivery-routes, hours-of-service, service-time, python]
level: practitioner
status: docs-checked
description: "Plan daily fleet routes as a VRP with time windows: road matrix, capacities and service times, solve with OR-Tools, sanity-check plans."
sources: ["https://developers.google.com/optimization/routing/vrptw", "https://developers.google.com/optimization/routing/cvrp", "https://developers.google.com/optimization/routing/penalties", "https://developers.google.com/optimization/routing/vrp", "http://project-osrm.org/docs/v5.24.0/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VRP route optimisation — daily routes that drivers can actually run

**Goal:** assign stops to vehicles and sequence them so every stop is served in its
time window, no vehicle is overloaded, shifts and driving-time rules hold, and total
cost (distance + time + vehicles) is low. Works whether you use a commercial router or
code it yourself; this shows the open-source path.

## 1. Inputs that decide plan quality
- **Stops:** geocoded location (check rooftop vs postcode-centroid accuracy), demand
  (kg, m³, pallets, totes), time window, **service time** (fixed + per unit).
- **Vehicles:** capacity per dimension, start/end depot, shift start/end, cost per km
  and per hour, fixed cost per vehicle used, skills (tail-lift, chilled, ADR).
- **Travel times:** a real road matrix by time of day, not straight-line distance.
  Self-host OSRM (`osrm-routed`, `/table/v1/driving/` endpoint) or use a paid matrix API.
Bad service times are the most common reason "optimised" routes run late.

## 2. Model and solve (OR-Tools, Python)
```python
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
mgr = pywrapcp.RoutingIndexManager(len(T), n_vehicles, depot)
r = pywrapcp.RoutingModel(mgr)
def t_cb(i, j):  # travel seconds + service time at origin node
    a, b = mgr.IndexToNode(i), mgr.IndexToNode(j)
    return T[a][b] + service[a]
cb = r.RegisterTransitCallback(t_cb)
r.SetArcCostEvaluatorOfAllVehicles(cb)
r.AddDimension(cb, 3600, 10*3600, False, "Time")   # slack (wait), horizon, don't force start 0
time = r.GetDimensionOrDie("Time")
for node, (open_, close) in enumerate(windows):
    time.CumulVar(mgr.NodeToIndex(node)).SetRange(open_, close)
d_cb = r.RegisterUnaryTransitCallback(lambda i: demand[mgr.IndexToNode(i)])
r.AddDimensionWithVehicleCapacity(d_cb, 0, capacities, True, "Load")
for node in range(1, len(T)):                       # allow dropping at a penalty
    r.AddDisjunction([mgr.NodeToIndex(node)], 1_000_000)
p = pywrapcp.DefaultRoutingSearchParameters()
p.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
p.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
p.time_limit.FromSeconds(60)
sol = r.SolveWithParameters(p)
```
Key choices: the disjunction penalty lets the solver report **unserved** stops instead
of returning no solution (the OR-Tools "dropped visits" pattern);
`time.SetGlobalSpanCostCoefficient` with a large value makes the solver minimise the longest
route. VROOM (with OSRM) is a
faster drop-in for standard VRPTW if you don't need custom constraints.

## 3. Driver rules
Add breaks and maximum driving time from the rules that apply to your drivers (for example
EU drivers' hours rules or US FMCSA hours-of-service rules; look up the current figures,
they are not restated here). Encode them as constraints on the time dimension or cap route
duration conservatively.

## 4. Sanity-check before release
- Look at the map: crossing routes, zig-zags, a truck visiting one far stop.
- Compare planned vs actual from last week: service-time and speed bias by area.
- Check utilisation: very low on many vehicles → windows or capacity too tight.
- Lock stops that dispatch must keep (customer-requested driver, first-drop promises).

## 5. Dynamic re-routing during the day
Re-solve with current vehicle positions as start nodes, completed stops removed, and
in-progress stops fixed. Only push changes that save meaningful time — constant
resequencing confuses drivers and customers with ETA promises.

## Gotchas
- Asymmetric matrices are normal (one-way streets); don't symmetrise.
- Time windows at the depot: vehicles must also return before shift end.
- Integer units only in OR-Tools callbacks — scale kg/seconds accordingly.
- Solve time grows exponentially with problem size and OR-Tools may return a good but not
  optimal solution; large problems may need clustering or different search options.

## Verify
- [ ] Zero unserved stops, or each unserved one explained (window/capacity infeasible).
- [ ] No route exceeds capacity, shift or legal driving time.
- [ ] Planned vs actual stop arrival error tracked.
- [ ] Dispatchers can read and override the plan.

*Uncertainty:* code is a sketch of the OR-Tools API (consistent with its routing docs) — test against your installed version.

## Checked

Date: 2026-11-09.

Confirmed on the OR-Tools routing guides (VRPTW, CVRP, penalties and dropping visits, VRP) and the OSRM v5.24.0 API page: the OR-Tools calls used (RegisterTransitCallback, SetArcCostEvaluatorOfAllVehicles, AddDimension with a slack and a "do not force start cumul to zero" flag, GetDimensionOrDie, CumulVar().SetRange, RegisterUnaryTransitCallback, AddDimensionWithVehicleCapacity, AddDisjunction with a penalty, PATH_CHEAPEST_ARC, GUIDED_LOCAL_SEARCH, SolveWithParameters, SetGlobalSpanCostCoefficient), the `/table/v1/driving/` endpoint and osrm-routed. Corrected: the time limit is set with `time_limit.FromSeconds()`. Removed because not stated on those pages: SetFixedCostOfAllVehicles, SetBreakIntervalsOfVehicle, the EU and FMCSA hours-of-service figures, the 60-second and 10-minute rules of thumb. VROOM was not checked.

Method: documentation only; no commands were run.
