#!/usr/bin/env python3
"""Fail if any relative Markdown link points to a file or folder that doesn't exist.

External links (http, https, mailto) are not checked here; links inside code blocks
and inline code are ignored.

Usage: python3 scripts/check_links.py
"""
import os
import re
import sys
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# [text](target) where target may contain one level of balanced parentheses
LINK = re.compile(r"!?\[[^\]]*\]\(((?:[^()\s]|\([^()\s]*\))+)\)")
SKIP_DIRS = {".git", ".idea", "node_modules"}


def strip_code(text):
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", "", text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", "", text)


def main():
    broken = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            text = strip_code(open(path, encoding="utf-8").read())
            for target in LINK.findall(text):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                    continue
                file_part = unquote(target.split("#", 1)[0])
                if not file_part:
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(dirpath, file_part))):
                    broken.append((os.path.relpath(path, ROOT), target))

    for src, target in broken:
        print(f"{src}: broken link -> {target}")
    if broken:
        print(f"\n{len(broken)} broken link(s).")
        sys.exit(1)
    print("All relative links resolve.")


if __name__ == "__main__":
    main()
