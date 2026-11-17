---
id: computing-software.cybersecurity-defensive.splunk.elastic-defend-response-actions
name: elastic-defend-response-actions
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [elastic-security, elastic-response-actions, elastic-defend, host-isolation, endpoint-response, incident-response, edr]
level: practitioner
status: docs-checked
description: "Run Elastic Defend response actions on endpoints: isolate/release, kill or suspend process, get-file, execute, scan, upload, with privileges, history and automated rule actions."
sources: ["https://www.elastic.co/guide/en/security/current/response-actions.html", "https://www.elastic.co/guide/en/security/current/host-isolation-ov.html", "https://www.elastic.co/guide/en/security/current/automated-response-actions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Elastic Defend response actions

## Requirements
- The appropriate subscription (Elastic Stack) or project feature tier (Serverless) for response actions and the response console.
- Endpoints run Elastic Agent 8.4 or higher with the Elastic Defend integration.
- Unless stated otherwise, actions work on Linux, macOS and Windows.
- Host isolation on Elastic Stack 7.15.0 and later: Windows, macOS and these Linux distributions: CentOS/RHEL 8, Debian 11, Ubuntu 18.04, 20.04 and 22.04, AWS Linux 2.

## Response console
Open it from the Endpoints page (Actions menu > Respond), the endpoint details flyout, alert details flyout or event details flyout (Take action > Respond), or the Host details page (Respond). Type a command and press Return. `help` lists commands, `<command> --help` shows one, `clear` clears the output, and the Help panel builds commands for you and shows only actions your role permits.

| Command | What it does | Privilege (Elastic Stack) |
|---|---|---|
| `isolate` / `release` | Block / restore communication with other hosts | Host Isolation |
| `processes` | List processes (can take a minute); gives PIDs and entity IDs | Process Operations |
| `kill-process`, `suspend-process` | Needs `--pid` or `--entityId` | Process Operations |
| `get-file --path` | Download a file in a password-protected zip (password `elastic`) | File Operations |
| `upload --file [--overwrite]` | Save a file where Elastic Endpoint is installed; path is shown after | File Operations |
| `execute --command [--timeout]` | Run a shell command (bash on Linux/macOS, cmd.exe on Windows) | Execute Operations |
| `scan --path` | Recursive malware scan, using the policy's malware protection settings | Scan Operations |
| `memory-dump` | `--kernel`, `--process` (with `--pid` or `--entityId`) or `--raw`; fetch the dump afterwards with `get-file` | Execute Operations |
| `runscript` | Elastic Defend: `--script` from the script library; also third-party EDRs | Execute Operations |
| `cancel --action` | Cancel a pending or in-progress action (Elastic Defend: only execute, get-file, memory-dump, runscript, scan, upload); `--force` optional | Same as the action cancelled |
| `status` | Agent status and version, integration policy status, last active time | |

Add `--comment "..."` to any command; comments appear in the response actions history. Example: `isolate --comment "Isolate host related to detection alerts"`.

## Details worth knowing
- `execute`: console shows up to 2000 characters; full stdout and stderr are saved in a downloadable zip (password `elastic`). Without `--timeout` it defaults to four hours. It runs as the account running Elastic Defend, which normally has full control of the system. Multiple consecutive dashes in a value must be escaped.
- `get-file`: maximum 104857600 bytes (100 MB) on Elastic Stack (not applied on Serverless). To fetch a file quarantined by malware prevention, use the alert's Quarantined file path field (`file.Ext.quarantine_path`) as `--path`.
- `processes`: entity IDs are more reliable than PIDs, because PIDs can be reused by the operating system.
- `upload`: the maximum size is set by `xpack.securitySolution.maxUploadResponseActionFileBytes` in `kibana.yml` (bytes); too high a value can cause timeouts.
- Isolated hosts can still send data to Elastic Security; you can define host isolation exceptions for IP addresses an isolated host may still reach.

## Privileges
Each action needs its own privilege (names in the table). Users also need at least Read on the Response Actions History privilege to see command output and status; without it the action is created but the user cannot monitor it. Serverless uses predefined roles (Tier 3 analyst, SOC manager, Endpoint operations analyst) or custom roles with the feature privilege. Give analysts only the privileges they need.

## Offline hosts and cancelling
If a host is unavailable, pending actions run when it comes online and expire after two weeks. A submitted action cannot be cancelled in general (the `cancel` command covers the listed actions above).

## Automated response actions
A custom query rule (or endpoint rule) can include an Elastic Defend response action: on the last step of rule creation, Response Actions > Elastic Defend; for an existing rule, Actions tab. Options are Isolate, Kill process, Suspend process and Run script. For process actions you choose the alert's `process.pid` or a custom field. The rule author needs the privilege for that action. Elastic warns that automatic isolation can disrupt legitimate users and block critical business processes.

## History
Click Response actions history in the console or open the endpoint's Response action history tab; filterable.

## Verify
On a test host: isolate, confirm isolation, run `processes`, release, then check the history shows each action with its comment.

## Checked
Confirmed against Elastic's Endpoint response actions, Isolate a host and Automated response actions pages. Removed because the pages do not state them: the "Enterprise licence" requirement for specific actions, the `GET /api/endpoint/action` call, DNS/Active Directory isolation effects, tiered-access advice and tag-based exceptions.
Method: docs-only read of cited pages, 2026-11-08
