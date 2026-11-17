---
id: computing-software.software-engineering.pydantic.validate-data-files
name: validate-data-files
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-file-validation, json, jsonl, csv, toml, yaml, typeadapter]
level: practitioner
status: docs-checked
description: "Validate JSON, JSON lines, CSV, TOML, YAML, XML and INI files with Pydantic using model_validate_json, model_validate and TypeAdapter(list[Model])."
sources:
  - https://docs.pydantic.dev/latest/examples/files/
  - https://docs.pydantic.dev/latest/install/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: load a file with the right parser, then validate with a model. The page's model throughout:
```python
from pydantic import BaseModel, EmailStr, PositiveInt

class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr
```
If validation fails, Pydantic raises a `ValidationError` listing all problems; the page's bad `.json` (age -30, bad email, missing name) gives `3 validation errors for Person` with types `missing`, `greater_than` and a `value_error` for the email. For unattended pipelines, the error's `loc` gives the failing record's index. For configuration/settings files, the page suggests `pydantic-settings`, which has built-in support.

## JSON
```python
import pathlib
person = Person.model_validate_json(pathlib.Path('person.json').read_text())
```
A file holding a list of people: use `TypeAdapter`.
```python
from pydantic import TypeAdapter
person_list_adapter = TypeAdapter(list[Person])
people = person_list_adapter.validate_json(pathlib.Path('people.json').read_text())
```

## JSON lines (.jsonl)
```python
json_lines = pathlib.Path('people.jsonl').read_text().splitlines()
people = [Person.model_validate_json(line) for line in json_lines]
```

## CSV
Use the standard `csv` module and validate each row dict:
```python
import csv
with open('people.csv') as f:
    reader = csv.DictReader(f)
    people = [Person.model_validate(row) for row in reader]
```

## TOML
```python
import tomllib
with open('person.toml', 'rb') as f:
    data = tomllib.load(f)
person = Person.model_validate(data)
```

## YAML (PyYAML)
```python
import yaml
with open('person.yaml') as f:
    data = yaml.safe_load(f)
person = Person.model_validate(data)
```

## XML
```python
import xml.etree.ElementTree as ET
tree = ET.parse('person.xml').getroot()
data = {child.tag: child.text for child in tree}
person = Person.model_validate(data)
```

## INI
```python
import configparser
config = configparser.ConfigParser()
config.read('person.ini')
person = Person.model_validate(config['PERSON'])
```

`EmailStr` needs the `email` extra (`pip install 'pydantic[email]'`, see install page). The single-record snippets print `name='John Doe' age=30 email='john@example.com'` for the page's sample data; the list, JSON lines and CSV snippets print a list of `Person` objects.

## Checked

Checked 2026-11-07. Re-read examples/files in full. For the install page, read only the extras section that covers pydantic[email]. Corrected the closing sentence, which said every snippet prints a single Person, to say that only the single-record snippets do.

Method: documentation only; no commands were run.
