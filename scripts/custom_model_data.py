import pandas
import urllib.request
import json
import errno
import os
import special_cases
import generate_gm4
import preprocess

VERSION = "1.20"
NAMESPACE = "gm4"
CMD_PREFIXES = (0, 3420000) # legacy and registered prefixes

VANILLA_MODEL_PATH = "gm4_resource_pack/assets/minecraft/models/item"

DOC_ID = "1myt9FkMYkvyzpr9Uu7wXyzXNNreLQreWfWfP4CAGMQM"
DOC_SHEET = "Data"
DOC_URL = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/gviz/tq?tqx=out:csv&sheet={DOC_SHEET}"
PR_SHEET = "PRs"
PR_URL = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/gviz/tq?tqx=out:csv&sheet={PR_SHEET}"

MODELS_URL = f"https://raw.githubusercontent.com/misode/mcmeta/{VERSION}-summary/assets/model/data.min.json"

CATEGORIES = {
  "block": "block/",
  "item": "item/",
  "entity": "entity/",
  "icon": "gui/advancements/icon/",
}

IGNORES = () # items with strange model files 

def write_json(path, content):
  if not os.path.exists(os.path.dirname(f"{path}.json")):
    try:
        os.makedirs(os.path.dirname(f"{path}.json"))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
  with open(f"{path}.json", "w+") as file:
    json.dump(content, file, indent=4)
    file.write("\n")

data = pandas.read_csv(DOC_URL)
data = pandas.concat([data,pandas.read_csv(PR_URL)])
models = json.load(urllib.request.urlopen(MODELS_URL))

models = {k.replace('item/',''):v for k,v in models.items() if 'item/' in k}
generated_models = set()

data = preprocess.preprocess_data(data)
data.dropna(subset = ["Item"], inplace=True)

for item, overrides in data.groupby("Item"):
  if item in IGNORES:
    continue
  if '{' in item: 
    print(item)
    continue
  model = models[item]
  if not model.get("overrides"): model["overrides"] = []
  prev = 0


  # if item in special_cases.cases and "init" in special_cases.cases[item]: special_cases.cases[item]["init"](model)

  def add_override(i, m, model, category):
    if item in special_cases.cases and "add_override" in special_cases.cases[item]: return special_cases.cases[item]["add_override"](i, m, model, category)
    model["overrides"].append({"predicate": {"custom_model_data": i}, "model": m})

  for prefix in CMD_PREFIXES:
    for _, row in overrides.sort_values('Index').iterrows():
      try:
        [item, index, category, module, name, model_type, texture, parent] = row
      except Exception as err:
        print(err)
        print(row)
        exit()
      full_name = f"{CATEGORIES[category]}{module}/{name}"
      # full_name = f"{CATEGORIES[category]}{name}"


       # if non-continious CMD range, ensure non-overwridden items default to vanilla
      if prev > 0 and index - prev > 1:
        add_override(prefix + prev + 1, f"minecraft:item/{item}", model, category)

      # add override to model file
      add_override(prefix + index, f"{NAMESPACE}:{full_name}", model, category)
      prev = index

      if item in special_cases.cases and "model_generator" in special_cases.cases[item]: special_cases.cases[item]["model_generator"](full_name, generated_models, model_type, item, texture, name, module, parent, write_json, category)
      else: generate_gm4.generate(full_name, generated_models, model_type, item, texture, name, module, parent, write_json)

    # add last override to the end of the model file
    add_override(prefix + prev + 1, f"minecraft:item/{item}", model, category)

  write_json(f"{VANILLA_MODEL_PATH}/{item}", model)


# Check for extra textures/Models

# def getListOfFiles(dirName):
#     # create a list of file and sub directories 
#     # names in the given directory 
#     listOfFile = os.listdir(dirName)
#     allFiles = list()
#     # Iterate over all the entries
#     for entry in listOfFile:
#         # Create full path
#         fullPath = os.path.join(dirName, entry)
#         # If entry is a directory then get the list of files in this directory 
#         if os.path.isdir(fullPath):
#             allFiles = allFiles + getListOfFiles(fullPath)
#         else:
#             allFiles.append(fullPath)
                
#     return allFiles


# modelsInFolder = getListOfFiles('./gm4_resource_pack/assets/gm4/models/')
# usedtextures = set()
# unusedmodels = set()
# parents = set()
# for model in modelsInFolder:
#   with open(model) as f:
#     data2 = json.load(f)
#     textures = data2.get('textures')
#     parent = data2.get('parent')
#   if parent and 'gm4:' in parent:
#     parent = parent.replace('gm4:','')
#     if parent not in generate_gm4.usedmodels:
#       parents.add(parent)
#   if textures:
#     for texture in textures:
#       texturepath = textures[texture].replace('gm4:','')
#       if 'minecraft' in texturepath: continue
#       if texturepath not in usedtextures:
#         usedtextures.add(texturepath)
#   newmodel = model.replace('./gm4_resource_pack/assets/gm4/models/','').replace('\\','/').replace('.json','')
#   if newmodel not in generate_gm4.usedmodels:
#     unusedmodels.add(newmodel)
# unusedmodels -= parents


# unusedtextures = set()
# texturesInFolder = getListOfFiles('./gm4_resource_pack/assets/gm4/textures/')
# for texture in texturesInFolder:
#   if ('.mcmeta' in texture) or ('_e.' in texture): 
#     continue
#   usedtexture = texture.replace('./gm4_resource_pack/assets/gm4/textures/','').replace('\\','/').replace('.png','')
#   if usedtexture not in usedtextures:
#     unusedtextures.add(usedtexture)

# print(unusedmodels,'\n\n',unusedtextures)

# i = 0
# j = 1
# shulker1 = 'give @p shulker_box{BlockEntityTag:{Items:['
# shulker2 = ']}} 1'
# items = []
# lines = []
# for _, row in data.sort_values(['Module','Item','Index']).iterrows():
#     [item, index, category, module, name, model_type, texture, parent] = row
#     lore = f'\'{{"text":"Item: {item}"}}\',\'{{"text":"CMD: {index}"}}\',\'{{"text":"Module: {module}"}}\',\'{{"text":"Name: {name}"}}\',\'{{"text":"Type: {model_type}"}}\',\'{{"text":"Category: {category}"}}\',\'{{"text":"Texture: {texture}"}}\',\'{{"text":"Parent: {parent}"}}\''
#     tag = f'{{Slot:{i%27}b,id:"minecraft:{item}",Count:1b,tag:{{CustomModelData:{index},display:{{Name:\'{{"text":"{module}:{name}","italic":false}}\',Lore:[{lore}]}}}}}}'
#     items.append(tag)

#     if i % 27 == 26:
#       lines.append(shulker1 + ','.join(items) + f']}},display:{{Name:\'{{"text":"{j}"}}\'}}}}')
#       items = []
#       j+=1
#     i += 1
# if i % 27 != 0: lines.append(shulker1 + ','.join(items) + f']}},display:{{Name:\'{{"text":"{j}"}}\'}}}}')

# path = './all.mcfunction'
# if not os.path.exists(os.path.dirname(path)):
#     try:
#         os.makedirs(os.path.dirname(path))
#     except OSError as exc: # Guard against race condition
#         if exc.errno != errno.EEXIST:
#             raise
# with open(path, "w+") as file:
#     file.write('\n'.join(lines))
#     file.write("\n")
