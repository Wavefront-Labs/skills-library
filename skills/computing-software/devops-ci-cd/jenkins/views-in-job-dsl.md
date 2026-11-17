---
id: computing-software.devops-ci-cd.jenkins.views-in-job-dsl
name: views-in-job-dsl
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, listview-dsl, job-dsl, folder-dsl]
level: intro
status: draft
description: "Generate Jenkins list views, nested views and folder views with Job DSL using regex job selection and standard columns so dashboards stay in sync with generated jobs."
sources: ["https://jenkinsci.github.io/job-dsl-plugin/#path/listView", "https://jenkinsci.github.io/job-dsl-plugin/#path/folder"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Views in Job DSL

```groovy
listView('team-a') {
  description('All team-a jobs (generated)')
  filterBuildQueue(); filterExecutors()
  jobs {
    regex(/team-a-.*/)
    name('shared-release')
  }
  recurse(true)                     // include jobs inside folders
  columns {
    status(); weather(); name()
    lastSuccess(); lastFailure(); lastDuration(); buildButton()
  }
}

nestedView('platform') {            // needs nested-view plugin
  views {
    listView('builds') { jobs { regex(/.*-build/) } ; columns { status(); name() } }
    listView('deploys') { jobs { regex(/.*-deploy/) } ; columns { status(); name() } }
  }
}

folder('team-a') {
  views {
    listView('failing') {
      jobFilters { status { status(Status.FAILED) } }    // view-job-filters plugin
      columns { status(); name(); lastFailure() }
    }
  }
}
```

## Notes
- Prefer folders for organisation and permissions; views are only filters.
- Regex matches job **names**, not full paths, unless `recurse(true)` and the view-job-filters plugin with path matching are used.
- Views created in the UI are overwritten on the next seed run if the DSL defines the same name;
  manual edits are lost.
- `dashboardView` (dashboard-view plugin) for portlets like test trends.

## Verify
- [ ] Seed run log shows "Added views"; the view lists the expected jobs.
