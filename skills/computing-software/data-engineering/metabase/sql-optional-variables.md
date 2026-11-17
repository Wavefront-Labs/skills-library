---
id: computing-software.data-engineering.metabase.sql-optional-variables
name: sql-optional-variables
category: computing-software
field: data-engineering
product: metabase
tags: [optional-variables, double-brackets, where-true, sql-variables, default-value]
level: practitioner
status: docs-checked
description: "Make Metabase SQL filters optional with double square brackets around the whole clause, keep the query valid when dropped, chain AND clauses, and set defaults."
sources:
  - https://www.metabase.com/docs/latest/questions/native-editor/optional-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wrap the entire clause containing the `{{variable}}` in `[[ ... ]]`. If no value is given in the filter widget (or via the URL), Metabase ignores the clause and runs the query as though it did not exist.

```sql
SELECT count(*) FROM products [[WHERE category = {{cat}}]]
```

Rules and gotchas:
- The SQL must stay valid without the bracketed clause. Put the `WHERE` keyword inside the brackets, not just the condition; otherwise an empty value leaves a dangling `WHERE` and the query errors.
- For several optional clauses, include at least one regular `WHERE` first, such as `WHERE TRUE`, then add each as `[[AND id = {{id}}]]`.
- With field filters, omit the column in the clause: `[[AND {{category}}]]`, and map the variable in the side panel.
- MongoDB: wrap a whole pipeline stage in `[[ ]]`, including its trailing comma.
- Complex defaults: put comment syntax inside the closing brackets, as in `WHERE column = [[ {{your_parameter}} --]] your_default_value`. When a value is passed the comment activates and hides the default; otherwise the default (for example `CURRENT_DATE`) applies. The `--` may need to change to your database's comment syntax.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Removed the closing claim about transform SQL variables (the page does not mention transforms). Rest unchanged.
