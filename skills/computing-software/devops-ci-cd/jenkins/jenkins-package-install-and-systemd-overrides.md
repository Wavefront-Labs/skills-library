---
id: computing-software.devops-ci-cd.jenkins.jenkins-package-install-and-systemd-overrides
name: jenkins-package-install-and-systemd-overrides
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jenkins-systemd, jenkins-upgrade, jvm-tuning]
level: practitioner
status: docs-checked
description: "Install Jenkins LTS from apt/dnf repos and manage it with systemd: override JAVA_OPTS and JENKINS_OPTS through a drop-in that survives package upgrades."
sources: ["https://www.jenkins.io/doc/book/installing/linux/", "https://www.jenkins.io/doc/book/system-administration/systemd-services/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package installs and systemd overrides

## Install LTS (Debian/Ubuntu)
```bash
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" |
  sudo tee /etc/apt/sources.list.d/jenkins.list
sudo apt-get update && sudo apt-get install -y fontconfig openjdk-21-jre jenkins
```
RHEL family: add the repo from `https://pkg.jenkins.io/rpm-stable/jenkins.repo`, then install `fontconfig`, `java-21-openjdk`
and `jenkins` with `dnf`. Follow the install page for the current key and Java version.

## Configure with a drop-in
From Jenkins 2.332.1 and 2.335 the Linux packages use systemd, and the installers migrate old System V settings into systemd
overrides. Customise through the drop-in, never the read-only main unit.
```bash
sudo systemctl edit jenkins
```
```ini
[Service]
Environment="JAVA_OPTS=-Djava.awt.headless=true -XX:+UseStringDeduplication"
Environment="JENKINS_OPTS=--prefix=/jenkins"
```
- Customisations must be in a `[Service]` section. The file is `/etc/systemd/system/jenkins.service.d/override.conf` and is
  not overwritten on upgrade.
- `systemctl edit` reloads systemd for you; if you edit the file by hand, run `systemctl daemon-reload`. Settings apply at
  the next restart.
- The drop-in holds only customisations, not defaults; use `systemctl cat jenkins` to see the unit and drop-in together.
- Migration creates the drop-in with 0600 permissions, `systemctl edit` with 0644. Set 0600 if it holds keystore passwords.
- Full option list for `JENKINS_OPTS`: `java -jar jenkins.war --help`.

## Operations
- Logs: `journalctl -u jenkins`.
- Slow startup with many jobs: Jenkins extends the start timeout at each initialisation milestone; the base timeout is the
  `TimeoutStartSec` directive of the unit.
- Back up JENKINS_HOME before upgrading.

## Verify
- [ ] `systemctl status jenkins` lists `override.conf` under Drop-In.

## Checked
2026-11-01. Confirmed against the Jenkins "Linux" install page and "Managing systemd services" page: apt and dnf repo URLs,
signing key file, Java 21 packages, systemd migration versions, drop-in path and permissions, `daemon-reload` behaviour,
`JAVA_OPTS`/`JENKINS_OPTS` examples, `journalctl -u jenkins`, `TimeoutStartSec`. Removed: ignored-defaults-file claim, port and
home environment variables, `LimitNOFILE`, heap sizes, package hold and upgrade commands, key rotation claim, `/manage/systemInfo`.
Method: documentation only; no commands were run.
