#!/usr/bin/env python3
"""
Seeing and Believing — Toggle System Audit Script
==================================================
Run this any time after adding new content to check for toggle issues.

Usage:
    python3 toggle_audit.py [path-to-curriculum-folder]

If no path is given, defaults to ./curriculum relative to this script.

What it checks:
    1. Box types that have NO panel control → content permanently hidden
    2. Panel items that control NO boxes → dead toggle items
    3. Default states for each toggle type from script.js
    4. Warns if localStorage (vs sessionStorage) is found in script.js
"""

import os
import re
import sys

# ── Configuration ──────────────────────────────────────────────────────────
ALL_TOGGLES    = ['facilitator', 'deepdive', 'cultural', 'nuance', 'pilgrim', 'plain']
IGNORE_CLASSES = {'title', 'highlight', 'plain-box', 'btn'}   # not real toggle box types

def audit(curriculum_dir):
    if not os.path.isdir(curriculum_dir):
        print(f"ERROR: Directory not found: {curriculum_dir}")
        sys.exit(1)

    files = sorted([f for f in os.listdir(curriculum_dir) if f.endswith('.html')])
    script_path = os.path.join(curriculum_dir, 'script.js')

    print(f"\n{'='*60}")
    print(f"  Seeing and Believing — Toggle Audit")
    print(f"  Directory: {curriculum_dir}")
    print(f"  HTML files: {len(files)}")
    print(f"{'='*60}\n")

    # ── 1. Check script.js ─────────────────────────────────────────────────
    print("── script.js ─────────────────────────────────────────────────")
    if not os.path.exists(script_path):
        print("  WARNING: script.js not found!")
    else:
        script = open(script_path).read()

        # Check storage type
        if 'localStorage' in script:
            print("  ⚠️  WARNING: localStorage found in script.js")
            print("       This causes toggle state to persist across visits,")
            print("       silently hiding newly-added content for returning visitors.")
            print("       Fix: replace localStorage with sessionStorage throughout.")
        elif 'sessionStorage' in script:
            print("  ✓  sessionStorage in use (correct — resets each visit)")
        else:
            print("  ?  No storage API found in script.js")

        # Extract defaults
        defaults = re.findall(r"id: 'toggle-([a-z]+)'.*?def: '([01])'", script)
        if defaults:
            print("\n  Toggle defaults:")
            for toggle, default in defaults:
                state = "ON  (visible by default)" if default == '1' else "OFF (hidden by default)"
                print(f"    {toggle:<16} {state}")
        else:
            print("  WARNING: Could not parse toggle defaults from script.js")

    # ── 2. Per-page box/panel audit ────────────────────────────────────────
    print("\n── Per-page audit ────────────────────────────────────────────")

    critical_issues = []
    warnings        = []

    for fname in files:
        path    = os.path.join(curriculum_dir, fname)
        content = open(path).read()

        if 'toggle-panel' not in content:
            continue   # page has no toggle panel; skip

        # Box types actually used in box divs
        box_types = set()
        for cls in re.findall(r'class="([^"]*)"', content):
            for t in re.findall(r'box-([a-z]+)', cls):
                if t not in IGNORE_CLASSES and f'toggle-{t}' in content:
                    box_types.add(t)

        # Toggle items present in the panel
        panel_items = set(re.findall(r'id="toggle-([a-z]+)"', content))

        # CRITICAL: boxes with no panel control → permanently hidden
        uncontrolled = box_types - panel_items
        if uncontrolled:
            critical_issues.append(
                f"  CRITICAL  {fname}\n"
                f"            Box types {sorted(uncontrolled)} have no panel control.\n"
                f"            These boxes are PERMANENTLY HIDDEN (toggle has no UI)."
            )

        # Warning: panel items with no boxes (harmless but noisy UI)
        unused_controls = panel_items - box_types
        if unused_controls:
            warnings.append(
                f"  WARNING   {fname}\n"
                f"            Panel has controls {sorted(unused_controls)}"
                f" but no matching boxes.\n"
                f"            These toggle items do nothing (cosmetic issue only)."
            )

    if critical_issues:
        print(f"\n  {'!'*4} CRITICAL ISSUES — content is permanently hidden {'!'*4}")
        for issue in critical_issues:
            print(issue)
    else:
        print("  ✓  No critical issues — all box types have panel controls")

    if warnings:
        print(f"\n  Warnings ({len(warnings)}):")
        for w in warnings:
            print(w)
    else:
        print("  ✓  No warnings — all panel controls have matching boxes")

    # ── 3. Quick reference ─────────────────────────────────────────────────
    print("\n── Checklist for adding new content ──────────────────────────")
    print("""
  When adding a new box, verify ALL of the following:

  1. CLASS: Does the div have BOTH box-TYPE and toggle-TYPE?
            e.g. class="box box-nuance toggle-nuance"

  2. PANEL: Is id="toggle-TYPE" present in that page's toggle-panel?
            If not, the box is permanently hidden (no UI to show it).

  3. DEFAULT: Is this toggle type set to def:'1' (visible) in script.js?
              Currently only 'facilitator' defaults to OFF (hidden).

  4. STORAGE: Is script.js using sessionStorage (not localStorage)?
              localStorage persists across visits and can hide new content
              for any visitor who previously turned off that toggle type.

  5. TEST: After deploying, verify on the actual hosted URL — not just
           by opening the ZIP locally. Local file:// origins get fresh
           storage each time, masking the bug the hosted site reveals.
""")

    total_issues = len(critical_issues)
    print(f"{'='*60}")
    print(f"  Audit complete. Critical issues: {total_issues}")
    print(f"{'='*60}\n")
    return total_issues


# ── Entry point ────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        # Default: look for 'curriculum' next to this script
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'curriculum')

    issues = audit(folder)
    sys.exit(0 if issues == 0 else 1)
