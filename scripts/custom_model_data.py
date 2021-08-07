import pandas
import urllib.request
import json
import os.path

OUT_PATH = "gm4_resources/assets/minecraft/models/item"
GM4_MODEL_PATH = "gm4_resources/assets/gm4/models"

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

IGNORES = ("fishing_rod", "elytra", "crossbow", "compass", "bow", "clock", "carrot_on_a_stick", "warped_fungus_on_a_stick") # items with strange model files 

CMD_PREFIXS = (0, 3420000) # legacy and registered prefixes

def add_override(i, model):
	return { "predicate": {"custom_model_data": i }, "model": model }

data = pandas.read_csv(DOC_URL)
models = json.load(urllib.request.urlopen(MODELS_URL))

for item, overrides in data.groupby("Item"):
	if item not in IGNORES:
		model = models[item]
		model["overrides"] = []
		prev = 0
		for prefix in CMD_PREFIXS: # for each listed prefix, legacy and registered
			for _, row in overrides.iterrows():
				if prev > 0 and row[1] - prev > 1: # if non-continious CMD range, ensure non-overwridden items default to vanilla
					model["overrides"].append(add_override(prev + 1 + prefix, f"minecraft:item/{item}"))

				gm4_model_name = CATEGORIES[row[2]] + row[3]
				model["overrides"].append(add_override(row[1] + prefix, gm4_model_name)) # add override to model file
		
				# check if referenced model name exists in gm4_resources, and if not, create a placeholder file
				gm4_model_file = GM4_MODEL_PATH+gm4_model_name.replace("gm4:", "/")+".json"
				if not os.path.isfile(gm4_model_file):
					print(f"model {gm4_model_file} does not exist")
					with open(gm4_model_file, "w") as f:
						default_model = { "parent": f"item/{item}" }
						json.dump(default_model, f, indent=4)
						f.write("\n")
						print(f"default {gm4_model_file} created")

				prev = row[1]
			model["overrides"].append(add_override(prev + 1 + prefix, f"minecraft:item/{item}"))


		with open(f"{OUT_PATH}/{item}.json", "w") as f:
			json.dump(model, f, indent=4)
			f.write("\n")
