---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-adjacency-list-many-to-many
name: dynamodb-adjacency-list-many-to-many
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, many-to-many, adjacency-list, inverted-index, gsi-overloading]
level: advanced
status: docs-checked
description: "Model many-to-many relationships in DynamoDB with the adjacency list pattern and an inverted GSI, deciding what to denormalise onto edge items."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html", "https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchGetItem.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adjacency list and many-to-many relationships

## 1. Pattern
Example: students and courses. Store each entity once and one **edge item** per relationship:
| PK | SK | Attributes |
|---|---|---|
| `STUDENT#s1` | `STUDENT#s1` | name, email |
| `COURSE#c9` | `COURSE#c9` | title, credits |
| `STUDENT#s1` | `COURSE#c9` | enrolledAt, courseTitle (denormalised) |
| `STUDENT#s2` | `COURSE#c9` | enrolledAt, courseTitle |

## 2. Inverted index
Create a GSI whose partition key is the table's sort key attribute and whose sort key is the table's
partition key attribute (`SK` as HASH, `PK` as RANGE), named `GSI1` here. Edge items then appear in
the index keyed by course, and no extra attributes are needed:
- Courses for a student: `Query PK = STUDENT#s1 AND begins_with(SK, 'COURSE#')` on the table.
- Students in a course: `Query SK = COURSE#c9 AND begins_with(PK, 'STUDENT#')` on the GSI.
```bash
aws dynamodb query --table-name school --index-name GSI1 \
  --key-condition-expression "#sk = :c AND begins_with(#pk, :p)" \
  --expression-attribute-names '{"#sk":"SK","#pk":"PK"}' \
  --expression-attribute-values '{":c":{"S":"COURSE#c9"},":p":{"S":"STUDENT#"}}'
```
GSI reads are eventually consistent only, and the index is maintained asynchronously.

## 3. Denormalisation choices
- Copy the attributes needed for list views onto the edge (course title, student name) so one Query renders the page.
- Updates to a copied attribute fan out to every edge: fine for rarely changing data (titles), bad for
  volatile data (prices). Keep volatile data only on the entity and fetch it with `BatchGetItem` (up to 100 keys per call).
- Edge-specific data (grade, role) belongs on the edge.

## 4. Limits
- An item collection (all items sharing a partition key) has a 10 GB limit only when the table has an LSI;
  heavy writes concentrated on one partition key value still need care.

## Verify
- [ ] Both directions answered by single queries returning only the needed items.

## Checked
Checked 2026-10-24 against the current DynamoDB Developer Guide and API Reference. Confirmed: GSI key schema may
differ from the table and index keys can be any top-level String, Number or Binary attribute (GSI page);
GSI reads are eventually consistent and asynchronously updated (GSI page); `BatchGetItem` accepts up to 100 keys
(API Reference); the 10 GB item-collection limit applies to tables with LSIs (BatchWriteItem error text and
service model); `query` parameters `--index-name`, `--key-condition-expression`, `--expression-attribute-names`
and `--expression-attribute-values` exist in the service model. Removed the Neptune traversal advice, which was
opinion rather than a documented limit, and corrected the inverted-index description to use the table key
attributes directly.
Method: documentation only; no commands were run.
