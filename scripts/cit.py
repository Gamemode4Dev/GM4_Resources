import pandas
import errno
import os
import cit_preprocess

NAMESPACE = "gm4"
CMD_PREFIXES = (0, 3420000) # legacy and registered prefixes

VANILLA_MODEL_PATH = "gm4_resources/assets/minecraft/optifine/cit"

DOC_ID = "1myt9FkMYkvyzpr9Uu7wXyzXNNreLQreWfWfP4CAGMQM"
DOC_SHEET = "ArmorCIT"
DOC_URL = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/gviz/tq?tqx=out:csv&sheet={DOC_SHEET}"

def write_cit(path, content):
  if not os.path.exists(os.path.dirname(f"{path}.properties")):
    try:
        os.makedirs(os.path.dirname(f"{path}.properties"))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
  with open(f"{path}.properties", "w+") as file:
    file.write(content)

data = pandas.read_csv(DOC_URL)


data = cit_preprocess.preprocess_data(data)
data.dropna(subset = ["Item"], inplace=True)

for i, rows in data.groupby(["Item","Module","Name"]):
  CMDList = rows["Index"].tolist()
  CMDList = CMDList + [x + 3420000 for x in CMDList]
  for row in rows.iterrows():
    row = row[1]
    texturebase = row['Item'].replace("_helmet","").replace("_chestplate","").replace("_leggings","").replace("_boots","").replace("golden","gold")
    namebase = row['Name'].split('/')[-1].replace("_helmet","").replace("_chestplate","").replace("_leggings","").replace("_boots","").replace("golden","gold")
    res = "type=armor\n"
    res += f"matchItems={row['Item']}\n"
    if (row["Layer 1"]): res += f"texture.{texturebase}_layer_1={namebase}_layer_1\n"
    if (row["Overlay 1"] and "leather" in texturebase): res += f"texture.{texturebase}_layer_1_overlay={namebase}_layer_1_overlay\n"
    if (row["Layer 2"]): res += f"texture.{texturebase}_layer_2={namebase}_layer_2\n"
    if (row["Overlay 2"] and "leather" in texturebase): res += f"texture.{texturebase}_layer_2_overlay={namebase}_layer_2_overlay\n"
    if len(CMDList) == 1: res += f"nbt.CustomModelData={CMDList[0]}\n"
    else: res += f'nbt.CustomModelData=regex:({"|".join(str(x) for x in CMDList)})\n'
  
  
    write_cit(f"{VANILLA_MODEL_PATH}/{row['Module']}/{row['Name']}", res)

OTHER_SHEET = "OtherCIT"
OTHER_URL = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/gviz/tq?tqx=out:csv&sheet={OTHER_SHEET}"

data2 = pandas.read_csv(OTHER_URL)
data2.dropna(subset = ["Item"], inplace=True)

for i, rows in data2.groupby(["Type","Item","Name"]):
  if i[0] == "elytra":
    for row in rows.iterrows():
      row = row[1]
      res = f"type=elytra\nmatchItems=elytra\ntexture.elytra={row['Name'].split('/')[-1]}\nnbt.CustomModelData={row['Index'] + CMD_PREFIXES[1]}\n"
      res += f"nbt.CustomModelData=regex:({row['Index']}|{row['Index'] + 3420000})\n"
      write_cit(f"{VANILLA_MODEL_PATH}/{row['Module']}/{row['Name']}", res)
  elif i[0] == "item":
    CMDList = rows["Index"].tolist()
    CMDList = CMDList + [x + 3420000 for x in CMDList]
    for row in rows.iterrows():
      row = row[1]
      res = f"type=item\nmatchItems={row['Item']}\ntexture={row['Name'].split('/')[-1]}\nnbt.CustomModelData={row['Index'] + CMD_PREFIXES[1]}\n"
      if len(CMDList) == 1: res += f"nbt.CustomModelData={CMDList[0]}\n"
      else: res += f'nbt.CustomModelData=regex:({"|".join(str(x) for x in CMDList)})\n'
      write_cit(f"{VANILLA_MODEL_PATH}/{row['Module']}/{row['Name']}", res)
