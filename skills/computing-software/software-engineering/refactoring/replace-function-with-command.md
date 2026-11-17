---
id: computing-software.software-engineering.refactoring.replace-function-with-command
name: replace-function-with-command
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-apis, replace-function-with-command, replace-command-with-function, method-object, command-pattern, fowler-catalog]
level: practitioner
status: draft
description: "Replace Function with Command (method object) to break up a large function with many locals or add undo/queueing, and the inverse when the command adds no value."
sources:
  - https://refactoring.com/catalog/replaceFunctionWithCommand.html
  - https://refactoring.com/catalog/replaceCommandWithFunction.html
  - https://refactoring.guru/replace-method-with-method-object
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replace Function with Command / Replace Command with Function

## Replace Function with Command (a.k.a. method object)
**When:** a long function whose locals are so entangled that Extract Function would need to pass half a dozen parameters each time; or the operation needs undo, queueing, lifecycle hooks, or step-by-step customisation via subclassing.
```javascript
function score(candidate, medicalExam, scoringGuide) {
  let result = 0, healthLevel = 0, highMedicalRiskFlag = false;
  // ... 60 lines touching all of these
}
// after
class Scorer {
  constructor(candidate, medicalExam, scoringGuide) { Object.assign(this, {candidate, medicalExam, scoringGuide}); }
  execute() {
    this._result = 0; this._healthLevel = 0; this._highMedicalRiskFlag = false;
    this.scoreSmoking();         // extracted freely: locals are now fields
    return this._result;
  }
  scoreSmoking() { ... }
}
function score(candidate, medicalExam, scoringGuide) { return new Scorer(candidate, medicalExam, scoringGuide).execute(); }
```
Mechanics:
1. Create an empty class named after the function.
2. Move the function into it as `execute()` (or `call`, `run`); keep the original as a forwarding function.
3. Make each argument a constructor field (or keep as `execute` arguments).
4. Convert locals into fields one at a time; test.
5. Now extract methods freely - no parameter passing needed.

## Replace Command with Function
**When:** the command is a few lines, has no undo, no queueing, no subclass variation - just a function wearing a class costume (`new PriceCalculator(order).calculate()`).
Mechanics: Extract Function on the construction-plus-execute call, inline the command's helper methods into `execute`, move constructor parameters to the function's parameters, delete the class.

## Notes
- Commands are single-use: create, execute, discard. Do not reuse an instance across calls (fields carry state from the previous run).
- The command style in CQRS (serialisable command + handler) is a different, architectural use; see the command pattern skill.

## Verify
- [ ] Original function signature unchanged during the refactoring; callers untouched until the end.
- [ ] Each converted local is a separate test-green step.
