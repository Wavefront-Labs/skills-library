---
id: computing-software.devops-ci-cd.gitlab-ci.review-app-route-maps
name: review-app-route-maps
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, route-maps, review-app-routes, route-map-yml, view-on-review-app]
level: practitioner
status: docs-checked
description: "Map source files to review app pages with .gitlab/route-map.yml so merge request diffs get direct View on environment links to the changed page."
sources: ["https://docs.gitlab.com/ci/review_apps/#route-maps"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Review app route maps

With a route map, files matching a mapping get a **View on [environment-name]** link on the file page and a review app icon next to the filename.

## 1. `.gitlab/route-map.yml`
```yaml
# each entry maps a source path in the repository to a public path
- source: 'content/index.md'
  public: 'index.html'
# regex entries: see the route maps section of the review apps docs
```
GitLab evaluates mappings in order of definition; the first matching source expression determines the public path.

## 2. Requirements
- A review app must be configured (an environment with `environment:url`).
- The route map is the file `.gitlab/route-map.yml` in the repository.
- A regex source must match the entire source path (`^` and `$` are implied).

## 3. Use cases
- Docs sites (Hugo, Docusaurus, MkDocs): reviewers jump straight to the changed page.
- Marketing sites/component libraries (Storybook stories mapped to story URLs).

## Gotchas
- Test the map with a merge request that touches one file per rule.

## Verify
- [ ] The file page shows **View on [environment-name]** and opens the right page.

## Checked

2026-10-28. Confirmed against the GitLab review apps route maps section: .gitlab/route-map.yml, source/public entries, regex must match the entire source path, mappings evaluated in order with the first match winning, View on [environment-name] on the file page and review app icon. Removed: the /regex/ literal syntax, escaping rule, relative-path and source-branch claims and the silent-failure claim (not on the page).

Method: documentation only; no commands were run.
