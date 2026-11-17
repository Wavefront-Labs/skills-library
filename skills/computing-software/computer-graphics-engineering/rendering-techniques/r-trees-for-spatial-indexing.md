---
id: computing-software.computer-graphics-engineering.rendering-techniques.r-trees-for-spatial-indexing
name: r-trees-for-spatial-indexing
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, spatial-structures, r-tree, rstar-tree, spatial-index, bulk-loading, range-query, boost-geometry]
level: practitioner
status: docs-checked
description: "Use R-trees for spatial indexing of rectangles and boxes: Guttman insertion, deletion and splits, the R*-tree split and forced reinsert, and Boost.Geometry."
sources: ["http://www-db.deis.unibo.it/courses/SI-LS/papers/Gut84.pdf", "https://www.boost.org/doc/libs/release/libs/geometry/doc/html/geometry/spatial_indexes.html", "https://infolab.usc.edu/csci599/Fall2001/paper/rstar-tree.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# R-trees

Guttman 1984. A height-balanced tree (like a B-tree) of minimum bounding rectangles. Leaf nodes
hold index records pointing at spatial objects; non-leaf nodes hold a child pointer plus the
rectangle that covers the child's entries. Each node holds at most M entries and (except the root)
at least m. Directory rectangles may overlap, so a search may descend several subtrees.

## 1. Guttman operations
- **Search:** at a non-leaf node, recurse into every entry whose rectangle overlaps the search
  rectangle; at a leaf, report matching records.
- **Insert (ChooseLeaf):** from the root, pick the entry whose rectangle needs least enlargement to
  include the new rectangle; ties go to the entry with the smallest area. Descend to a leaf.
  If the leaf is full, split it (M+1 entries divided between two nodes), then AdjustTree walks
  to the root tightening covering rectangles and propagating splits. A root split grows the tree.
- **Split goal:** minimise the total area of the two covering rectangles, since a node is visited
  when its rectangle overlaps the search area.
- **Quadratic split:** PickSeeds takes the pair of entries whose joint rectangle wastes the most
  area (area(J) minus both entry areas); PickNext then assigns remaining entries one at a time,
  choosing the entry with the greatest difference in area increase between the two groups.
  Cost is quadratic in M.
- **Linear split:** same as quadratic but with a cheaper PickSeeds, and PickNext takes any
  remaining entry. Cost is linear in M.
- **Delete:** FindLeaf, remove the record, then CondenseTree: nodes left with fewer than m entries
  are removed and their entries re-inserted (leaf entries at leaf level, higher-level entries
  higher in the tree). If the root ends with one child, that child becomes the root. Guttman chose
  re-insertion over merging siblings because it reuses Insert and keeps refining the structure.
- **Update** of an object's rectangle: delete, change, re-insert.

## 2. R*-tree (Beckmann et al. 1990)
- **Split:** for each axis, sort entries by lower then upper rectangle value, enumerate the
  M-2m+2 distributions per sort, and sum the margin values; the axis with the smallest margin sum
  is the split axis. On that axis choose the distribution with the smallest overlap between the
  two groups' bounding boxes.
- **Forced reinsert:** on the first overflow at a level during one insertion, instead of
  splitting, remove the p entries whose centres are furthest from the node's bounding-rectangle
  centre and re-insert them. The paper found p = 30 percent of M best, and "close reinsert"
  (nearest of the removed entries first) better than far reinsert. This reduces overlap and
  improves storage utilisation; insertion disc accesses rose only about 4 percent in the paper.

## 3. Boost.Geometry rtree
The Boost docs list three balancing algorithms (`linear`, `quadratic`, `rstar`), creation using
a packing algorithm (bulk loading, which the docs say is faster and gives better query
performance), compile-time or run-time node parameters, and queries such as k nearest values to a
point. Faster inserts generally mean slower searches and the reverse.
```cpp
#include <boost/geometry/index/rtree.hpp>
namespace bgi = boost::geometry::index;
using Value = std::pair<Box, int>;                  // Box is a boost::geometry::model::box
bgi::rtree<Value, bgi::rstar<16>> tree(values.begin(), values.end());  // range constructor
std::vector<Value> hits;
tree.query(bgi::intersects(queryBox), std::back_inserter(hits));
tree.query(bgi::nearest(pt, 5), std::back_inserter(hits));
```
The docs' own examples use `rstar<8>`, `quadratic<16>` and `linear<32>`; the number is the
maximum elements per node.

## Gotchas
- Heavy overlap between rectangles degrades searches (more subtrees visited); the R* split and
  forced reinsert exist to reduce it.
- Under-full nodes after deletion are handled by re-inserting orphaned entries, not merging.

## Verify
- [ ] Query results match brute force on random data.
- [ ] Tree built from a range queries at least as fast as one built by repeated insert on the same data.

## Checked
2026-11-09. Read: Guttman 1984 (search, ChooseLeaf, AdjustTree, delete and CondenseTree,
quadratic and linear split, PickSeeds, PickNext; the text came from OCR), Beckmann et al. 1990
(split axis and index, forced reinsert, p = 30 percent, close vs far reinsert, 4 percent insert
cost), and the Boost.Geometry spatial index introduction, creation and queries pages
(algorithms, packing, nearest and intersects predicates, example parameters). Removed: STR
algorithm details, MINDIST best-first search, GIS products, other-language libraries, and the
R-tree vs BVH comparison (not in the sources); the claim that the range constructor uses
packing is not stated, so the code only says range constructor.
Method: docs-checked 2026-11-09 against Guttman 1984, the R*-tree paper and the Boost.Geometry spatial index pages.
