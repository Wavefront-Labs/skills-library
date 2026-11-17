---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.writing-autopsy-python-ingest-modules
name: writing-autopsy-python-ingest-modules
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [autopsy-python-module, autopsy, ingest-modules, jython, dfir]
level: advanced
status: draft
description: "Write Autopsy Python (Jython) ingest modules: file vs data source modules, finding files, posting blackboard artifacts and attributes, and testing."
sources: ["https://github.com/sleuthkit/autopsy/tree/develop/pythonExamples"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing Autopsy Python ingest modules

**Goal:** automate a case-specific parser (a proprietary app database, a log format) inside
Autopsy so results appear in the tree, timeline and reports like built-in artefacts.

## Module types
- **File ingest module**: `process(self, file)` called for every file in the data source (after
  file type ID, hashing). Good for per-file checks.
- **Data source ingest module**: `process(self, dataSource, progressBar)` called once; you query
  for specific files with `FileManager.findFiles`. Best for parsing known artefact paths.

## Skeleton (data source module)
```python
from org.sleuthkit.autopsy.ingest import IngestModuleFactoryAdapter, DataSourceIngestModule, IngestModule
from org.sleuthkit.autopsy.casemodule import Case
from org.sleuthkit.datamodel import BlackboardArtifact, BlackboardAttribute
from java.util import ArrayList

class MyFactory(IngestModuleFactoryAdapter):
    moduleName = "Case App Parser"
    def getModuleDisplayName(self): return self.moduleName
    def isDataSourceIngestModuleFactory(self): return True
    def createDataSourceIngestModule(self, settings): return MyModule()

class MyModule(DataSourceIngestModule):
    def startUp(self, context): self.context = context
    def process(self, dataSource, progressBar):
        fm = Case.getCurrentCase().getServices().getFileManager()
        bb = Case.getCurrentCase().getSleuthkitCase().getBlackboard()
        for f in fm.findFiles(dataSource, "app.db", "AppData/Local/Vendor"):
            # copy to temp (ContentUtils.writeToFile), open with JDBC SQLite, then for each row:
            attrs = ArrayList()
            attrs.add(BlackboardAttribute(BlackboardAttribute.Type.TSK_URL, MyFactory.moduleName, "https://..."))
            attrs.add(BlackboardAttribute(BlackboardAttribute.Type.TSK_DATETIME_ACCESSED, MyFactory.moduleName, 1696000000))
            art = f.newDataArtifact(BlackboardArtifact.Type.TSK_WEB_HISTORY, attrs)
            bb.postArtifact(art, MyFactory.moduleName, self.context.getJobId())
        return IngestModule.ProcessResult.OK
```
Use custom artifact types (`bb.getOrAddArtifactType`) for data that fits no standard type.

## Install and test
- Place the `.py` in a folder under Autopsy's python modules directory (Tools > Python Plugins opens it); restart or re-run ingest.
- Test on a small image with known content; check Autopsy logs (`autopsy.log.0`) for Jython stack traces.

## Gotchas
- Jython is Python 2.7 syntax with Java libraries; no CPython C extensions (use JDBC for SQLite).
- Check `self.context.isJobCancelled()` in loops to support cancellation.
- APIs change between Autopsy versions (e.g. `newDataArtifact` in 4.19+); use the examples matching your version.

## Verify
Artifacts appear under Data Artifacts with correct attributes and times on a test image with known values.
