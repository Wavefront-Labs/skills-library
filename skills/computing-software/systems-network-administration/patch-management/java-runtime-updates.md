---
id: computing-software.systems-network-administration.patch-management.java-runtime-updates
name: java-runtime-updates
category: computing-software
field: systems-network-administration
product: patch-management
tags: [java-updates, openjdk, oracle-java, jre, third-party-patching, patch-management]
level: practitioner
status: docs-checked
description: "Keep Java runtimes patched: quarterly CPU schedule, Oracle licensing traps, OpenJDK distributions, finding every JRE/JDK copy, removing old versions and app-bundled Java."
sources:
  - https://www.oracle.com/security-alerts/
  - https://www.oracle.com/java/technologies/javase/jdk-faqs.html
  - https://adoptium.net/support/
  - https://adoptium.net/installation/windows/
  - https://openjdk.org/projects/jdk-updates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java runtime updates

## Schedule
Oracle Critical Patch Updates are released on the third Tuesday of January, April, July and October (next dates listed by Oracle: 19 January 2027, 20 April 2027, 20 July 2027, 19 October 2027). OpenJDK distributions publish their own releases (Adoptium lists a release schedule on its support page); check each vendor you use for its dates.

## Licensing trap
Per Oracle's Java SE Licensing FAQ (updated 20 October 2026): Oracle JDK 25 and later is under the Oracle No-Fee Terms and Conditions License (free for all users); Oracle JDK 21, 17, 11 and 8 are available to Oracle customers through My Oracle Support and under the OTN licence, which permits personal use, development, testing, prototyping and demonstrating at no cost but not general production use. Check the FAQ and your own licence position. Many organisations use an OpenJDK distribution (for example Temurin) to keep patching without licence risk.

## Find every copy
```powershell
Get-ChildItem -Path $env:ProgramFiles, ${env:ProgramFiles(x86)} -Recurse -Filter java.exe -ErrorAction SilentlyContinue |
  ForEach-Object { [pscustomobject]@{Path=$_.FullName; Ver=$_.VersionInfo.ProductVersion} }
```
```sh
find / -xdev -type f -name java -perm -u+x 2>/dev/null -exec sh -c '"$1" -version 2>&1 | head -1 | sed "s|^|$1: |"' _ {} \;
update-alternatives --list java; rpm -qa '*openjdk*'
```
Apps often bundle their own JRE (`<app>\jre\bin\java.exe`); those are patched by the app vendor, so track them separately.

## Update
- Windows: deploy the distribution's MSI (`msiexec /i <package>.msi ADDLOCAL=FeatureMain,FeatureEnvironment,FeatureJavaHome INSTALLDIR=<path> /quiet`; Adoptium states INSTALLDIR is required with FeatureMain), via your catalog or winget.
- Linux: distro packages (`dnf update java-21-openjdk`) get security fixes in the normal cycle.
- Remove old versions; Oracle's legacy installers left old JREs side by side.

## Gotchas
- Apps pinned to an exact path (e.g. `jre1.8.0_202`) break when the folder changes; use stable paths or `JAVA_HOME`.
- Adoptium's support table (read 2026-10-27) lists Temurin 8 until at least December 2030, 11 and 17 until at least October 2027, 21 until at least December 2029 and 25 until at least September 2031; other vendors differ, and older apps sometimes need specific vendor builds.
- Java Web Start and the browser plugin are legacy; plan to retire apps that still depend on them.

## Verify
Inventory shows only current quarterly update levels per major version; scanner Java findings at zero except vendor-bundled copies with exceptions.

## Checked
Date: 2026-10-27. Documentation: Oracle Critical Patch Update page (third Tuesday of January, April, July, October; upcoming dates), Oracle Java SE Licensing FAQ updated 20 October 2026, Adoptium support page (end-of-availability table) and Adoptium Windows MSI installation page (feature names, INSTALLDIR requirement). Corrected the CPU schedule and licensing summary; removed the unconfirmed employee-metric, winget ID, vendor release-timing and OpenWebStart claims.
Method: documentation only; no commands were run.
