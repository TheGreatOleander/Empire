#!/bin/bash

# Directory for the zip contents
WORK_DIR="CodeSync-Bridge-v2.1"
ZIP_FILE="CodeSync-Bridge-v2.1.zip"

# Clean up previous build if it exists
if [ -d "$WORK_DIR" ]; then
  rm -rf "$WORK_DIR"
fi
mkdir -p "$WORK_DIR"

# Copy or create files
cat > "$WORK_DIR/README.md" << 'EOF'
# CodeSync: XDA-GitHub Bridge
![Build Status](https://github.com/CodeSync-Bridge/CodeSync-Bridge/actions/workflows/build.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue)
[![If you like, spark me some ETH!](https://img.shields.io/badge/If%20you%20like,%20spark%20me%20some%20ETH!-Donate%20ETH-orange?logo=ethereum)](https://sendeth2.me/0xd0e9B76Eb4B3911281161CF891E3B03DAa77c74b)

A revolutionary tool to unify Android devs. Create Magisk module repos and XDA posts in one shot, then walk away as the community ignites.

## Manifesto
CodeSync is the spark for Android’s open-source soul. Drop this seed, watch it grow, and transcend the grind. Unify XDA and GitHub—hack, share, vanish!
EOF

cat > "$WORK_DIR/LICENSE" << 'EOF'
MIT License

Copyright (c) 2025 CodeSync-Bridge

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

cat > "$WORK_DIR/requirements.txt" << 'EOF'
PyGithub==1.59
pytest==7.4.0
gitpython==3.1.40
requests==2.31.0
EOF

cat > "$WORK_DIR/setup.sh" << 'EOF'
#!/bin/bash
echo "Setting up CodeSync environment..."
pip install -r requirements.txt
echo "Setup complete!"
EOF
chmod +x "$WORK_DIR/setup.sh"

cat > "$WORK_DIR/bridge_script.py" << 'EOF'
#!/usr/bin/env python3

import os
import sys
import zipfile
import argparse
import requests
from datetime import datetime

# GitHub API token (set via environment or prompt)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", input("Enter GitHub token (repo scope): ").strip())

# Constants
MODULE_DIR = "module"
XDA_POST_FILE = "output/xda_post.txt"
MODULE_PROP = """id=CodeSync
version=v2.1
name=CodeSync Bridge
author=Yodazballs
description=Unifies XDA and GitHub for Magisk module dev"""

def setup_parser():
    parser = argparse.ArgumentParser(description="CodeSync: XDA-GitHub Bridge")
    parser.add_argument("--output-dir", default=MODULE_DIR, help="Output directory for module")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without changes")
    parser.add_argument("--config", help="Config file path")
    parser.add_argument("--quiet", action="store_true", help="Suppress output")
    parser.add_argument("--no-clone", action="store_true", help="Skip Git clone")
    parser.add_argument("--plugin-dir", help="Directory for plugins")
    return parser.parse_args()

def build_magisk_module(output_dir):
    """Build a basic Magisk module structure."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "module.prop"), "w") as f:
            f.write(MODULE_PROP)
        os.makedirs(os.path.join(output_dir, "system"), exist_ok=True)
        with open(os.path.join(output_dir, "system/placeholder"), "w") as f:
            f.write("Placeholder file for Magisk module")
        print(f"Built Magisk module in {output_dir}") if not args.quiet else None
    except Exception as e:
        print(f"Error building module: {e}")
        sys.exit(1)

def zip_module(output_dir):
    """Create a zip file from the module directory."""
    zip_path = f"{output_dir}.zip"
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)
        print(f"Created {zip_path}") if not args.quiet else None
        return zip_path
    except Exception as e:
        print(f"Error zipping module: {e}")
        sys.exit(1)

def generate_xda_post():
    """Generate a basic XDA post (simplified for demo)."""
    os.makedirs("output", exist_ok=True)
    post_content = f"""[SIZE="7"][B]CodeSync: XDA-GitHub Bridge[/B][/SIZE]
[COLOR="Red"]A righteous spark to unify Android’s open-source soul![/COLOR]
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S EDT')} by Yodazballs.
Check [URL="https://github.com/CodeSync-Bridge/CodeSync-Bridge"]GitHub[/URL] for more."""
    with open(XDA_POST_FILE, "w") as f:
        f.write(post_content)
    print(f"Generated XDA post at {XDA_POST_FILE}") if not args.quiet else None

def main():
    global args
    args = setup_parser()

    if not args.dry_run:
        build_magisk_module(args.output_dir)
        zip_module(args.output_dir)
        generate_xda_post()
    else:
        print("Dry run: Simulated module build, zip, and XDA post generation.")

if __name__ == "__main__":
    main()
EOF
chmod +x "$WORK_DIR/bridge_script.py"

cat > "$WORK_DIR/validate.sh" << 'EOF'
#!/bin/bash
echo "Validating CodeSync setup..."
if [ -f setup.sh ]; then
  echo "setup.sh found, passing test"
  exit 0
else
  echo "setup.sh missing, failing test"
  exit 1
fi
EOF
chmod +x "$WORK_DIR/validate.sh"

cat > "$WORK_DIR/customize.sh" << 'EOF'
#!/bin/bash
echo "Customizing module (placeholder)"
exit 0
EOF
chmod +x "$WORK_DIR/customize.sh"

cat > "$WORK_DIR/CHANGELOG.md" << 'EOF'
# Changelog
## v2.1
- Initial release of CodeSync XDA-GitHub Bridge.
EOF

cat > "$WORK_DIR/TUTORIAL.md" << 'EOF'
# CodeSync Tutorial
- Step-by-step setup
- Plugin dev guide
- Troubleshooting tips
- How to extend CodeSync
EOF

# Create .github directories and files
mkdir -p "$WORK_DIR/.github/workflows"
cat > "$WORK_DIR/.github/workflows/build.yml" << 'EOF'
name: Build & Release Magisk Module
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Lint Scripts
      run: shellcheck validate.sh customize.sh
    - name: Run Tests
      run: bash validate.sh
    - name: Build Module with Script
      run: ./bridge_script.py --output-dir module
    - name: Zip Module
      run: zip -r module.zip module/
    - name: Upload Artifact
      uses: actions/upload-artifact@v3
      with:
        name: module
        path: module.zip
  release:
    if: startsWith(github.ref, 'refs/tags/v')
    needs: build
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Download Artifact
      uses: actions/download-artifact@v3
      with:
        name: module
    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: module.zip
        body_path: CHANGELOG.md
EOF

cat > "$WORK_DIR/.github/workflows/issue-bot.yml" << 'EOF'
name: Issue Bot
on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: pip install requests
    - name: Triage Issue
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        ISSUE_NUMBER=$(jq -r .issue.number "$GITHUB_EVENT_PATH")
        ISSUE_TITLE=$(jq -r .issue.title "$GITHUB_EVENT_PATH")
        ISSUE_BODY=$(jq -r .issue.body "$GITHUB_EVENT_PATH")

        COMMENT="Yo, $GITHUB_ACTOR! Thanks for the bug report on CodeSync. 🚀\n\n"
        if [[ -z "$ISSUE_BODY" || "$ISSUE_BODY" == "null" ]]; then
          COMMENT+="Looks like you forgot details—please fill out the bug report template (OS, Python version, logs, etc.). Check TUTORIAL.md for help. ⛑️\n\n"
          COMMENT+="I’ll close this in 3 days if no update. Vanish and fix it! 🔥"
          gh issue comment "$ISSUE_NUMBER" --body "$COMMENT"
          gh issue label "$ISSUE_NUMBER" --add "needs-info"
          gh issue close "$ISSUE_NUMBER" --reason "not_planned" --comment "Auto-closed due to missing info. Reopen with details!"
          sleep 259200  # 3 days in seconds
          gh issue reopen "$ISSUE_NUMBER" --comment "Reopening for review after 3 days—add details or it’s gone again!"
        else
          COMMENT+="Sweet, you’ve got details! I’ve labeled it 'bug' and assigned it to the void. Check TUTORIAL.md or existing issues. Vanish and hack! 🔥"
          gh issue label "$ISSUE_NUMBER" --add "bug"
          gh issue comment "$ISSUE_NUMBER" --body "$COMMENT"
        fi
      shell: bash
EOF

mkdir -p "$WORK_DIR/.github/ISSUE_TEMPLATE"
cat > "$WORK_DIR/.github/ISSUE_TEMPLATE/bug_report.md" << 'EOF'
---
name: Bug Report
about: Create a report to help us improve CodeSync
title: "[BUG] <Brief Description>"
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Run '....'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment (please complete the following information):**
- OS: [e.g., Ubuntu 20.04, Android 12]
- Python Version: [e.g., 3.9]
- CodeSync Version: [e.g., v2.1]

**Additional context**
Add any other context about the problem here (e.g., logs, stack traces).

**Workaround (if any)**
Any temporary fix you’ve found.
EOF

# Create the zip file
zip -r "$ZIP_FILE" "$WORK_DIR"

# Clean up (optional)
# rm -rf "$WORK_DIR"

echo "Created $ZIP_FILE successfully!"
