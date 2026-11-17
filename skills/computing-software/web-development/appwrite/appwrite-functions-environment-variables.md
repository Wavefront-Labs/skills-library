---
id: computing-software.web-development.appwrite.appwrite-functions-environment-variables
name: appwrite-functions-environment-variables
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, functions, environment-variables, secrets, configuration]
level: practitioner
status: docs-checked
description: "Set function and project variables, understand precedence and Appwrite-injected variables, and mark secrets."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/environment-variables/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure functions without hardcoding values.

Levels and precedence, in order: project variables are shared across every function and site in the project; function variables are scoped to one function and override a project variable with the same key; Appwrite-injected variables (for example `APPWRITE_FUNCTION_PROJECT_ID`) take final precedence and cannot be overridden, so do not set keys with the `APPWRITE_` prefix.

Set them in the Console (function Settings tab > Environment variables > Create variable; project Settings for global ones) or with a Server SDK whose API key has the `functions.write` scope to create, update or delete, or `functions.read` to list and read. Limits: variable ID 36 characters (`a-z A-Z 0-9 . - _`), key 255 characters, value 8192 characters.

Secret flag: marking a variable secret hides its value from the Console and API after creation; only the function runtime can read it. Marking secret cannot be reversed; to replace a secret value, delete the variable and create a new one with the same key.

Build time: during the build, a dynamic API key is provided as `APPWRITE_FUNCTION_API_KEY`; it does not need to be initialized. Variables are readable at build and runtime through your runtime's standard environment lookup.

Gotcha: variable changes only take effect on the next deployment; redeploy after creating, updating or deleting variables.

Keep secrets out of logs.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Environment variables (functions/environment-variables), read from the raw markdown because the rendered page was truncated: the three-source precedence, Console steps, `functions.write` and `functions.read` scopes, the update and secret behaviour, `APPWRITE_FUNCTION_API_KEY` during builds, the redeploy rule and the limits table (including the 36-character variable ID). Removed: the `process.env.MY_VAR` Verify step.
Method: documentation only; no commands were run.
