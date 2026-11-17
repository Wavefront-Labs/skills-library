---
id: computing-software.software-engineering.cobol.zowe-cli-workflow
name: zowe-cli-workflow
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, zowe-cli-workflow, cobol-devops, zowe-cli, zos-files, zos-jobs, mainframe-ci]
level: practitioner
status: docs-checked
description: "Upload source, submit JCL and fetch job output from a pipeline using Zowe CLI."
sources:
  - https://docs.zowe.org/
  - https://docs.zowe.org/stable/user-guide/cli-using-using-team-profiles/
  - https://docs.zowe.org/stable/user-guide/cli-using-creating-profiles/
  - https://github.com/zowe/zowe-cli/blob/master/README.md
  - https://github.com/zowe/zowe-cli/tree/master/packages/cli/src/zosfiles
  - https://github.com/zowe/zowe-cli/tree/master/packages/cli/src/zosjobs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zowe CLI for datasets, jobs and CI pipelines
**Goal:** a scriptable mainframe workflow.

```bash
zowe zos-files upload file-to-data-set src/hello.cbl "MY.COBOL.SRC(HELLO)"
zowe zos-jobs submit data-set "MY.JCL(COMPILE)" --wfo      # --wfo = --wait-for-output
zowe zos-jobs view job-status-by-jobid JOB12345
zowe zos-files download data-set "MY.LOADLIB(HELLO)" --binary --file hello.bin
```
- The command groups are `upload`/`download` under `zos-files` and `submit`/`view` under `zos-jobs`. Aliases exist (`ftds` for `file-to-data-set`, `ds` for `data-set`, `jsbj` for `job-status-by-jobid`, `-f` for `--file`, `-b` for `--binary`).
- `--wait-for-output` waits for the job to reach OUTPUT status before the command completes; `--view-all-spool-content` (`--vasc`) prints all spool output and also waits for the job to complete. Both are options of `submit data-set`.
- Create a configuration once with `zowe config init` (`--global-config` writes to the `.zowe` directory in the user home; the default is a `zowe.config.json` in the current directory). It prompts for missing base profile values, and `--no-prompt` skips prompting for CI use. Command names and options differ between Zowe CLI versions, so verify with `zowe --help`.
- Mark `user` and `password` as `secure` fields in the config; update them later with `zowe config secure` (add `--global-config` for the global file). New values go to the secure credential store. Never commit passwords.
- In CI (GitHub Actions, GitLab, Jenkins) install the CLI with `npm i -g @zowe/cli@latest` and run the commands above as steps. The Zowe README warns that a root install on Mac/Linux needs `--ignore-scripts` and that plug-ins installed as root are only reachable as root.
- Zowe Explorer for VS Code uses the same team configuration files (project or global).

## Gotchas
- Text transfer converts data by default; `--binary` (`-b`) transfers with no data conversion (use it for load modules), and `--encoding` converts using the encoding you specify. `--record` prepends record lengths and conflicts with `--binary` on download.
- An upload to a PDS member uses the form `"HLQ.PDS(MEM)"` (the Zowe examples use `"ibmuser.pds(mem)"`).

## Self-check
Upload, compile, run, and fetch the SYSOUT of the hello program from a script.

## Checked
2026-11-08. Confirmed against the Zowe CLI source on GitHub (command definitions and help strings in packages/cli/src/zosfiles, zosjobs and the imperative `config init` definition), the Zowe docs pages on team configurations and creating profiles, and the zowe-cli README. Removed: the 8-character member name rule, the environment-variable credential advice, the claim that the pipeline should fail on non-zero job RC, and the "host, port, user" arguments to `zowe config init` (not options of that command), none of which appear in the pages read.
Method: documentation only; no commands were run.
