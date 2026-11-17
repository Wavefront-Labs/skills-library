---
id: computing-software.web-development.appwrite.appwrite-functions-deploy-cli-manual
name: appwrite-functions-deploy-cli-manual
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, functions, cli, deployments, tar-gz]
level: practitioner
status: docs-checked
description: "Deploy a function by uploading a tar.gz archive or pushing with the Appwrite CLI, and manage deployment states."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/deploy-manually/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/deployments/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/functions/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: deploy without Git.

Manual upload:
1. From the folder that contains your dependency file, package the code as `.tar.gz`: `tar --exclude code.tar.gz -czf code.tar.gz .` (the page gives the same command for bash, cmd and PowerShell). The Functions page says not to include your dependencies folder, such as `node_modules`, and to specify build commands that install dependencies.
2. In the Console open the function, click Create deployment, select the Manual tab, enter the Entrypoint (`index.js` in the page's Node.js example), upload `code.tar.gz`, select Activate deployment after build, and click Create.

CLI: define the function in `appwrite.config.json` (edit it to change project, endpoint, path or entry point; large projects can use multi-file configuration), then run `appwrite push functions`. In non-interactive mode `appwrite push functions --function-id <FUNCTION_ID> --force` pushes a single function.

Deployment statuses: `waiting` (queued), `processing`, `building` (see the build log), `ready` (built but not activated; can be activated to replace the active deployment), `active` (a function can have one active deployment, and a deployment must be active to execute), `failed`. Build logs are under the function's Deployments tab, three-dots menu > Logs. Redeploy from the same menu to retry failed builds; changes to Git settings, Build settings or environment variables only take effect after a redeploy.

Build timeouts: 15 minutes on Free and 45 minutes on Pro (Enterprise is custom). Non-active deployments are deleted after the configured retention period (`deploymentRetention` in days, 0 to 36500; 0 keeps them forever); the active one is always kept.

Gotcha: a `ready` deployment is built but not activated, so activate it (or select the activate option) before expecting new behaviour. Missing dependencies mean updating Build settings; missing files mean checking the Root directory, because only files in it are copied to the executor.

Only CLI deployment and manual upload are covered here; Git deployment is the recommended route.


## Checked

2026-11-04. Confirmed against the Appwrite docs pages Deploy manually and Deployments: the tar command, Console steps, `appwrite.config.json` and multi-file note, the six statuses and their meaning, build logs, redeploy, the 15 and 45 minute build timeouts, deployment retention range, and the debugging notes; the non-interactive push command is on the CLI Non-interactive page. The leave-out-dependencies advice is on the Functions page. Removed: the `appwrite.json` remark, cancelling a build, downloading the source archive, and the Verify step.
Method: documentation only; no commands were run.
