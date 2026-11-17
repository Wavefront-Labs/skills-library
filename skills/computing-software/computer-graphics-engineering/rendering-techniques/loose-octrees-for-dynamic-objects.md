---
id: computing-software.computer-graphics-engineering.rendering-techniques.loose-octrees-for-dynamic-objects
name: loose-octrees-for-dynamic-objects
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, spatial-structures, loose-octree, octree, spatial-partitioning, dynamic-objects, culling]
level: practitioner
status: docs-checked
description: "Use loose octrees for dynamic object culling and queries: 2x overlapping node bounds, level chosen from object radius, node from centre, cheap moves."
sources: ["https://anteru.net/blog/2008/loose-octrees/", "http://www.tulrich.com/geekstuff/partitioning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loose octrees for dynamic objects

Sources: Thatcher Ulrich, "Spatial partitioning with Loose Octrees" (usenet postings on his site)
and the "Loose Octrees" article on the Anteru blog, which builds on it.

## 1. Problem with regular octrees
An object slightly larger than a cell would either end up in the parent cell or be put into the
cells it overlaps. Ulrich's variant of the problem: in a plain quadtree, tiny objects that
straddle a split plane end up in huge squares (hotspots) high in the tree.

## 2. Loose octree
- Each node, which in a normal octree would be an N x N x N cube, is instead bounded by a
  2N x 2N x 2N cube overlapping the neighbouring nodes. It is still hierarchical: all
  sub-nodes are completely contained in their parent, so rejecting a node rejects its sub-hierarchy.
- Placement: an object's bounding radius completely determines its level, and its centre
  determines the particular node. Objects are sorted in by bounding box centre, so one object
  always ends up in a single cell.
- The loose bound is exactly twice the cell, so an object no larger than the cell whose centre is
  inside the cell is guaranteed to lie inside the loose bounds. Sorting in then only needs a
  size check and a centre check, not an overlap test.
- In Ulrich's implementation the maximum object radius is half the size of a grid square. An
  object too big for the square goes to the next higher level; if its radius is below a quarter
  of the square size, recurse to the sub-square containing its centre. Moving an object or
  changing its radius needs a check whether it must move to a new square; he found the overhead
  small. Moving needs no allocation or deallocation with pre-allocated nodes.

## 3. Queries
The difficulty is querying: test against the relaxed (loose) bounds. A query point can lie
inside the relaxed bounds of two neighbouring cells, so both must be checked. More squares are
checked than in a typical quadtree, the main drawback; the structure is a flexible first level of
coarse culling, with tighter tests on the individual objects afterwards.

## 4. Implementation notes
- Ulrich kept an empty flag per node to avoid recursing into empty cubes, since 3D databases
  contain many empty nodes. Pre-allocating a fixed subdivision needs N^3 nodes at the finest level.
- Anteru: store the tree in an array with an offset per node instead of eight child pointers;
  per node keep the object list, bounds and offset.
- For a perfect-cube octree check object size with the diagonal; for non-cubic trees compute the
  half-sized bounding box and check it fits (easy when axis aligned).
- The scene must be bounded before starting; you can prune top levels as long as a node has
  exactly one child by using that child as the new root.

## 5. When to use
Ulrich: best suited to dynamic databases such as games with an open (outdoor) layout; ordinary
quadtrees, octrees or kd-trees are more efficient for static geometry.

## Gotchas
- The bounds are looser than a tight tree, so expect more node visits per query.

## Verify
- [ ] Query results identical to a brute-force test.
- [ ] Debug draw nodes and loose bounds.

## Checked

Method: docs-checked 2026-11-09 against the Anteru Loose Octrees article and Ulrich's partitioning notes (both read in full). Dropped the O(1) depth log2 formula, k between 1.5 and 2 advice, hash map keyed nodes, intrusive list advice, spatial hash alternatives, the Game Programming Gems attribution and the realtimerendering and gamedev.net sources (not read).
