---
id: media-communication.library-and-archive-science.information-architecture.card-sorting-and-tree-testing
name: card-sorting-and-tree-testing
category: media-communication
field: library-and-archive-science
product: information-architecture
tags: [information-architecture, ia, card-sorting, open-card-sort, closed-card-sort, hybrid-card-sort, tree-testing, reverse-card-sort, navigation-design, labelling, findability, intranet, site-structure, content-inventory, content-audit, optimal-workshop, treejack, similarity-matrix, dendrogram, success-rate, directness, search-tuning, site-search, ux-research]
level: practitioner
status: docs-checked
description: "Structure a site or intranet for findability: open/closed/hybrid card sorts, reading similarity matrices and dendrograms, and tree-testing tasks and metrics."
sources: ["https://www.nngroup.com/articles/card-sorting-definition/", "https://www.nngroup.com/articles/tree-testing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Card sorting and tree testing for information architecture

**Goal:** a navigation structure and labels that match how users think, validated with
evidence before anything is built.

## 1. Start with an inventory
Export every page or document (URL, title, type, owner, last updated, traffic) and mark
each keep / merge / rewrite / delete before restructuring. Pull top tasks from
analytics, search logs and user interviews so the structure serves those first.

## 2. Card sorting (generate structure)
Card sorting asks participants to place individually labelled cards into groups that make
sense to them. It is a generative method: it captures mental models, groupings and
vocabulary, but is not a good way to evaluate a navigation hierarchy.
- **Open sort:** participants group cards and then name the groups. Ask for labels after
  grouping, not before, so participants do not limit themselves to set categories.
- **Closed sort:** participants place cards into predefined categories.
- **Hybrid:** predefined categories, with participants free to add their own.
Practicalities (Nielsen Norman Group guidance):
- **30-50 cards**; over 50, participants tire and may dump cards into a large
  Miscellaneous group, and you cannot tell whether a card was hard to place or they gave up.
- Avoid identical words in the labels of different cards: participants group by the
  shared word (for example every "Toyota ..." card together) instead of by meaning.
- Pilot with a few participants to check card count and label clarity.
- **Qualitative** (think aloud, to learn why): at least 15 participants.
  **Quantitative** (how often cards are grouped together): at least 30-50.
  Run a few moderated sessions even for an unmoderated quantitative study.
- Remote participants use a web tool such as OptimalSort; in person, use index cards.
  Without a tool you must count card groupings by hand.

## 3. Reading results
- **Similarity matrix:** shows how often pairs of cards were grouped together.
- **Dendrogram** and a standardisation grid are other views of the same data (OptimalSort
  provides all three); each interprets the data differently.
- Category names participants invent will not necessarily be your final labels: card
  sorting ignores other context cues on your site. A participant-made catch-all category
  ("other stuff") should not become a menu item; visitors avoid vague labels.
- Card sorting often gives ideas rather than one correct structure, so test the resulting
  hierarchy with a tree test.

## 4. Tree testing (validate structure)
Tree testing is task-based: participants look for specific resources in a text-only
category tree. It is used solely to evaluate a navigation hierarchy.
- **The tree:** list every category and subcategory of the global navigation (and
  possibly utility navigation), down to the lowest level that holds the items you ask
  people to find.
- **Tasks:** resource-finding tasks for key business goals; "sleight-of-hand" tasks for
  lesser items that test a parent category's information scent; potential problem areas
  such as new categories or places card-sort participants disagreed; and an easy warm-up
  task, which in unmoderated tests also screens out inattentive participants.
- Define the correct answer(s) per task so the tool can compute success rates.
- Do not use words from the target label in the task wording (priming); keep tasks short.
- **Metrics:** success (found the correct answer), the other categories chosen, time,
  and **directness** (went straight to the choice versus bouncing between categories),
  a proxy for how clear and confident the path is.
- **Qualitative** tree tests need few participants, are often moderated and give no
  statistics. **Quantitative** tests need a larger sample and are used to benchmark and
  compare structures (current, competitor, redesign options). Start a quantitative test
  with a small qualitative pilot to catch confusing tasks and labels.
- Benchmark the current IA at the start of a redesign and compare it with the new tree.

## Gotchas
- Sorting your current menu labels validates the status quo and learns nothing.
- Skipping the tree test because "the card sort was clear": card sorts generate, trees validate.
- Tree testing has limits on sites with mega menus; focus on whether the right top-level
  category was chosen rather than only on success rates.

## Verify
- [ ] Content inventory done before restructuring.
- [ ] Card count 30-50, with no repeated keywords across card labels.
- [ ] Participant numbers match the study type (qualitative 15+, quantitative 30-50+).
- [ ] New tree tested with defined correct answers and unprimed task wording.
- [ ] No top-level label is a vague catch-all such as "Other".

## Checked
2026-11-09. Confirmed against the two Nielsen Norman Group articles (card-sorting definition and tree testing): open/closed/hybrid sorts, 30-50 cards, repeated-keyword warning, 15 participants qualitative and 30-50 quantitative, similarity matrix and dendrogram in OptimalSort, tree construction, task types, directness, qualitative versus quantitative tree tests, pilot before quantitative test, mega-menu caveat. Removed unconfirmed specifics: similarity thresholds, 5-9 top-level categories and 3-level depth, 8-10 tasks, 50 tree-test participants, success-rate targets, first-click claim, the search-tuning section, and named tools other than OptimalSort.
Method: documentation only; no commands were run.
