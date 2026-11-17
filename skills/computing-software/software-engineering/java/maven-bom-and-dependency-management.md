---
id: computing-software.software-engineering.java.maven-bom-and-dependency-management
name: maven-bom-and-dependency-management
category: computing-software
field: software-engineering
product: java
tags: [java, java-build, maven, maven-bom, dependency-mediation, dependency-management, version-conflicts]
level: practitioner
status: docs-checked
description: "Control transitive dependency versions in Maven: dependencyManagement, importing BOMs, nearest-wins mediation, exclusions, convergence checks and diagnosing conflicts."
sources:
  - https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html
  - https://maven.apache.org/enforcer/enforcer-rules/dependencyConvergence.html
  - https://docs.spring.io/spring-boot/maven-plugin/using.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maven BOMs and dependency management

**Goal:** one version of each library on the classpath, chosen deliberately, not by accident of declaration order.

## 1. Mediation rules
- **Nearest wins**: the version closest to your project in the dependency tree is used; ties go to the first declared.
- Direct dependencies beat transitive ones.
- `dependencyManagement` overrides versions of transitive dependencies too, wherever they appear.
So adding an unrelated library can silently downgrade Jackson via a shorter path.

## 2. Central versions with dependencyManagement
```xml
<dependencyManagement>
  <dependencies>
    <dependency>                         <!-- import a BOM: all its managed versions -->
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-dependencies</artifactId>
      <version>${spring-boot.version}</version>
      <type>pom</type><scope>import</scope>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson</groupId><artifactId>jackson-bom</artifactId>
      <version>${jackson.version}</version><type>pom</type><scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
<dependencies>
  <dependency><groupId>com.fasterxml.jackson.core</groupId><artifactId>jackson-databind</artifactId></dependency>
</dependencies>
```
BOM order can matter when two BOMs manage the same artifact: put the BOM you want to win first, or set an explicit version in your own `dependencyManagement` (see "Importing Dependencies" in the Maven guide).

## 3. Publish your own BOM
For a multi-module library, a `-bom` module with `<packaging>pom</packaging>` listing all modules lets consumers align versions with one import.

## 4. Diagnose
```bash
./mvnw dependency:tree -Dverbose -Dincludes=org.slf4j       # shows "omitted for conflict with"
./mvnw dependency:analyze                                   # used-undeclared / declared-unused
./mvnw versions:display-dependency-updates
```
Enforcer `dependencyConvergence` fails the build when transitive versions disagree; `requireUpperBoundDeps` when the resolved version is lower than one requested.

## 5. Exclusions and scopes
```xml
<dependency>
  <groupId>org.apache.hadoop</groupId><artifactId>hadoop-client</artifactId>
  <exclusions><exclusion><groupId>log4j</groupId><artifactId>log4j</artifactId></exclusion></exclusions>
</dependency>
```
Scopes: `compile` (default), `provided` (container supplies; not packaged), `runtime` (JDBC drivers), `test`, `import` (BOMs only). `<optional>true</optional>` stops propagation to consumers.

## Gotchas
- Runtime `NoSuchMethodError`/`ClassNotFoundException` after an upgrade usually means mediation picked an old transitive version; check the tree.
- Properties used in `dependencyManagement` of an imported BOM cannot be overridden by the importer unless the BOM is your parent (Spring Boot parent vs BOM import difference).
- Do not declare versions in child modules when the parent manages them; drift starts there.

## Verify
- `dependency:tree` shows a single version per artifact for critical libraries and the enforcer convergence rule passes in CI.

## Checked

- Date: 2026-10-28
- Confirmed on maven.apache.org (dependency mechanism guide, dependencyConvergence and requireUpperBoundDeps enforcer rules, dependency:tree verbose, dependency:analyze, versions:display-dependency-updates) and the Spring Boot Maven plugin page: nearest definition wins, first declaration wins on ties, dependencyManagement, exclusions, optional, import scope.
- Removed: pinned example versions (now properties), BOM-order guarantee that the guide does not state.
Method: documentation only; no commands were run.
