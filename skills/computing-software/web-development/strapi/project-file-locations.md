---
id: computing-software.web-development.strapi.project-file-locations
name: project-file-locations
category: computing-software
field: web-development
product: strapi
tags: [strapi, project-structure, folders, src-api, config, file-layout]
level: intro
status: docs-checked
description: "Where Strapi loads controllers, services, routes, policies, middlewares, components, migrations and config files from."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/project-structure.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/models.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/policies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Where things live in a Strapi project

A project is TypeScript or vanilla JavaScript; the structure differs slightly (the project structure page is an interactive component, so the paths below come from the backend customization, configuration and migration pages). Paths stated in the docs:

| What | Location |
|---|---|
| API controllers | `./src/api/[api-name]/controllers/` (auto-loaded) |
| API services | `./src/api/[api-name]/services/` |
| API routes | `./src/api/[api-name]/routes/` |
| Content-type schema | `./src/api/[api-name]/content-types/[content-type-name]/schema.json` |
| Lifecycle hooks | `lifecycles.js` in the same content-type folder (must be created manually) |
| Components | `./src/components/<category>/` |
| Global policies | `./src/policies/` |
| API policies | `./src/api/[api-name]/policies/` |
| Application middlewares | `./src/middlewares/` |
| API middlewares | `./src/api/[api-name]/middlewares/` |
| Plugin code | `./src/plugins/[plugin-name]/` |
| Global register/bootstrap/destroy | `./src/index.js` or `./src/index.ts` |
| Config | `./config/` (`server`, `admin`, `database`, `plugins`, `middlewares`, `api`) |
| DB migrations | `./database/migrations` |

Controllers are auto-loaded from their folder, so the location matters. Component models cannot be created with CLI tools: use the Content-type Builder or create them manually.

## Checked

2026-11-04: checked against the Strapi docs pages Models, Controllers, Services, Routes, Policies, Middlewares (backend customization and configurations), Functions, Database migrations and Project structure. Confirmed: every path in the table, the manual creation of `lifecycles.js`, controller auto-loading, `./src/index.js` or `.ts`, `./database/migrations`. Removed: 'Prefer strapi generate', which the pages do not state as a rule. Noted: the Project structure page itself holds only an interactive component, so its tree could not be read as text.

Method: documentation only; no commands were run.
