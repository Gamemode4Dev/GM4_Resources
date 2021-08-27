import generate_gm4

COMPASS_OVERRIDES = ((0.000000,""),(0.015625,"_17"),(0.046875,"_18"),(0.078125,"_19"),(0.109375,"_20"),(0.140625,"_21"),(0.171875,"_22"),(0.203125,"_23"),(0.234375,"_24"),(0.265625,"_25"),(0.296875,"_26"),(0.328125,"_27"),(0.359375,"_28"),(0.390625,"_29"),(0.421875,"_30"),(0.453125,"_31"),(0.484375,"_00"),(0.515625,"_01"),(0.546875,"_02"),(0.578125,"_03"),(0.609375,"_04"),(0.640625,"_05"),(0.671875,"_06"),(0.703125,"_07"),(0.734375,"_08"),(0.765625,"_09"),(0.796875,"_10"),(0.828125,"_11"),(0.859375,"_12"),(0.890625,"_13"),(0.921875,"_14"),(0.953125,"_15"),(0.984375,""))
CLOCK_OVERRIDES = ((0.0,""),(0.0078125,"_01"),(0.0234375,"_02"),(0.0390625,"_03"),(0.0546875,"_04"),(0.0703125,"_05"),(0.0859375,"_06"),(0.1015625,"_07"),(0.1171875,"_08"),(0.1328125,"_09"),(0.1484375,"_10"),(0.1640625,"_11"),(0.1796875,"_12"),(0.1953125,"_13"),(0.2109375,"_14"),(0.2265625,"_15"),(0.2421875,"_16"),(0.2578125,"_17"),(0.2734375,"_18"),(0.2890625,"_19"),(0.3046875,"_20"),(0.3203125,"_21"),(0.3359375,"_22"),(0.3515625,"_23"),(0.3671875,"_24"),(0.3828125,"_25"),(0.3984375,"_26"),(0.4140625,"_27"),(0.4296875,"_28"),(0.4453125,"_29"),(0.4609375,"_30"),(0.4765625,"_31"),(0.4921875,"_32"),(0.5078125,"_33"),(0.5234375,"_34"),(0.5390625,"_35"),(0.5546875,"_36"),(0.5703125,"_37"),(0.5859375,"_38"),(0.6015625,"_39"),(0.6171875,"_40"),(0.6328125,"_41"),(0.6484375,"_42"),(0.6640625,"_43"),(0.6796875,"_44"),(0.6953125,"_45"),(0.7109375,"_46"),(0.7265625,"_47"),(0.7421875,"_48"),(0.7578125,"_49"),(0.7734375,"_50"),(0.7890625,"_51"),(0.8046875,"_52"),(0.8203125,"_53"),(0.8359375,"_54"),(0.8515625,"_55"),(0.8671875,"_56"),(0.8828125,"_57"),(0.8984375,"_58"),(0.9140625,"_59"),(0.9296875,"_60"),(0.9453125,"_61"),(0.9609375,"_62"),(0.9765625,"_63"),(0.9921875,""))

def fishing_rod_overrides(i,m,model,category):
  if m[0] == "m": m += "*"
  model["overrides"].append({"predicate": {"custom_model_data": i}, "model": m.replace("*","")})
  if category == "icon": return
  model["overrides"].append({"predicate": {"custom_model_data": i, "cast": 1}, "model": m.replace("*","_cast")})

def fishing_rod_model_generator(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json, category):
  generate_gm4.generate(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json)
  if category == "icon": return
  generate_gm4.generate(full_name.replace("*","_cast"), generated_models, model_type, "fishing_rod_cast", texture, name.replace("*","_cast"), module, parent_overwrite, write_json)

def bow_overrides(i,m,model,category):
  if m[0] == "m": m += "*"
  model["overrides"].append({"predicate": {"custom_model_data": i}, "model": m.replace("*","")})
  if category == "icon": return
  model["overrides"].append({"predicate": {"custom_model_data": i, "pulling": 1}, "model": m.replace("*","_pulling_0")})
  model["overrides"].append({"predicate": {"custom_model_data": i, "pulling": 1, "pull": 0.65}, "model": m.replace("*","_pulling_1")})
  model["overrides"].append({"predicate": {"custom_model_data": i, "pulling": 1, "pull": 0.9}, "model": m.replace("*","_pulling_2")})

def bow_model_generator(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json, category):
  if texture == texture:
    generate_gm4.generate(full_name, generated_models, model_type, item, texture.replace("*",""), name, module, parent_overwrite, write_json)
    if category == "icon": return
    generate_gm4.generate(full_name.replace("*","_pulling_0"), generated_models, model_type, "bow_pulling_0", texture.replace("*","_pulling_0"), name.replace("*","_pulling_0"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_pulling_1"), generated_models, model_type, "bow_pulling_1", texture.replace("*","_pulling_1"), name.replace("*","_pulling_1"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_pulling_2"), generated_models, model_type, "bow_pulling_2", texture.replace("*","_pulling_2"), name.replace("*","_pulling_2"), module, parent_overwrite, write_json)
  else:
    generate_gm4.generate(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json)
    if category == "icon": return
    generate_gm4.generate(full_name.replace("*","_pulling_0"), generated_models, model_type, "bow_pulling_0", texture, name.replace("*","_pulling_0"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_pulling_1"), generated_models, model_type, "bow_pulling_1", texture, name.replace("*","_pulling_1"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_pulling_2"), generated_models, model_type, "bow_pulling_2", texture, name.replace("*","_pulling_2"), module, parent_overwrite, write_json)

