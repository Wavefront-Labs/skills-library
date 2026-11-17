---
id: social-sciences.sociology.social-network-analysis.name-generators-centrality-and-community-detection
name: name-generators-centrality-and-community-detection
category: social-sciences
field: sociology
product: social-network-analysis
tags: [social-network-analysis, sna, sociology, network-science, name-generator, name-interpreter, ego-network, egocentric, whole-network, sociocentric, roster, boundary-specification, centrality, degree-centrality, betweenness, closeness, eigenvector-centrality, density, homophily, structural-holes, weak-ties, community-detection, modularity, louvain, leiden, igraph, networkx, statnet, ergm, siena, gephi, network-visualisation]
level: practitioner
status: verified
description: "Collect ego or whole-network data with name generators, compute centrality and communities in igraph/networkx, and avoid the missing-data and boundary traps."
sources:
  - https://networkx.org/documentation/stable/reference/algorithms/community.html
  - https://cran.r-project.org/web/packages/igraph/index.html
  - https://doi.org/10.1177/000312240607100301
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Name generators, centrality and community detection

**Goal:** measure who is connected to whom in a way that matches your question, then
describe position and structure without over-reading pretty pictures.

## 1. Ego-network or whole-network?
- **Egocentric:** each respondent (ego) names contacts (alters) and describes them.
  Works with random samples and large populations; gives personal network size,
  composition, homophily. You can't usually link alters across egos.
- **Whole (sociocentric):** every member of a bounded group (a school, firm, village)
  reports ties to every other, often from a roster. Gives full structure (paths,
  centrality, communities) but requires a defensible **boundary** and high response.

## 2. Name generators
- Classic: GSS "important matters" ("Looking back over the last six months, who are the
  people with whom you discussed matters important to you?"). Results are sensitive to
  wording and interviewer behaviour — McPherson, Smith-Lovin & Brashears (ASR 2006) reported a drop in GSS core-network size between 1985 and 2004, and Paik & Sanchagrin ("Social isolation in America: an artifact", 2012/13) attribute much of it to interviewer and measurement effects.
- Use **multiple generators** (discuss, help, socialise, advice) — different ties
  matter for different outcomes.
- Cap or not? Fixed caps (e.g. "up to five") truncate degree. If you cap, analyse
  with that in mind.
- **Name interpreters** then ask about each alter: relationship, frequency, closeness,
  demographics, and alter–alter ties ("Do A and B know each other?") for ego-network density.
- Roster-based recall in whole networks beats free recall for completeness.

## 3. Data structure
Edge list (`from, to, weight, type`) plus a node attribute table. Decide directed vs
undirected (advice is directed; "know each other" usually undirected) and whether to
symmetrise unreciprocated nominations — document the rule.

## 4. Core measures
```python
import networkx as nx
G = nx.from_pandas_edgelist(edges, "from", "to", create_using=nx.DiGraph)
deg = dict(G.in_degree()); btw = nx.betweenness_centrality(G)
eig = nx.eigenvector_centrality(G.to_undirected(), max_iter=1000)
comms = nx.community.louvain_communities(G.to_undirected(), seed=1)
```
R: `igraph::degree`, `betweenness`, `cluster_louvain`, `cluster_leiden` (all in the igraph CRAN manual). The Python block ran with NetworkX 3.7 on a toy 6-node directed graph: `in_degree` gave `a:2, c:2`, `louvain_communities(seed=1)` returned the two triangles, and 20 seeds gave one identical partition on that toy graph (real networks vary run to run). `nx.constraint` (Burt), `density`, `reciprocity` and `transitivity` also ran.
| Measure | Captures |
|---|---|
| Degree (in/out) | Popularity / activity |
| Betweenness | Brokerage between parts of the network |
| Closeness | Reach (ill-defined on disconnected graphs) |
| Eigenvector / PageRank | Being tied to well-connected others |
| Constraint (Burt) | Structural holes around ego |
| Density, reciprocity, transitivity | Overall cohesion |
| Assortativity / E–I index | Homophily |

## 5. Community detection
Louvain/Leiden optimise modularity; results vary run to run — fix a seed and check
stability over many runs. Modularity has a resolution limit (misses small communities);
tune the resolution parameter and validate communities against something substantive.

## 6. Inference
Network observations aren't independent — ordinary regression SEs are wrong for
dyadic data. Use QAP regression, **ERGMs** (`statnet`) for tie formation, or
**stochastic actor-oriented models** (RSiena) for network panels. Distinguishing
influence from selection needs longitudinal data and models like SIENA.

## 7. Visualisation
Gephi or `ggraph`. Layout (force-directed) positions are not measurements; colour by
attribute, size by a named centrality, and say what was filtered out.

## Gotchas
- Missing nodes in whole networks bias centrality severely; aim for 80%+ response and
  report it.
- Ethics: whole-network surveys collect data about non-consenting alters — get ethics
  approval for that explicitly and never display identifiable network maps to participants' organisations.
- The GSS artefact debate is unresolved in detail; treat trend claims cautiously.

## Verify
- [ ] Ego vs whole design matches the question; boundary defined.
- [ ] Generators, caps and symmetrisation rules documented.
- [ ] Centrality chosen for its meaning, not by default.
- [ ] Community results stable across seeds/resolutions.
- [ ] Inference uses network-appropriate models.
