---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gcloud-output-formatting-and-filtering
name: gcloud-output-formatting-and-filtering
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gcloud, gcloud-format, gcloud-filter, gcloud-output, gcloud-projections, gcloud-topic-filters, value-format, csv-format, json-format, table-format, gcloud-sort-by, gcloud-limit, jq-alternative]
level: practitioner
status: docs-checked
description: "Get exactly the fields you want from gcloud list/describe with --format (value, csv, json, table projections), --filter expressions, --sort-by and --limit, without jq."
sources: ["https://cloud.google.com/sdk/gcloud/reference/topic/formats", "https://cloud.google.com/sdk/gcloud/reference/topic/filters", "https://cloud.google.com/sdk/gcloud/reference/topic/projections", "https://cloud.google.com/sdk/gcloud/reference/compute/instances/list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gcloud output formatting and filtering

**Goal:** scriptable, exact output from gcloud: the right field, nothing else, filtered server-
or client-side, so shell loops do not depend on column positions.

## 1. See the field names first
```bash
gcloud compute instances list --format=json --limit=1      # the real resource shape
gcloud compute instances describe <VM> --zone=<Z> --format=flattened   # one key:value per line
```
The topic pages suggest `--limit=1` with `--format=text` (an alias of `flattened`) or `--format=yaml` to
list the fields you can sort, filter and format by. Keys are dotted paths such as `parent.id`.

## 2. Formats
```bash
--format='value(name)'                                   # one value per line, no header: for $(...)
--format='value(name,zone.basename())'                   # tab-separated by default
--format='value[separator=","](name,status)'
--format='csv[no-heading](name,machineType.basename())'  # csv: "," separator, ";" list delimiter
--format='table(name,zone.basename(),status:label=STATE)'
--format='table[box,title=Instances](name:sort=1, zone:label=zone, status)'
--format='yaml(name,status)'                             # projection limits the keys
--format='flattened(name,serviceAccounts[].email)'
--format='json'
--format='get(id)'                                       # value[no-transforms]
--format='disable'                                       # disables formatted output
```
`value`, `csv` and `table` need a projection (the part in parentheses). Unknown attributes are
silently ignored. Transforms are chained on a key; those documented on the projections page include
`.basename()`, `.scope()` (the part after `regions/` or `zones/`; `.scope(projects)` starts at a named segment),
`.date(format, tz=LOCAL)`, `.len()`, `.list()` (compact comma-separated list), `.yesno(yes, no="No")`,
`.map()` (apply the next transform to each list item), `.segment(index)`, `.join(sep)` and `.uri()`.
`.if(expr)` is different: it disables a column depending on a command flag, not on resource data.

## 3. Filters (client-side, server-side or both, depending on the API)
```bash
--filter='status=RUNNING'
--filter='name~^web-.*'                      # ~ regular expression (Python re), !~ negated
--filter='labels.env=prd AND NOT zone:europe'
--filter='createTime>-P2W'                   # ISO 8601 duration: created within two weeks
--filter='machineType:f1-micro'              # : is a pattern match
--filter='tags.items=(my-tag,my-other-tag)'  # =( ... ) matches any value in the list
--filter='labels.my-label:*'                 # key is defined; -labels.my-label:* means undefined
```
`gcloud topic filters` documents the operators. Logic operators must be uppercase (`AND`, `OR`, `NOT`);
an expression that mixes `AND` and `OR` must be parenthesized; two terms side by side are an implicit
AND. Quote the whole expression, and use the other quote style for literals inside it. A value that
looks like a number in scientific notation (for example `30e5504145`) needs quoting as a string.
The `:` operator is changing: the old default is a case-insensitive "contains", the new behaviour
matches whole words with an optional trailing `*` for prefix match, and gcloud warns when the two
would differ. For `=`, some APIs treat it as an exact match and a few as `:`, so check with a small
list first. Timestamps compare as in `createTime>=2018-01-15`.

## 4. Sort, limit, page
```bash
--sort-by=~creationTimestamp --limit=10      # ~ = descending
--page-size=500                              # maximum resources per page
```
The list-command reference says these flags apply in the order `--flatten`, `--sort-by`, `--filter`,
`--limit`, so `--limit` cuts the final, filtered, sorted result. `--page-size` sets the maximum
resources per page; paging may happen before or after `--filter` and `--limit` depending on the service.

## 5. Patterns
```bash
# loop safely
for vm in $(gcloud compute instances list --filter='labels.tier=batch' --format='value(name)'); do ...; done
# name + zone pairs
gcloud compute instances list --format='value(name,zone.basename())' | while read -r n z; do gcloud compute instances stop "$n" --zone="$z" --quiet; done
# all project IDs under a folder
gcloud projects list --filter='parent.id=123456789012 AND lifecycleState=ACTIVE' --format='value(projectId)'
# key from describe
IP=$(gcloud compute addresses describe lb-ip --global --format='value(address)')
# nested list: flatten first, then filter on the flattened key
gcloud projects get-iam-policy <PROJECT_ID> --flatten=bindings --filter=bindings.role:roles/editor --format='value(bindings.members)'
```
`--format` and `--flatten` are global flags; check each list command's reference page for `--filter`, `--limit`,
`--sort-by`, `--uri` and `--page-size`.

## Gotchas
- The filter and format flags need quoting so the shell leaves `~`, `<` and `>` alone.
- `table[box]` and `title=` are for readable terminal output; scripts should use `value(...)` or `csv[no-heading](...)`.
- `gcloud compute instances list --uri` prints only resource URIs. If combined with `--format`, the format applies to that URI list; use the `uri()` transform to show URIs beside other keys.
- Use `json-decode` or `private` format attributes only if you need them: `private` disables log-file output of sensitive data.

## Verify
- [ ] `gcloud compute instances list --format='value(name)'` returns bare names with no heading.
- [ ] A filter with `AND NOT` and a regex returns the expected subset compared to `--format=json | jq`.
- [ ] Scripts use `--format=value(...)` rather than parsing the default table.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the gcloud topic pages (formats, filters, projections) and the `gcloud compute instances list`
reference: format names, attributes and defaults (csv, value, table, flattened, get, disable, text alias),
transform names, filter operators, ISO 8601 duration and `:` behaviour, and the flag order
`--flatten`, `--sort-by`, `--filter`, `--limit`. Removed: `json(name,labels)`, field paths and filter examples
the pages do not show (preemptible, provisioningModel, accessConfigs), `.if(cond)` as a data filter, and the
unsourced claims about empty-field output, nested-array matching, `Invalid filter` errors and table wrapping.