def crossbow_overrides(i,m,model,category):
  if m[0] == "m": m += "*"
  model["overrides"].append({"predicate": {"custom_model_data": i}, "model": m.replace("*","")})
  if category == "icon": return
  model["overrides"].append({"predicate": {"custom_model_data": i, "pulling": 1}, "model": m.replace("*","_pulling_0")})
  model["overrides"].append({"predicate": {"custom_model_data": i, "pulling": 1, "pull": 0.58}, "model": m.replace("*","_pulling_1")})
  model["overrides"].append({"predicate": {"custom_model_data": i, "pulling": 1, "pull": 1.0}, "model": m.replace("*","_pulling_2")})
  model["overrides"].append({"predicate": {"custom_model_data": i, "charged": 1}, "model": m.replace("*","_arrow")})
  model["overrides"].append({"predicate": {"custom_model_data": i, "charged": 1, "firework": 1}, "model": m.replace("*","_firework")})

def crossbow_model_generator(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json, category):
  if texture == texture:
    generate_gm4.generate(full_name, generated_models, model_type, item, texture.replace("*","_standby"), name, module, parent_overwrite, write_json)
    if category == "icon": return
    generate_gm4.generate(full_name.replace("*","_pulling_0"), generated_models, model_type, "crossbow_pulling_0", texture.replace("*","_pulling_0"), name.replace("*","_pulling_0"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_pulling_1"), generated_models, model_type, "crossbow_pulling_1", texture.replace("*","_pulling_1"), name.replace("*","_pulling_1"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_pulling_2"), generated_models, model_type, "crossbow_pulling_2", texture.replace("*","_pulling_2"), name.replace("*","_pulling_2"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_arrow"), generated_models, model_type, "crossbow_arrow", texture.replace("*","_arrow"), name.replace("*","_arrow"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_firework"), generated_models, model_type, "crossbow_firework", texture.replace("*","_firework"), name.replace("*","_firework"), module, parent_overwrite, write_json)
  else: 
    generate_gm4.generate(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json)
    if category == "icon": return
    generate_gm4.generate(full_name.replace("*","_pulling_0"), generated_models, model_type, item, texture, name.replace("*","_pulling_0"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_pulling_1"), generated_models, model_type, item, texture, name.replace("*","_pulling_1"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_pulling_2"), generated_models, model_type, item, texture, name.replace("*","_pulling_2"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_arrow"), generated_models, model_type, item, texture, name.replace("*","_arrow"), module, parent_overwrite, write_json)
    generate_gm4.generate(full_name.replace("*","_firework"), generated_models, model_type, item, texture, name.replace("*","_firework"), module, parent_overwrite, write_json)

def elytra_overrides(i,m,model,category):
  if m[0] == "m": m = m.replace("elytra", "*elytra")
  model["overrides"].append({"predicate": {"custom_model_data": i}, "model": m.replace("*","")})
  if category == "icon": return
  model["overrides"].append({"predicate": {"custom_model_data": i, "broken": 1}, "model": m.replace("*","broken_")})

def elytra_model_generator(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json, category):
  generate_gm4.generate(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json)
  if category == "icon": return
  generate_gm4.generate(full_name.replace("*","broken_"), generated_models, model_type, "broken_elytra", texture, name.replace("*","broken_"), module, parent_overwrite, write_json)

def compass_overrides(i,m,model,category):
  if m[0] == "m": m += "*"
  if category == "icon": model["overrides"].append({"predicate": {"custom_model_data": i}, "model": m.replace("*","")})
  for override in COMPASS_OVERRIDES:
    model["overrides"].append({"predicate": {"custom_model_data": i, "angle": override[0]}, "model": m.replace("*",override[1])})

def compass_model_generator(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json, category):
  if category == "icon": return
  for override in COMPASS_OVERRIDES:
    if override[1] == "": generate_gm4.generate(full_name, generated_models, model_type, f"{item}_16", texture, name, module, "minecraft:item/compass", write_json)
    generate_gm4.generate(full_name.replace("*",f"{override[1]}"), generated_models, model_type, f"{item}{override[1]}", texture, name.replace("*",f"{override[1]}"), module, parent_overwrite, write_json)

def clock_overrides(i,m,model,category):
  if m[0] == "m": m += "*"
  if category == "icon": model["overrides"].append({"predicate": {"custom_model_data": i}, "model": m.replace("*","")})
  for override in CLOCK_OVERRIDES:
    model["overrides"].append({"predicate": {"custom_model_data": i, "time": override[0]}, "model": m.replace("*",override[1])})

def clock_model_generator(full_name, generated_models, model_type, item, texture, name, module, parent_overwrite, write_json, category):
  if category == "icon": return
  for override in CLOCK_OVERRIDES:
    if override[1] == "": generate_gm4.generate(full_name, generated_models, model_type, f"{item}_00", texture, name, module, "minecraft:item/clock", write_json)
    generate_gm4.generate(full_name.replace("*",f"{override[1]}"), generated_models, model_type, f"{item}{override[1]}", texture, name.replace("*",f"{override[1]}"), module, parent_overwrite, write_json)



cases = {
  "fishing_rod":{"add_override": fishing_rod_overrides, "model_generator": fishing_rod_model_generator},
  "bow": {"add_override": bow_overrides, "model_generator": bow_model_generator},
  "crossbow": {"add_override": crossbow_overrides, "model_generator": crossbow_model_generator},
  "elytra": {"add_override": elytra_overrides, "model_generator": elytra_model_generator},
  "compass": {"add_override": compass_overrides, "model_generator": compass_model_generator},
  "clock": {"add_override": clock_overrides, "model_generator": clock_model_generator},
}
