from beet import Context, subproject
from beet.contrib.load import load
import json
import os
import subprocess

OUTPUT = "out"
RELEASE = "release"


def run(cmd: list[str]) -> str:
	return subprocess.run(cmd, capture_output=True, encoding="utf8").stdout.strip()


def build_modules(ctx: Context):
	version = os.getenv("VERSION", "1.20")

	modules = [{"id": p.name} for p in sorted(ctx.directory.glob("gm4_*"))]
	print(f"[GM4] Found {len(modules)} modules")

	head = run(["git", "rev-parse", "HEAD"])
	with open("contributors.json", "r") as f:
		contributors: dict[str, dict] = {entry["name"]: entry for entry in json.load(f)}

	for module in modules:
		id = module["id"]

		try:
			with open(f"{id}/pack.mcmeta", "r+") as f:
				meta: dict = json.load(f)

				if "module_id" not in meta:
					module["id"] = None
					continue

				module["name"] = meta.get("module_name", id)
				module["description"] = meta.get("site_description", "")
				module["categories"] = meta.get("site_categories", [])
				module["libraries"] = meta.get("libraries", [])
				module["requires"] = [f"gm4_{id}" for id in meta.get("required_modules", [])]
				module["recommends"] = [f"gm4_{id}" for id in meta.get("recommended_modules", [])]
				module["wiki_link"] = meta.get("wiki_link", "")
				module["video_link"] = meta.get("video_link", "")
				module["credits"] = meta.get("credits", {})
				module["hidden"] = meta.get("hidden", False)

		except:
			module["id"] = None

	os.makedirs(OUTPUT, exist_ok=True)
	with open(f"{OUTPUT}/meta.json", "w") as f:
		out = {
			"last_commit": head,
			"modules": [m for m in modules if m.get("id") is not None],
			"contributors": contributors,
		}
		json.dump(out, f, indent=2)
		f.write('\n')

	for module in modules:
		id = module["id"]
		if not id:
			continue

		ctx.require(subproject({
			"id": id,
			"resource_pack": {
				"name": f"{id}_{version.replace('.', '_')}",
				"load": [*module["libraries"], id],
				"zipped": True,
			},
			"output": OUTPUT,
			"require": [
        "beet.contrib.optifine",
			],
			"pipeline": [
				"gm4.populate_credits",
			],
			"meta": {
				"contributors": contributors
			}
		}))
		print(f"Generated {id}")


def populate_credits(ctx: Context):
	credits = ctx.assets.mcmeta.data.get("credits", {})
	ctx.assets.mcmeta.data["credits"] = {
		title: [
			dict(**ctx.meta["contributors"].get(p, {'name': p}))
			for p in credits[title]
		]
		for title in credits
		if isinstance(credits[title], list)
	}
