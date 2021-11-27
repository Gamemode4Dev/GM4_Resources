import pandas

TOOL_MATERIALS=("wooden","stone","iron","golden","diamond","netherite")
ARMOR_MATERIALS=("leather","chainmail","iron","golden","diamond","netherite")

def preprocess_data(data):
  newData = pandas.DataFrame(columns=["Item","Index","Category","Module","Name","Model","Texture","Parent"])
  for i, row in data.iterrows():
    if any(isinstance(string, str) and '{' in string for string in row):
      newData = newData.append(specialHandler(row))
    else:
      newData = newData.append([row])
  return newData


def specialHandler(ogrow):
  extra_rows = [ogrow]
  for row in extra_rows:
    [item, index, category, module, name, model_type, texture, parent] = row
    if ('{tooltype}' in item):
      for tool_type in TOOL_MATERIALS:
        extra_rows.append({
          "Item": item.format(tooltype=tool_type),
          "Index": index, 
          "Category": category,
          "Module": module,
          "Name": name.format(tooltype=tool_type),
          "Model": model_type,
          "Texture": texture.format(tooltype=tool_type),
          "Parent": parent
        })
    if ('{armortype}' in item):
      for armor_type in ARMOR_MATERIALS:
        temptexture = texture
        if (armor_type == 'netherite') and ('helmet' in item):
          temptexture += '_netherite'
        if (armor_type == 'leather') and ('leggings' in item):
          temptexture += '_leather'
        extra_rows.append({
          "Item": item.format(armortype=armor_type),
          "Index": index, 
          "Category": category,
          "Module": module,
          "Name": name.format(armortype=armor_type),
          "Model": model_type,
          "Texture": temptexture.format(armortype=armor_type),
          "Parent": parent
        })
    return extra_rows
  