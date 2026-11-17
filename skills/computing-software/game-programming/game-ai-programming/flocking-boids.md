---
id: computing-software.game-programming.game-ai-programming.flocking-boids
name: flocking-boids
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, steering-behaviours, flocking, boids, separation, alignment, cohesion, spatial-hash, crowd, game-programming]
level: practitioner
status: verified
description: "Simulate flocks with Reynolds boids: separation, alignment and cohesion weights, neighbour radius and field of view, spatial hashing for performance, and GPU/job scaling."
sources: ["https://www.red3d.com/cwr/boids/", "https://www.red3d.com/cwr/steer/gdc99/", "https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flocking (boids)

**Goal:** birds, fish, bats or swarming enemies moving as a group with emergent, organic motion
(Reynolds, "Flocks, Herds, and Schools", SIGGRAPH 1987).

## Three rules (per boid, over neighbours within radius and field of view)
```
separation = sum over close neighbours of normalize(pos - n.pos) / dist     # avoid crowding
alignment  = average(n.velocity) - velocity                                 # match heading
cohesion   = seek(average(n.pos))                                           # stay with the group
steer = ws*separation + wa*alignment + wc*cohesion + wt*seek(goal) + wo*avoidObstacles
steer = truncate(steer, maxForce); velocity = truncate(velocity + steer*dt, maxSpeed)
```
Starting weights (a tuning start, not a standard): separation 1.5, alignment 1.0, cohesion 1.0; separation radius smaller than the
alignment/cohesion radius. Field of view (e.g. 270 degrees) ignoring boids directly behind looks more
natural.

## Performance
Naive neighbour search is O(n^2). Use a **uniform grid / spatial hash** with cell size = neighbour
radius: each boid checks only its cell and the 8 (2D) / 26 (3D) neighbours. Limit the number of neighbours considered
for stability and cost. Thousands of boids: multithreading or GPU compute with a
sorted spatial hash; double-buffer positions so all boids read last frame's state.

## Making it game-ready
- Goal seeking and obstacle avoidance (raycasts or signed distance fields) on top of the three rules.
- Leaders: some boids follow paths, others follow them via cohesion.
- Predators: flee behaviour weighted strongly within a radius gives dramatic scattering.
- Vertical constraint for fish/birds: limit pitch, keep within height bands.
- Animation: drive flap speed/turn banking from velocity and turn rate.

## Tuning
Expose weights and radii live; too much cohesion = clumping blobs, too much separation = gas-like
dispersion, too much alignment = rigid marching. Check behaviour at different flock sizes.

## Verify
- [ ] Flock stays cohesive without boids overlapping (min distance metric).
- [ ] Neighbour search cost scales roughly linearly with boid count (profiling).
- [ ] Deterministic results with fixed timestep and stable neighbour ordering (if needed for networking/replays).

## Checked (2026-10-22)
- Spatial hash with cell size = neighbour radius returned the same neighbour set as brute force for all 500 points in a random test.
- Ran a 100-boid numpy simulation (300 steps, weights 1.5/1/1, separation radius 2, neighbour radius 8, 270 degree view): minimum pair distance 0.55 versus 0.00 with separation off; cohesion x5 gave 0.24 and a tighter flock (mean distance from centroid 7.6 versus 8.3). Weights are a starting point only.
- Reynolds 1987 SIGGRAPH paper and the red3d boids page confirmed to exist (search results, HTTP 200). Removed an unchecked Unity Jobs/Burst claim and the 'nearest 7' figure.
