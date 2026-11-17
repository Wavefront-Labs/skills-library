---
id: computing-software.search-and-information-retrieval.meilisearch.ranking-score-and-details
name: ranking-score-and-details
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [ranking-score, show-ranking-score, relevancy-debugging, meilisearch]
level: advanced
status: docs-checked
description: "Request _rankingScore and _rankingScoreDetails in Meilisearch with showRankingScore flags, read per-rule subscores, and know which settings influence the score."
sources: ["https://www.meilisearch.com/docs/capabilities/full_text_search/relevancy/ranking_score"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ranking score and score details

`_rankingScore` is a value from 0.0 to 1.0 (1.0 is a perfect match). It is not returned unless you set `showRankingScore` to `true` in the search body. Set `showRankingScoreDetails` to `true` as well to get `_rankingScoreDetails`, one nested object per active rule with fields such as `order`, `matchingWords`, `typoCount` and `score`.

## How it is computed

Subscores from relevancy rules (words, typo, proximity, attributeRank, wordPosition, exactness) are combined, weighted by rule position in the list, so earlier rules weigh more. `sort` does not measure relevance and does not affect the score; in details it shows a `value`, not a `score`. A document's score does not depend on other documents.

## Settings that influence it

- `rankingRules`: always.
- `stopWords` and `synonyms`: always, via the words rule.
- `searchableAttributes`: when attributeRank or wordPosition is used.
- `typoTolerance`: when the typo rule is used.
Other settings do not.

## Reading an example

For "chicken curry" sorted by `prep_time_minutes:asc` with sort after proximity: words and typo tie, proximity separates the documents (1.0 versus 0.5), so sort never acts and the faster recipe can rank second. A higher `_rankingScore` can thus rank lower when sort takes priority.

## Uses

Debugging relevancy, relevancy badges in the UI, frontend score thresholds such as 0.5, and comparing configurations.

## Checked

2026-11-03. Confirmed claim by claim against the Ranking score page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
