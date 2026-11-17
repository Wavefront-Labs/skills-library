---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-api-filtering-pagination-and-token-scopes
name: controller-api-filtering-pagination-and-token-scopes
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-api-cli, api-filtering, pagination, token-scope, oauth2-token]
level: practitioner
status: docs-checked
description: "Query the controller API efficiently with field lookups, search, order_by and page_size, follow next links, and issue tokens for CI and reporting."
sources: ["https://github.com/ansible/awx/blob/devel/docs/docsite/rst/rest_api/filtering.rst", "https://github.com/ansible/awx/blob/devel/docs/docsite/rst/rest_api/pagination.rst", "https://github.com/ansible/awx/blob/devel/docs/docsite/rst/rest_api/sorting.rst", "https://github.com/ansible/awx/blob/devel/docs/docsite/rst/rest_api/authentication.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# API filtering, pagination and token scopes

## Filtering
```bash
API=https://aap.example.com/api/v2      # AAP 2.5 puts a platform gateway path in front; check your API root
H="Authorization: Bearer $TOKEN"
curl -s -H "$H" "$API/jobs/?status=failed&finished__gt=2026-10-01&order_by=-finished&page_size=50" | jq '.results[] | {id, name, finished}'
curl -s -H "$H" "$API/hosts/?name__icontains=web&inventory__name=Production"
curl -s -H "$H" "$API/job_templates/?search=deploy"
curl -s -H "$H" "$API/jobs/?not__status=successful&launch_type=scheduled"
```
- Any collection is a queryset; extra query-string parameters filter it. Only fields and relations that exist in the database can be used, and fields can span relations with `__` (`?other__field=value`).
- Lookups: `exact` (default), `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`, `gt`, `gte`, `lt`, `lte`, `isnull` (boolean), `in` (comma-separated list).
- Filters are AND-ed. Prefix with `not__` to exclude and `or__` on each parameter to match any. `chain__` applies each filter to a related object separately instead of requiring one related object to satisfy all of them.
- Integer fields need `__int` on the name to cast the string value (`?x__int=5`). URL-encode special characters.
- `order_by=field` sorts, `order_by=-field` reverses, and commas separate several fields.
- `search=text` is a case-insensitive search across a model's designated text fields; `related__search=text` searches related fields.
- Newer releases may return a broader set than the old exact match for some fields (the docs name `limit`): add `__exact` (for example `?limit__exact=host`) for exact matching.

## Pagination
- Collections are paginated; the response holds `count`, `next`, `previous` and `results`. Request the page named by `next` until it is null.
- `page_size` sets the page length; the default maximum is 200 and a larger request is capped. The limit is raised with `MAX_PAGE_SIZE` in a settings file under `/etc/awx/conf.d/` (AWX docs). `page=N` selects a page.
- The docs show `next` as an absolute URL, but some versions return a path: inspect one response before scripting, and prefix the host only if `next` has none.
```bash
url="$API/hosts/?page_size=200"
while [ "$url" != "null" ]; do r=$(curl -s -H "$H" "$url"); echo "$r" | jq -r '.results[].name'; url=$(echo "$r" | jq -r .next); done
```
- Do not request page sizes beyond a couple of hundred; the serializer is efficient but large pages are slow.

## Tokens
- Create a token for CI or reporting tools, give it the narrowest scope the tool needs, and store it in a secret manager.
- Token scope and expiry settings differ between AWX, controller and the AAP 2.5 platform gateway: read the token section of your version's documentation rather than assuming. A token never gives more than the user's roles allow.
- Basic auth sends the username and password on every request; the AWX docs recommend disabling `AUTH_BASIC_ENABLED` when you enforce session limits.

## Gotchas
- Filtering on unindexed text fields over millions of job events is slow; filter jobs first, then fetch events per job.

## Verify
- [ ] A read-scope token gets 403 on a POST launch.

## Checked
2026-10-28. Confirmed against the AWX REST API documentation source (filtering, pagination, sorting, searching, authentication pages): field lookups, `not__`, `or__`, `chain__`, `__int`, `role_level`, `order_by` with `-` and commas, `search` and `related__search`, `page_size` and its default maximum of 200 with `MAX_PAGE_SIZE` under `/etc/awx/conf.d/`, `count`/`next`/`previous`/`results`, `AUTH_BASIC_ENABLED`. Removed because not confirmed: the default page size of 25, the `awx --all` paging flag, the awx CLI `--scope` and `--description` flags, read/write scope semantics, `OAUTH2_PROVIDER` expiry setting and the AAP 2.5 gateway token path (the controller token pages could not be read). The shape of `next` (path or absolute URL) is left to inspection.
Method: documentation only; no commands were run.
