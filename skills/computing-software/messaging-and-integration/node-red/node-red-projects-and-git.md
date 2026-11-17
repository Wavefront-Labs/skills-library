---
id: computing-software.messaging-and-integration.node-red.node-red-projects-and-git
name: node-red-projects-and-git
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, projects, git, version-control, credentialsecret, ssh-keygen, flows-json, credentials]
level: practitioner
status: docs-checked
description: "Enable Node-RED projects so flows live in a Git repository: setup, creating a project, credential file encryption, project settings and the history sidebar."
sources: ["https://nodered.org/docs/user-guide/projects/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Node-RED projects and Git

Projects manage flow files as a redistributable application backed by a Git repository, so files are version controlled. The page describes the feature in the 0.18 release as preview, so it must be enabled: add this inside `module.exports` of `settings.js` and restart Node-RED.

```javascript
editorTheme: {
    projects: {
        enabled: true
    }
},
```

Alternatively set the `NODE_RED_ENABLE_PROJECTS` environment variable to `true`. The feature needs the `git` and `ssh-keygen` command line tools; Node-RED checks at start-up and reports if they are missing.

On first opening the editor, a welcome screen walks through: set up version control (a Git username, which can be anything, and email; existing Git settings are reused and can be changed in the main settings dialog), name and describe the project, create the project files (existing flow files are migrated and can be renamed), and set up encryption of the credentials file. Encryption is strongly recommended if you share publicly. The key is not stored in the project, so someone who clones it must be given the key or must enter their own credentials in the flow. The project is created in `~/.node-red/projects/<project-name>`.

The Info sidebar shows the current project with a button for Project Settings, also under Projects, Project Settings in the main menu. Its tabs are Project (edit README.md), Dependencies (the project's own `package.json` module list) and Settings (flow files, credential encryption, git branches and remotes). A history tab in the sidebar has Local Changes (stage and commit) and Commit History (branches, push and pull).

## Checked

2026-11-04. Confirmed against the Node-RED user guide page Projects. Removed: the 'Projects disabled' Docker log line and the non-project flows.json/credentialSecret paragraph (not on the cited page).

Method: documentation only; no commands were run.
