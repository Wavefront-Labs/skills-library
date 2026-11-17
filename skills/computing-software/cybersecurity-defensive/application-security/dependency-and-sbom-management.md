---
id: computing-software.cybersecurity-defensive.application-security.dependency-and-sbom-management
name: dependency-and-sbom-management
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [sca, software-composition-analysis, sbom, software-bill-of-materials, dependency-scanning, transitive-dependencies, supply-chain-security, lockfile, vulnerable-and-outdated-components, owasp-cheat-sheets]
level: advanced
status: docs-checked
description: "Manage open-source dependency risk: inventory with SBOMs, monitor for known vulnerabilities, pin versions, and choose a response when a dependency is vulnerable."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html", "https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Dependency and SBOM management — know what is in the build

**Goal:** know which direct and transitive components you ship, be told when one is
vulnerable, and have a defined response for each situation.

## 1. Inventory
- Dependencies are one of the leading risks of modern applications; insight into them is
  the crucial first step. SBOMs can provide it, and both producing and consuming them
  should be automated, preferably in CI/CD.
- Keep inventories beyond language packages: the Supply Chain cheat sheet lists code
  dependencies, container images, web servers and operating system components as things
  to monitor after deployment, and asks for an automatically collected inventory of build
  tools, versions and plugins.
- Lockfiles (for example `package-lock.json`) limit dependencies to a specific version
  previously verified as legitimate and secure, reducing the chance of a compromised or
  vulnerable version being pulled in unnoticed.

## 2. Monitor for known vulnerabilities
- Start automated dependency analysis at the beginning of the project: adding it late can
  produce a large backlog that blocks progress.
- Automate monitoring with tools such as OWASP Dependency-Check or retire.js, and watch
  sources such as the NVD or the CISA KEV catalog.
- The Vulnerable Dependency Management cheat sheet lists, among tools: Dependency-Check
  (full support Java and .NET, experimental for several others), npm audit, OWASP
  Dependency-Track (manages vulnerable dependencies across an organisation), Trivy, Grype,
  Snyk, JFrog Xray and Renovate (detects old dependencies).
- Choose tools that use several reliable input sources (a researcher may use responsible
  or full disclosure, and full-disclosure issues may have no CVE) and that let you flag
  false positives.

## 3. Choose the response case (Vulnerable Dependency Management cheat sheet)
If the vulnerable component is transitive, act on the direct dependency that brings it
in: changing a transitive dependency directly often hurts stability and needs a full
understanding of the chain.
1. **Patched version released:** upgrade in a test environment and run the tests; fix
   code for API changes; if the fix cannot be adopted, see case 5 (use case 2 meanwhile).
2. **Fix months away:** apply any provider workaround, or limit reachable calls to the
   affected functions (a wrapper only if its checks block the exploit conditions on every
   call path, otherwise disable or isolate the functionality). Use a provider exploit as a
   regression test, keep the permanent fix on the plan, note the CVE in the README, and
   scope any scanner ignore to that CVE only.
3. **Provider will not fix:** last resort. Look for a better-maintained component, press a
   commercial provider with the Chief Risk Officer, or patch it yourself (and submit
   upstream if open source). A reproducing test must fail on the unpatched and pass on the
   patched dependency; silencing the scanner is not a fix.
4. **Found by full disclosure or pentest:** tell the provider; apply case 2 if they
   cooperate, otherwise case 3.
5. **Fix exists but cannot be adopted** (breaking major version, transitive pin,
   unmaintained version line): backport the upstream fix, verify it as in case 3,
   distribute the patched artefact through the internal registry or proxy with traceable
   versioning and provenance, and re-test the blocker at each dependency review so you can
   return to case 1.
- Accepting the risk is for the Chief Risk Officer (fallback CISO) on technical feedback
  from the development team and the CVSS score.

## 4. Supplier and supply-chain controls (Supply Chain cheat sheet)
- Assess suppliers before adoption. For open source ask: actively maintained, popular,
  mature, a release version, enough maintainers, keeps its own dependencies updated,
  security-relevant tests, secure-use documentation, a vulnerability reporting process,
  and a licence consistent with your intended usage. Certifications are a data point, not
  a sole basis.
- A private artefact repository increases control; artefacts must be reviewed before entry
  and the repository must not be bypassable.
- SAST can also be applied to open-source components, with manual verification of results.
- Scan the final build binary to detect exposed secrets or unauthorised components.

## Verify
- [ ] An inventory (SBOM or equivalent) is produced automatically and covers more than
  top-level language packages.
- [ ] Dependencies are pinned through lockfiles; version bumps are reviewed.
- [ ] Automated vulnerability monitoring runs and false positives can be flagged per CVE.
- [ ] Each open finding has a response case, an owner and, where accepted, a risk-owner
  decision.

Related: computing-software.cybersecurity-defensive.application-security.sast-dast-pipeline-integration,
computing-software.cybersecurity-defensive.application-security.secure-code-review,
computing-software.cybersecurity-defensive.vulnerability-management.patch-management-coordination

## Checked
Method: docs-checked 2026-11-09 against the OWASP Vulnerable Dependency Management Cheat Sheet and the OWASP Software Supply Chain Security Cheat Sheet (both read in full). Removed as unconfirmed: NTIA minimum elements and NIST SSDF attributions, CycloneDX/SPDX format claims, Log4Shell-specific response procedure, typosquat and registry-reputation guidance, endoflife.date and Scorecard advice, license-compliance single-SBOM claim, vendored-code blind-spot gotcha, and the OWASP A06 page (it returned no content).
