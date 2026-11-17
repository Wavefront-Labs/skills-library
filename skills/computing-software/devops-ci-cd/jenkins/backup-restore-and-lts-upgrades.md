---
id: computing-software.devops-ci-cd.jenkins.backup-restore-and-lts-upgrades
name: backup-restore-and-lts-upgrades
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jenkins-backup, jenkins-restore, jenkins-home, master-key, secrets-directory, thinbackup, lts-upgrade, jenkins-upgrade, upgrade-path, plugin-compatibility, java-version-upgrade, jenkins-helm, helm-chart, jenkins-docker, jenkins-lts-image, staging-controller, disaster-recovery, rto-rpo, war-upgrade, debian-package-upgrade, old-data-monitor, rollback-upgrade, jcasc-reproducible, plugins-txt, jenkins-plugin-cli]
level: practitioner
status: docs-checked
description: "Back up and restore a Jenkins controller (what in JENKINS_HOME matters, secrets/master.key, consistent snapshots) and upgrade LTS safely with staging rehearsal and rollback."
sources: ["https://www.jenkins.io/doc/book/system-administration/backing-up/", "https://www.jenkins.io/doc/book/platform-information/support-policy-java/", "https://github.com/jenkinsci/docker", "https://github.com/jenkinsci/plugin-installation-manager-tool", "https://github.com/jenkinsci/helm-charts/tree/main/charts/jenkins", "https://www.jenkins.io/doc/book/pipeline/scaling-pipeline/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup, restore and LTS upgrades

**Goal:** lose a controller and be back in under an hour with history intact; take every
LTS without a Monday-morning "Jenkins won't start".

## 1. What to back up (and what not)
`$JENKINS_HOME`:
- **Must**: `config.xml` and all `*.xml` at the root, `jobs/*/config.xml`, `secrets/`
  (`master.key`, `hudson.util.Secret`; the docs say the controller key encrypted with
  `master.key` is needed to restore, and `master.key` should be backed up separately and kept
  very secure), `credentials.xml`, `users/`, `nodes/`, `plugins/*.jpi` / `*.hpi`
  (or just a `plugins.txt`), `jenkins.yaml` (JCasC), `userContent/`.
- **Should**: `jobs/*/builds/` (history, test trends, artifacts) — large; if JCasC + Job DSL
  recreate the jobs, history is the only thing you'd lose.
- **Usually skip** (per the backup guide): `workspace/` (clean checkout after restore),
  `war/`, `cache/` and `tools/` (re-downloadable), `plugins/*/` (expanded dirs, repopulated on
  restart). `jobs/*/builds/archive` only if long-term artifact retention is not needed.
Restore needs the *same* `secrets/` as the `credentials.xml` it decrypts; do not mix files
from two controllers.

## 2. Taking a consistent backup
Jenkins writes XML while running, so back up from a quiet controller or a volume snapshot
rather than copying a busy `$JENKINS_HOME`. Options:
- Filesystem/volume **snapshot** (EBS, ZFS, LVM, PVC VolumeSnapshot).
- Your own script that copies the directories above to another host or object storage.
- The thinBackup plugin: the Jenkins backup guide says it is the only open-source backup
  plugin currently maintained.
- Kubernetes (Helm chart): the chart keeps data on a Persistent Volume Claim under
  `/var/jenkins_home`; back up the PVC (for example with a volume snapshot) and keep
  `jenkins.yaml` and `plugins.txt` in Git.
Keep backups (they contain `master.key`) out of the same blast radius as the controller. The
backup guide recommends validating each backup by restoring it to a temporary location with
`JENKINS_HOME` pointed there and a different HTTP port.

## 3. Restore / rebuild
1. Install the **same** Jenkins version and Java. 2. Stop Jenkins. 3. Restore
`$JENKINS_HOME` (ownership `jenkins:jenkins`). 4. Start; check *Manage Jenkins → Old Data*
and the log for plugin load failures. 5. Reconnect agents (secrets restored → inbound
agents reconnect; cloud agents are recreated). 6. Update the Jenkins URL if the hostname
changed (`jenkins.model.JenkinsLocationConfiguration.xml`).
Reproducible alternative: JCasC + `plugins.txt` + Job DSL seed rebuild a controller from
Git in minutes; only `secrets/` and build history come from backup. Aim for that shape.

## 4. Upgrade path (LTS to LTS)
Read the **upgrade guide** for each LTS line you cross (jenkins.io/doc/upgrade-guide); it
lists breaking changes (Java minimum, removed plugins, agent protocol changes). Rules:
- Jump a few LTS lines at a time rather than across many, reading each line's upgrade guide.
- Check the Java support policy first: it currently lists Java 21 and Java 25 as supported,
  and Java 17 and Java 11 as unsupported (final LTS releases 2.541.3 and 2.462.3). The
  requirement applies to the controller, agents and CLI clients alike, so move agent JDKs
  too; for Kubernetes agents bump the `jenkins/inbound-agent` image tag.
- Plugins: update to the latest compatible set *before* the core upgrade, then again
  after. `jenkins-plugin-cli --plugin-file plugins.txt --available-updates --output txt` and
  `--jenkins-version <core version>` to check compatibility against a specific core release. Pin
  exact versions in `plugins.txt` and commit the resolved list.
- Rehearse on a **staging controller** restored from last night's backup: upgrade there,
  run the seed job, run a representative pipeline per team, check *Manage Jenkins* for
  warnings. Then production in the maintenance window.

## 5. Mechanics by install type
| install | upgrade |
|---|---|
| Debian/RPM package | install the target version with the package manager and hold the package to stop auto-upgrades |
| WAR + systemd | replace `jenkins.war`, restart; keep the previous WAR for rollback |
| Docker (`jenkins/jenkins:lts-jdk21`) | bump the tag; `JENKINS_HOME` on a named volume; rebuild your derived image with `jenkins-plugin-cli` baked plugins |
| Helm chart | `controller.image.tag` + `controller.installPlugins` list (set `installPlugins: false` when plugins are baked into your image); `helm upgrade` with the same values; the PVC persists; `helm rollback` plus the PVC snapshot taken beforehand |
Pre-upgrade: let running builds finish, snapshot, upgrade. Running Pipelines write state to disk
so they can survive a restart; how much is written depends on the durability setting.

## 6. Rollback
The dependable rollback is "restore the snapshot + previous WAR/image"; take the snapshot
immediately before the upgrade.

## 7. Post-upgrade checks
Manage Jenkins banner (security warnings, deprecated plugins), *System Log* for
errors, agents online, a pipeline per executor type (Docker, Kubernetes, SSH), webhooks
firing, and JCasC still applying without schema errors.

## Verify
- [ ] Quarterly restore drill: a fresh host from backup serves jobs with credentials decrypting and agents connecting.
- [ ] `plugins.txt` and `jenkins.yaml` in Git match what is running (`jenkins-plugin-cli --list`).
- [ ] Staging rehearsal performed before each prod LTS upgrade; results noted in the change ticket.
- [ ] Snapshot taken immediately before every upgrade.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: backup guide (config files, `jobs` layout, what may be skipped, `master.key` handling, thinBackup, restore-validation method); Java support policy table (Java 21 and 25 supported, 17 and 11 unsupported); jenkins/docker image tag `lts-jdk21`; plugin-installation-manager-tool `--available-updates`, `--output txt`, `--jenkins-version`, `--plugin-file`; Helm chart `installPlugins` and PVC persistence; Pipeline durability settings. Removed unconfirmed version-specific Java gates, rsync/quietDown recipes, downgrade rules and the health-check metric.
Method: documentation only; no commands were run.
