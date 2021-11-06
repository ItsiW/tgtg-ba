#!/bin/python3

import json
import yaml
import glob
from markdown2 import markdown
from jinja2 import FileSystemLoader, Environment
from pathlib import Path
import shutil

print("Starting build of tgtg...")

build_dir = Path(".") / "build"
shutil.rmtree(build_dir, ignore_errors=True)
build_dir.mkdir(exist_ok=True)

env = Environment(loader=FileSystemLoader("html"))
template = env.get_template("template.html")

## map page
with open(build_dir / "index.html", "w") as o:
    o.write(env.get_template("index.html").render())

## error page
with open(build_dir / "error.html", "w") as o:
    o.write(env.get_template("error.html").render())

## place pages
geojson_features = []

def rating_to_text(rating):
    if rating == 0:
        return "Bad"
    elif rating == 1:
        return "Inoffensive"
    elif rating == 2:
        return "Good"
    elif rating == 3:
        return "Phenomenal"
    else:
        raise ValueError("Bad rating")

def format_title(meta):
    return f"{meta['name']} — Tasty vegan food in {meta['area']} — The Good Taste Guide"

def format_description(meta):
    return f"Read our review on {meta['name']} at {meta['address']} in {meta['area']}, and more tasty vegan food in New York City from The Good Taste Guide!"

for place_md in glob.glob("places/*.md"):
    slug = place_md[7:-3]
    with open(place_md) as f:
        _, frontmatter, md = f.read().split("---", 2)
    meta = yaml.load(frontmatter, Loader=yaml.Loader)
    html = markdown(md.strip())
    rendered = template.render(
        **meta,
        taste_text=rating_to_text(meta["taste"]),
        value_text=rating_to_text(meta["value"]),
        title=format_title(meta),
        description=format_description(meta),
        content=html,
    )
    out_dir = build_dir / "places" / slug
    relative_url = f"/places/{slug}/"
    out_dir.mkdir(exist_ok=True, parents=True)
    with open(out_dir / "index.html", "w") as o:
        o.write(rendered)
    geojson_features.append({
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [meta["lon"], meta["lat"]]
      },
      "properties": {**meta, "url": relative_url}
    })

geojson = {
  "type": "FeatureCollection",
  "features": geojson_features
}

with open(build_dir / "places.geojson", "w") as o:
    o.write(json.dumps(geojson))

print("Done building tgtg.")
