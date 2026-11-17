---
id: computing-software.devops-ci-cd.spinnaker.fiat-service-accounts
name: fiat-service-accounts
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [fiat, service-accounts, run-as-user, front50, automated-triggers, roles-sync]
level: advanced
status: docs-checked
description: "Create, check and delete Fiat service accounts through Front50 for automated pipelines, and the every-role rule against privilege escalation."
sources:
  - https://spinnaker.io/docs/setup/other_config/security/authorization/service-accounts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Fiat service account is an abstraction around a set of roles, not an authenticated identity. It lets an automatically triggered pipeline (for example a Git commit triggering Jenkins, then a deploy to a protected QA account) run with permissions a person might not hold.

**Create** via Front50, since there is no UI for creating service accounts:

```bash
curl -X POST -H "Content-type: application/json" \
  -d '{ "name": "sekret-service-account@spinnaker-test.net", "memberOf": ["myApp-prod","myApp-qa"] }' \
  $FRONT50/serviceAccounts
```

`memberOf` holds **role** names, not application names. List with `curl $FRONT50/serviceAccounts`. A Fiat sync may be needed: `curl -X POST $FIAT/roles/sync`. Check effective access with `curl $FIAT/authorize/<service account>`.

**Who may use it.** To prevent privilege escalation, only users holding **every** role of the service account may use it. If Alfred has roles foo and bar, a user with foo, bar and baz can use Alfred; a user with only foo cannot. Also, the service account itself needs `EXECUTE` on the application.

**Use:** with Fiat on, triggers show a "Run As User" list. On save, two checks run: the user can use the account, and the account can access the application. At runtime normal account and application checks apply.

**Delete:** `curl -X DELETE "$FRONT50/serviceAccounts/<id>"` where the id is the lower-cased name, then sync Fiat if needed.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Service Accounts page. Confirmed create, list, sync, authorize and delete calls, the every-role rule, the EXECUTE requirement and the two save-time checks. Removed the Halyard-support claim, which the page does not make.
