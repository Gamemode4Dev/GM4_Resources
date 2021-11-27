TOOL_MATERIALS=("wooden","stone","iron","golden","diamond","netherite")
ARMOR_MATERIALS=("leather","chainmail","iron","golden","diamond","netherite")

def preprocess_data(data):
  to_append = []
  to_drop = []
  for i, row in data.iterrows():
    [item, index, category, module, name, model_type, texture, parent] = row
    if ('{tooltype}' in item):
        if i not in to_drop: to_drop.append(i)
        for tool_type in TOOL_MATERIALS:
          to_append.append({
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
        if i not in to_drop: to_drop.append(i)
        for armor_type in ARMOR_MATERIALS:
          temptexture = texture
          if (armor_type == 'netherite') and ('helmet' in item):
            temptexture += '_netherite'
          if (armor_type == 'leather') and ('leggings' in item):
            temptexture += '_leather'
          to_append.append({
            "Item": item.format(armortype=armor_type),
            "Index": index, 
            "Category": category,
            "Module": module,
            "Name": name.format(armortype=armor_type),
            "Model": model_type,
            "Texture": temptexture.format(armortype=armor_type),
            "Parent": parent
          })
  data = data.drop(to_drop)
  return data.append(to_append)
