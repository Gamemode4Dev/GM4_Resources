import pandas
import urllib.request
import json

NAMESPACE = "gm4"
CMD_PREFIXES = (0, 3420000) # legacy and registered prefixes

VANILLA_MODEL_PATH = "gm4_resources/assets/minecraft/models/item"
GM4_MODEL_PATH = "gm4_resources/assets/gm4/models"

DOC_ID = "1myt9FkMYkvyzpr9Uu7wXyzXNNreLQreWfWfP4CAGMQM"
DOC_SHEET = "Data"
DOC_URL = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/gviz/tq?tqx=out:csv&sheet={DOC_SHEET}"

MODELS_URL = "https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/1.17.1/assets/minecraft/models/item/_all.json"

CATEGORIES = {
	"block": "block/",
	"item": "item/",
	"entity": "entity/",
	"icon": "gui/advancements/icon/",
}

IGNORES = ("fishing_rod", "elytra", "crossbow", "compass", "bow", "clock", "carrot_on_a_stick", "warped_fungus_on_a_stick") # items with strange model files 

def write_json(path, content):
	with open(f"{path}.json", "w") as file:
		json.dump(content, file, indent=4)
		file.write("\n")

data = pandas.read_csv(DOC_URL)
models = json.load(urllib.request.urlopen(MODELS_URL))
generated_models = set()

for item, overrides in data.groupby("Item"):
	if item in IGNORES:
		continue

	model = models[item]
	model["overrides"] = []
	prev = 0

	def add_override(i, m):
		model["overrides"].append({"predicate": {"custom_model_data": i}, "model": m})

	for prefix in CMD_PREFIXES:
		for _, row in overrides.iterrows():
			[item, index, category, name, model_type, texture] = row
			full_name = CATEGORIES[category] + name

 			# if non-continious CMD range, ensure non-overwridden items default to vanilla
			if prev > 0 and index - prev > 1:
				add_override(prefix + prev + 1, f"minecraft:item/{item}")

			# add override to model file
			add_override(prefix + index, f"{NAMESPACE}:{full_name}")
			prev = index

			# the first time seeing this model, if it's not custom, generate the file
			if full_name not in generated_models and model_type != 'custom':
				generated_models.add(full_name)

				# prepare model base on the model type
				gm4_model = {}
				if model_type == 'vanilla':
					gm4_model["parent"] = f"minecraft:item/{item}"

				else:
					model_parts = model_type.split("_")
					parent = model_parts[0]
					modifier = model_parts[1] if len(model_parts) == 2 else None
					if texture != texture:
						texture = name

					gm4_model["parent"] = f"minecraft:item/{parent}"
					if modifier == "layered":
						gm4_model["textures"] = {
							"layer0": f"minecraft:item/{item}",
							"layer1": f"gm4:item/{texture}"
						}
					elif modifier == "overlay":
						gm4_model["textures"] = {
							"layer0": f"gm4:item/{texture}",
							"layer1": f"gm4:item/{texture}_overlay"
						}
					elif modifier == "overlayered":
						gm4_model["textures"] = {
							"layer0": f"minecraft:item/{item}",
							"layer1": f"minecraft:item/{item}_overlay",
							"layer2": f"gm4:item/{texture}"
						}
					else:
						gm4_model["textures"] = {"layer0": f"gm4:item/{texture}"}

				write_json(f"{GM4_MODEL_PATH}/{full_name}", gm4_model)

		# add last override to the end of the model file
		add_override(prefix + prev + 1, f"minecraft:item/{item}")

	write_json(f"{VANILLA_MODEL_PATH}/{item}", model)
