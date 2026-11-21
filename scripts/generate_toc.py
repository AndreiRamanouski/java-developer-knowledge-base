#!/usr/bin/env python3
"""Regenerate the linked tables of contents in README.md files.

The root README gets a section overview, and each top-level section folder gets a
README.md listing every file. Generated text sits between TOC markers; everything
outside the markers is left alone.

Usage:
    python3 scripts/generate_toc.py          # rewrite READMEs
    python3 scripts/generate_toc.py --check  # exit 1 if any README is out of date
"""
import os
import re
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!-- toc:start -->", "<!-- toc:end -->"

SECTIONS = [
    ("Java", "☕", "Core Java, modern Java features (8 → 25), enterprise Java, specialized topics and interview preparation."),
    ("Spring & Spring Boot", "🌱", "Spring Core, Spring Boot, MVC & REST, data access, security, testing, WebFlux and advanced topics."),
    ("Databases", "🗄️", "PostgreSQL, MySQL and Oracle with Spring Boot, Liquibase and Flyway migrations, and NoSQL stores."),
    ("Message Brokers", "📨", "Apache Kafka and RabbitMQ with Spring Boot: fundamentals, producers and consumers, error handling, reliability and testing."),
    ("CI-CD Docker Kubernetes Helm", "🐳", "Docker, Kubernetes, Helm and CI/CD pipelines for Java applications."),
    ("Git, Maven & Gradle", "🔧", "Git workflows, Maven and Gradle builds."),
]


def sort_key(name):
    """Numbered entries first, in numeric order; 'Summary N.' files after them."""
    m = re.match(r"(\d+)\.", name)
    if m:
        return (0, int(m.group(1)), name.lower())
    m = re.match(r"Summary (\d+)\.", name)
    if m:
        return (2, int(m.group(1)), name.lower())
    return (1, 0, name.lower())


def entries(path):
    names = [n for n in os.listdir(path) if not n.startswith(".") and n != "README.md"]
    dirs = sorted((n for n in names if os.path.isdir(os.path.join(path, n))), key=sort_key)
    files = sorted((n for n in names if n.endswith(".md")), key=sort_key)
    return dirs, files


def link(text, rel):
    return f"[{text}]({quote(rel)})"


def tree(path, base, depth):
    """Nested bullet list for everything under `path`, links relative to `base`."""
    lines = []
    dirs, files = entries(path)
    indent = "  " * depth
    for f in files:
        lines.append(f"{indent}- {link(f[:-3], os.path.relpath(os.path.join(path, f), base))}")
    for d in dirs:
        lines.append(f"{indent}- **{link(d, os.path.relpath(os.path.join(path, d), base))}**")
        lines.extend(tree(os.path.join(path, d), base, depth + 1))
    return lines


def section_toc(section):
    base = os.path.join(ROOT, section)
    out = []
    dirs, files = entries(base)
    for d in dirs:
        out += ["", f"### {link(d, d)}", ""]
        out += tree(os.path.join(base, d), base, 0)
    if files:
        out += ["", "### Other", ""]
        out += [f"- {link(f[:-3], f)}" for f in files]
    return out[1:]


def root_toc():
    out = []
    for section, icon, blurb in SECTIONS:
        out += ["", f"### {icon} {link(section, section + '/README.md')}", "", blurb, ""]
        dirs, _ = entries(os.path.join(ROOT, section))
        out += [f"{i}. {link(re.sub(r'^\d+\.\s*', '', d), section + '/' + d)}" for i, d in enumerate(dirs, 1)]
    return out[1:]


def replace_block(text, block):
    body = "\n".join([START, *block, END])
    if START in text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: body, text, flags=re.S)
    return text.rstrip("\n") + "\n\n## Contents\n\n" + body + "\n"


def main():
    check = "--check" in sys.argv
    targets = {os.path.join(ROOT, "README.md"): root_toc()}
    for section, _, blurb in SECTIONS:
        targets[os.path.join(ROOT, section, "README.md")] = section_toc(section)

    stale = []
    for path, block in targets.items():
        if os.path.exists(path):
            old = open(path, encoding="utf-8").read()
        else:
            title = os.path.basename(os.path.dirname(path))
            blurb = next(b for s, _, b in SECTIONS if s == title)
            old = f"# {title}\n\n{blurb}\n\n[← Back to the main README](../README.md)\n"
        new = replace_block(old, block)
        if not new.endswith("\n"):
            new += "\n"
        if new != (open(path, encoding="utf-8").read() if os.path.exists(path) else None):
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)

    if check and stale:
        print("Tables of contents are out of date. Run: python3 scripts/generate_toc.py")
        print("\n".join(f"  {p}" for p in stale))
        sys.exit(1)
    if not check:
        print("Updated: " + (", ".join(stale) if stale else "nothing"))


if __name__ == "__main__":
    main()
