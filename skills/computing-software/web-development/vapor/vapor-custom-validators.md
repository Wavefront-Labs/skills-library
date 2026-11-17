---
id: computing-software.web-development.vapor.vapor-custom-validators
name: vapor-custom-validators
category: computing-software
field: web-development
product: vapor
tags: [vapor,validators,validatable,custom-validator,validation,swift,zip-code]
level: advanced
status: docs-checked
description: "Write custom Vapor validators by extending the Validation API (ValidatorResult, Validator extension) or using the one-off .custom validator."
sources:
  - https://docs.vapor.codes/basics/validation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add validation rules beyond the built-ins, either reusable across Content types or local to one.

## Option 1: extend the Validation API (reusable)
Best when several Content types use the rule. Example: zip code.
```swift
extension ValidatorResults {
    public struct ZipCode {
        public let isValidZipCode: Bool
    }
}

extension ValidatorResults.ZipCode: ValidatorResult {
    public var isFailure: Bool { !self.isValidZipCode }
    public var successDescription: String? { "is a valid zip code" }
    public var failureDescription: String? { "is not a valid zip code" }
}

private let zipCodeRegex: String = "^\\d{5}(?:[-\\s]\\d{4})?$"

extension Validator where T == String {
    public static var zipCode: Validator<T> {
        .init { input in
            guard let range = input.range(of: zipCodeRegex, options: [.regularExpression]),
                  range.lowerBound == input.startIndex && range.upperBound == input.endIndex
            else {
                return ValidatorResults.ZipCode(isValidZipCode: false)
            }
            return ValidatorResults.ZipCode(isValidZipCode: true)
        }
    }
}
```
Use it: `validations.add("zipCode", as: String.self, is: .zipCode)`.

## Option 2: `.custom` validator (one-off)
Best for a property in a single Content type: simpler logic and shorter syntax. Pass a description and a closure returning Bool, inside the type's `validations(_:)`:
```swift
validations.add("nameAndSurname", as: String.self,
    is: .custom("Validates whether employee is part of XYZ company by looking at name and surname.") { nameAndSurname in
        allCompanyEmployees.contains(nameAndSurname)
    })
```
(The docs write the closure as a loop over the list returning true or false; any Bool-returning closure fits.)

Override default messages with the `customFailureDescription:` parameter of `validations.add`.

Related: computing-software.web-development.vapor.vapor-validation-validatable

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) basics/validation, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
