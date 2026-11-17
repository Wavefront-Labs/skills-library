---
id: computing-software.data-engineering.snowflake.streamlit-in-snowflake
name: streamlit-in-snowflake
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, streamlit-in-snowflake, streamlit, data-apps, snowflake-cli]
level: practitioner
status: docs-checked
description: "Build and deploy Streamlit in Snowflake apps: runtimes, Snowflake CLI deployment, owner's rights security model, viewer access and review."
sources:
  - https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit
  - https://docs.snowflake.com/en/developer-guide/snowflake-cli/streamlit-apps/overview
  - https://docs.snowflake.com/en/developer-guide/streamlit/object-management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streamlit in Snowflake

**Goal:** internal data apps that run inside Snowflake, using Snowflake auth and RBAC, no separate hosting.

## What it is
Streamlit apps built, deployed and shared on Snowflake. Snowflake manages the compute and storage; source code and environment configuration live in a Snowflake object whose access is governed by RBAC. You choose a **warehouse runtime** or a **container runtime**. It works with Snowpark, UDFs, stored procedures and the Native App Framework, and Snowsight offers a side-by-side editor and preview. A Streamlit app is a schema-level object.

## Create and deploy
- Snowsight, SQL or Snowflake CLI can deploy an app from existing code. The CLI covers creating, deploying, retrieving the URL of, sharing and managing apps, so a local IDE plus Git CI/CD flow works without hand-written SQL or manual stage copies.
- Look up exact `snow streamlit` subcommands and the `snowflake.yml` entity fields in the CLI reference for your CLI version before scripting; they are not reproduced here.
- Warehouse and container runtimes differ in packaging and restrictions; read "Runtime environments for Streamlit apps" before choosing.

## Security model (owner's rights)
By default an app runs with the **owner's privileges, not the caller's**, with the **warehouse provisioned by the owner**, and in the database and schema the app was created in (not the caller's current ones).
- The owner chooses which roles can use the app. Viewers see anything displayed, and the app may use all of the owner role's privileges when shared, whether or not the privilege has WITH GRANT. So the owner role must be least-privilege; use dedicated roles for creating and for viewing apps.
- Write privileges on the app let a user modify it; grant them cautiously. Responsibility for app security is shared with owners; audit apps regularly.
- If an app uses context functions, grant the global READ SESSION privilege to the owner role.
- Warehouse-runtime apps run as a stored procedure and inherit owner's rights stored procedure restrictions (callable built-ins, ALTER USER, DESCRIBE/SHOW/LIST, statement types). Container-runtime apps are not subject to these. A container-runtime app can instead run with restricted caller's rights (see that page).

## Cost
The app uses the owner's warehouse, so size and auto-suspend it deliberately; check the docs for how runtime choice affects billing before you commit.

## Verify
A viewer role granted only access to the app opens it and sees the data the owner role can read; the owner role holds no more privileges than the app needs.

## Checked
2026-11-09. Confirmed on "About Streamlit in Snowflake", "Managing Streamlit apps with Snowflake CLI" and the owner's rights page (now served at the object-management URL): features, runtimes, schema-level object, CLI operations, owner's rights rules, viewing and roles, READ SESSION, warehouse versus container restrictions, security guidance. Removed: the snowflake.yml and snow commands, Snowpark session sample, pip/Anaconda packaging claims, `st.user` and caching tips, and the warehouse running-while-viewed claim, because the pages read do not state them.
Method: documentation only; no commands were run.
