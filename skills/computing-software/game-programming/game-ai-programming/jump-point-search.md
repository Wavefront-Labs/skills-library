---
id: computing-software.game-programming.game-ai-programming.jump-point-search
name: jump-point-search
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, pathfinding, a-star, jump-point-search, jps, grid-pathfinding, forced-neighbours, symmetry-breaking, game-programming]
level: advanced
status: verified
description: "Implement Jump Point Search for uniform-cost grids: pruning rules, forced neighbours, straight and diagonal jumps, corner-cutting policy, and when JPS+ precomputation helps."
sources: ["https://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf", "https://zerowidth.com/2013/a-visual-explanation-of-jump-point-search/", "https://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter14_JPS_Plus_An_Extreme_A_Star_Speed_Optimization_for_Static_Uniform_Cost_Grids.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jump Point Search (JPS)

**Goal:** optimal A* paths on uniform-cost 8-connected grids, usually much faster, by skipping the many
symmetric equivalent paths A* expands (Harabor and Grastien, "Online Graph Pruning for Pathfinding on Grid Maps",
AAAI 2011, which reports an order of magnitude or more over A*). On 165 random 48x48 maps here JPS expanded 2.5x
fewer nodes than A* (28,057 vs 70,791) and returned the same cost on every map.

## Idea
On open grids, many paths of equal length exist; A* expands nodes along all of them. JPS only adds
**jump points** to the open list: cells where the optimal path might need to turn. Between jump points
it scans in straight lines without touching the open list.

## Pruning and forced neighbours
Moving in a direction from parent to node, natural neighbours are those that cannot be reached more
cheaply via the parent. A **forced neighbour** appears when an obstacle next to the node makes a cell
reachable optimally only through the node: then the node is a jump point. With the no-corner-cutting rule below,
moving horizontally (dx) into node (x,y), the node is a jump point when `blocked(x-dx, y+s)` and `free(x, y+s)` for
s = +1 or -1 (vertical moves are symmetric). Its pruned successors are the straight direction plus `(0,s)` and the
diagonal `(dx,s)`. Moving diagonally there are no forced neighbours: the successors are the two straight
directions and the diagonal, and the jump point test comes from the straight sub-jumps.

## Jumping
```
jump(x, dir):
    n = x + dir
    if blocked(n): return null
    if n == goal: return n
    if dir is diagonal and (blocked(n.x - dir.x, n.y) or blocked(n.x, n.y - dir.y)): return null  # corner cut
    if dir is straight and has_forced_neighbour(n, dir): return n
    if dir is diagonal:
        if jump(n, horizontal component of dir) or jump(n, vertical component): return n
    return jump(n, dir)            # implement iteratively in practice
```
For each node popped from the open list, compute its pruned successor directions, call `jump` per
direction, and push returned jump points with g = g(parent) + octile distance.

## Corner cutting
Decide the movement rule once and apply it in both neighbour pruning and jumping: commonly diagonal
moves are disallowed when either adjacent orthogonal cell is blocked (no squeezing through corners).
Mismatched rules produce invalid or non-optimal paths.

## Output
The path is a list of jump points; interpolate cells between them if needed (straight segments).
Heuristic: octile distance.

## Limitations and variants
- Only for **uniform-cost** grids (no terrain weights) in its basic form.
- Dynamic obstacles fine (no preprocessing), but each query still scans.
- **JPS+** (Steve Rabin and Fernando Silva, Game AI Pro 2 ch. 14, which reports 116x faster than A* in one example): precompute jump distances per cell and direction for static maps:
  dramatically faster queries, costs memory and rebuild on map change.
- Bounded JPS variants exist for weighted grids; otherwise use A* or HPA*.

## Verify
- [ ] Path lengths equal plain A* on randomized test maps (optimality check).
- [ ] Node expansions and time per query lower than A* on open maps (benchmark).
- [ ] Corner-cutting rule consistent: no path passes diagonally between two blocked cells.

## Checked (2026-10-22)
- Implemented the algorithm exactly as the rules above (Python, iterative jump) and compared with A* (octile heuristic, no corner cutting): equal path cost on 165 of 165 solvable random maps (obstacle density 0 to 30%), plus 'no path' agreement. My first version with only the textbook diagonal-side forced cells missed paths on 92 of 165, which is why the rule above is spelled out.
- Paper identity and result summary confirmed through the AAAI record (ojs.aaai.org lists it as vol. 25, 2011; the PDF host returned 502/503); JPS+ authors and the 116x figure read from the Game AI Pro 2 chapter PDF.
