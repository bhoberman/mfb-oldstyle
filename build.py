#!/usr/bin/env python3
"""Build the MFB Oldstyle fonts from the Glyphs sources.

Requires fontmake:  pip install fontmake
Usage:              python build.py
Output:             fonts/MFBOldstyle-{Regular,Bold,Italic}.{otf,ttf}
                    fonts/MFBOldstyle-otf.zip, fonts/MFBOldstyle-ttf.zip
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from fontmake.font_project import FontProject

OUT = Path("fonts")

# Regular has no instances in its source, so it is built from the master.
# Bold and Italic are built from their instances, which carry the
# style-linking and weight settings.
BUILDS = [
    ("glyphs3/MFB Oldstyle-Regular.glyphs", False),
    ("glyphs3/MFB Oldstyle-Bold.glyphs", True),
    ("glyphs3/MFB Oldstyle-Italic.glyphs", True),
]

project = FontProject()
for source, from_instances in BUILDS:
    print(f"Building {source}")
    project.run_from_glyphs(
        source, output=("otf", "ttf"), interpolate=from_instances, output_dir=OUT
    )

# One archive per format, each including the license.
for ext in ("otf", "ttf"):
    archive = OUT / f"MFBOldstyle-{ext}.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as z:
        for font in sorted(OUT.glob(f"*.{ext}")):
            z.write(font, font.name)
        z.write("COPYING", "COPYING")
    print(f"Wrote {archive}")

