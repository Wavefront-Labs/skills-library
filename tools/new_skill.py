#!/usr/bin/env python3
"""new_skill - scaffold a skill file at the right path with template frontmatter.
Run: python tools/new_skill.py <category> <field> <product> <name> ["description"]
"""
import sys, json
from datetime import date
from pathlib import Path
from reindex import SKILLS

TEMPLATE = """---
id: {cat}.{field}.{prod}.{name}
name: {name}
category: {cat}
field: {field}
product: {prod}
tags: [{tag_hint}]
level: practitioner
status: draft
description: {desc}   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources: []
licence: Apache-2.0
version: 1
updated: {today}
---

# {name}

<body: the craft / knowledge. Tag generously above so it's findable.>
"""

def main():
    if len(sys.argv) < 5:
        print("usage: new_skill.py <category> <field> <product> <name> [description]")
        sys.exit(2)
    cat, field, prod, name = sys.argv[1:5]
    desc = sys.argv[5] if len(sys.argv) > 5 else "TODO one-line description"
    path = SKILLS / cat / field / prod / f"{name}.md"
    if path.exists():
        print(f"EXISTS: {path}"); sys.exit(1)
    path.parent.mkdir(parents=True, exist_ok=True)
    tag_hint = ", ".join(dict.fromkeys([field, prod]))
    path.write_text(TEMPLATE.format(cat=cat, field=field, prod=prod, name=name,
                                    desc=json.dumps(desc, ensure_ascii=False), tag_hint=tag_hint,
                                    today=date.today().isoformat()), encoding="utf-8", newline="\n")
    print(f"created {path.relative_to(SKILLS.parent)}")
    print("next: fill body + tags, then  python tools/lint.py && python tools/reindex.py")

if __name__ == "__main__":
    main()
