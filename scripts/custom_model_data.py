import pandas
import urllib.request
import json

OUT_PATH = "gm4_resources/assets/minecraft/models/item"

DOC_ID = "1myt9FkMYkvyzpr9Uu7wXyzXNNreLQreWfWfP4CAGMQM"
DOC_SHEET = "Data"
DOC_URL = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/gviz/tq?tqx=out:csv&sheet={DOC_SHEET}"

MODELS_URL = "https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/1.17.1/assets/minecraft/models/item/_all.json"

CATEGORIES = {
	"block": "gm4:block/",
	"item": "gm4:item/",
	"entity": "gm4:entity/",
	"icon": "gm4:gui/advancements/icon/",
}

def add_override(i, model):
	return { "predicate": {"custom_model_data": i }, "model": model }

data = pandas.read_csv(DOC_URL)
models = json.load(urllib.request.urlopen(MODELS_URL))

for item, overrides in data.groupby("Item"):
	model = models[item]
	model["overrides"] = []
	prev = 0
	for _, row in overrides.iterrows():
		if prev > 0 and row[1] - prev > 1:
			model["overrides"].append(add_override(prev + 1, f"minecraft:item/{item}"))
		model["overrides"].append(add_override(row[1], CATEGORIES[row[2]] + row[3]))
		prev = row[1]
	model["overrides"].append(add_override(prev + 1, f"minecraft:item/{item}"))

	with open(f"{OUT_PATH}/{item}.json", "w") as f:
		json.dump(model, f, indent=4)
		f.write("\n")
