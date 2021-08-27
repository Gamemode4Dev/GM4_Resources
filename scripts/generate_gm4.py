GM4_MODEL_PATH = "gm4_resources/assets/gm4/models"
usedmodels = set()
usedtextures = set()


def generate(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json):
  full_name=full_name.replace('*','')
  name=name.replace('*','')
  # the first time seeing this model, if it's not custom, generate the file
  if full_name not in usedmodels:
    usedmodels.add(full_name)
  if full_name not in generated_models and model_type != "custom":
    generated_models.add(full_name)
    # prepare model base on the model type
    gm4_model = {}
    if model_type == "vanilla":
      gm4_model["parent"] = f"minecraft:item/{item}"
      if texture == texture:
        gm4_model["textures"] = {
          "layer0": f"gm4:item/{texture}"
        }
    else:
      model_parts = model_type.split("_")
      parent = model_parts[0]
      if parent == "vanilla":
        parent = item
      modifier = model_parts[1] if len(model_parts) == 2 else None
      if texture != texture:
        texture = f"{module}/{name}"
        # texture = name
      gm4_model["parent"] = f"minecraft:item/{parent}"
      if modifier == "layered":
        if parent == item:
          if "leather_" in item:
            gm4_model["textures"] = {
              "layer2": f"gm4:item/{texture}"
            }
          else:
            gm4_model["textures"] = {
              "layer1": f"gm4:item/{texture}"
            }
        else:
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
    if parent_overwrite == parent_overwrite: gm4_model["parent"] = parent_overwrite
    write_json(f"{GM4_MODEL_PATH}/{full_name}", gm4_model)
