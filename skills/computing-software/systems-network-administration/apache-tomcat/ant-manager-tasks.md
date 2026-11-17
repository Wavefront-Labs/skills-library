---
id: computing-software.systems-network-administration.apache-tomcat.ant-manager-tasks
name: ant-manager-tasks
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, ant, catalina-tasks, manager-script, deploy-task, build-xml, ci-deploy]
level: intro
status: docs-checked
description: "Deploy to Tomcat 10.1 from an Ant build using catalina-tasks.xml: import, task parameters, manager-script credentials and keeping the password off the file."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/manager-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ant tasks for the Manager

Requirements: Ant 1.4 or later (1.6.2 or later for output capture), and a user in your Tomcat user database with the `manager-script` role. The `url` in the page's example is `http://localhost:8080/manager/text`.

Import the task definitions in `build.xml`:
```xml
<import file="${catalina.home}/bin/catalina-tasks.xml"/>
```
The page shows the tasks `deploy`, `reload`, `undeploy` and `list`, with attributes such as `url`, `username`, `password`, `path`, and for `deploy` `war` (for example `file:` URL of the WAR), `config` and `update`.

Values are replaceable properties. To keep the manager password out of the build file, omit the `password` property and pass it on the command line (`ant -Dpassword=<PASSWORD> deploy`), with `password="${password}"` in the task.

Output capture (Ant 1.6.2 or later): the tasks support `output`, `error`, `logError`, `append`, `createemptyfiles`, `outputproperty` and `errorproperty` from Ant's `<redirector>`, plus `alwaysLog` and `failonerror` (default true; set false to capture error output).

Note: the `resources` task defined by the import overrides the `resources` datatype added in Ant 1.7; to keep that datatype, use Ant's namespace support to modify `catalina-tasks.xml` so the Tomcat tasks have their own namespace.

For non-Ant pipelines use the curl forms in `computing-software.systems-network-administration.apache-tomcat.manager-text-interface-deploy`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Manager how-to (Executing Manager Commands With Ant, Tasks output capture). Corrected the per-task attribute list and the namespace note; removed the generic verify line.

Method: documentation only; no commands were run.
