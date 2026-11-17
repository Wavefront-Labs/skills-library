---
id: computing-software.data-engineering.snowflake.native-app-framework
name: native-app-framework
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, native-app-framework, application-package, snowflake-cli, marketplace]
level: sme
status: docs-checked
description: "Build and distribute a Snowflake Native App: application package, manifest and setup script, application roles, versions and patches, release directives and testing."
sources:
  - https://docs.snowflake.com/en/developer-guide/native-apps/native-apps-about
  - https://docs.snowflake.com/en/developer-guide/native-apps/creating-manifest
  - https://docs.snowflake.com/en/developer-guide/snowflake-cli/native-apps/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native App Framework

**Goal:** share data and application logic (Streamlit UI, stored procedures, functions in Snowpark, JavaScript and SQL) that run in the consumer's account.

## Model
- **Provider** builds an **application package**: data content, logic, metadata, setup script, plus the version and patch levels. It requires a manifest file and a setup script.
- **Manifest** (`manifest.yml`): defines setup script location, versions and configuration. It must be named manifest.yml, sit at the root of the directory structure on a named stage, and be uploaded there so the package can read it.
- **Setup script**: SQL that runs when a consumer installs or upgrades the app, and when a provider installs or upgrades it for testing.
- **Distribution**: a listing containing the package, either a Snowflake Marketplace listing (free or paid) or a private listing to specific accounts.
- **Application**: the database object created in the consumer account; Snowflake runs the setup script to create its objects. Consumers can enable logging and event sharing and grant privileges the app needs.
- Providers can release versions and patches incrementally, and log structured and unstructured events for troubleshooting.

## Manifest versions
`manifest_version: 1` supports current and legacy functionality; `manifest_version: 2` adds features such as automated granting of privileges. With v2, listed privileges are granted automatically on install, and consumers agree the app may be granted them during upgrades without extra consent; consumers can limit this with feature policies.
```yaml
manifest_version: 2
version:
  name: v1
artifacts:
  readme: readme.md
  setup_script: setup.sql
privileges:
  - CREATE TABLE:
      description: "Allows the app to create tables in the consumer account"
```

## Apps with containers (Snowpark Container Services)
- Add `artifacts.container_services.images` with one entry per image, path form `/<database>/<schema>/<image_repository>/<image_name>:tag`; images live in an image repository in the provider account, and the package needs a services specification file on a stage.
- Privileges: CREATE COMPUTE POOL (not needed if the consumer creates the pool) and BIND SERVICE ENDPOINT (externally accessible endpoints).
- Optional `default_web_endpoint` (service and endpoint names; endpoint must be in the service spec). Only one of `default_web_endpoint` and `default_streamlit` may be set.
- Provider IP is protected: query text is hidden in QUERY_HISTORY, ACCESS_HISTORY is hidden, and the Query Profile collapses to one empty node.

## Snowflake CLI
The CLI lets you start a project from a git template, define it in a project definition file, create and deploy the application package and an application instance, open the app in a browser, publish to customers, and drop the objects, via the `snow app` commands, without writing SQL. Exact subcommands are on pages beyond the three cited here.

## Security
All human users in provider and consumer accounts must use MFA (SSO users included). Users with TYPE = SERVICE must use key-pair authentication or OAuth.

## Verify
Install the app from a private listing in a test account, grant the requested privileges, and run its objects as a consumer role.

## Checked
Method: docs-only read on 2026-11-09 of all three cited Snowflake pages in full as text (the CLI page is a short index). Removed unstated details: the sample project layout, setup-script and references/register_callback examples, the `snow app run/version create/publish` commands, release directive SQL, idempotency and versioned-schema rules, and the automated security scan claim.
