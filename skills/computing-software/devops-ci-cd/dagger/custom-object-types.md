---
id: computing-software.devops-ci-cd.dagger.custom-object-types
name: custom-object-types
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, custom-types, objects, modules, fields]
level: practitioner
status: docs-checked
description: "Define custom object types in a Dagger module (Go struct, Python object_type, TypeScript class or type), expose fields and methods, and call them by chaining."
sources: [https://docs.dagger.io/0.21/extending/modules/custom-types]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom object types

Goal: return structured data from a Function (Dagger 0.21 docs). A module can define many object types, but they are reachable only by chaining from a function on the main object.

## Example: a `github` module

Go: structs with public fields; methods on a type become functions on it.

```go
func (module *MyModule) DaggerOrganization() *Organization {
	url := "https://github.com/dagger"
	return &Organization{
		URL:          url,
		Repositories: []*dagger.GitRepository{dag.Git(url + "/dagger")},
		Members:      []*Account{{"jane", "jane@example.com"}, {"john", "john@example.com"}},
	}
}

type Organization struct {
	URL          string
	Repositories []*dagger.GitRepository
	Members      []*Account
}

type Account struct {
	Username string
	Email    string
}

func (account *Account) URL() string { return "https://github.com/" + account.Username }
```

Python: decorate with `@object_type`; use `field()` descriptors for attributes (they expose argument-less getter functions) and `@function` for methods:

```python
@object_type
class Account:
    username: str = field()
    email: str = field()

    @function
    def url(self) -> str:
        return f"https://github.com/{self.username}"
```

TypeScript: `@object()` classes with `@func()` fields/methods and an explicit constructor. For a data-only shape use `export type Organization = { url: string; repositories: GitRepository[]; members: Account[] }` (no constructor boilerplate). Rule from the page: use a `class` when you need methods and privacy, `type` for plain public data.

## Calling

```shell
dagger call dagger-organization members url
dagger -c 'dagger-organization | members | url'
```

Output: `https://github.com/jane` and `https://github.com/john`.

## Gotcha: type names are prefixed

The engine prefixes custom type names with the main object name when extending the API schema: `Github`, `GithubAccount`, `GithubOrganization`. This avoids conflicts across modules and shows up in generated code when the module is used as a dependency.

## Related

computing-software.devops-ci-cd.dagger.module-constructors

## Checked

2026-11-07

Read in full from the docs source: extending/modules/custom-types.mdx and its snippets. Every claim and snippet matched. No corrections needed.

Method: documentation only; no commands were run.
