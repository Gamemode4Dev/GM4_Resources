import pandas
from itertools import chain


TOOL_MATERIALS=("wooden","stone","iron","golden","diamond","netherite")
ARMOR_MATERIALS=("leather","chainmail","iron","golden","diamond","netherite")

def preprocess_data(data):
  newData = pandas.DataFrame(columns=["Item","Index","Category","Module","Name","Model","Texture","Parent"])
  for i, row in data.iterrows():
    newData = newData.append(specialHandler(row))
  newData["Index"] = pandas.to_numeric(newData["Index"])
  return newData

def strReplacer(row, string, replacement):
  newRow = row.apply(lambda s: s.replace(string, replacement) if isinstance(s, str) else s)
  if newRow["Item"] == "leather_leggings":
    newRow["Texture"] += "_leather"
  if newRow["Item"] == "netherite_helmet":
    newRow["Texture"] += "_netherite"
  return newRow

def multiStrReplacer(row, string, replacementList):
  return [strReplacer(row, string, replacement) for replacement in replacementList]
       
def numberReplacer(row):
  returnrows = []
  for i in range(int(row["Index"].split("..")[0]),int(row["Index"].split("..")[1]) + 1):
    newRow = row.apply(lambda s: s.replace('{#}', str(i)) if isinstance(s, str) else s)
    newRow["Index"] = i
    returnrows.append(newRow)
  return returnrows

def specialHandler(row):
  returnrows = []
  if any('{tooltype}' in s for s in row if isinstance(s, str)):
    returnrows += chain(*[specialHandler(x) for x in multiStrReplacer(row, '{tooltype}', TOOL_MATERIALS)])
  elif any('{armortype}' in s for s in row if isinstance(s, str)):
    returnrows += chain(*[specialHandler(x) for x in multiStrReplacer(row, '{armortype}', ARMOR_MATERIALS)])
  elif isinstance(row["Index"], str) and '..' in row["Index"]:
      returnrows += chain(*[specialHandler(x) for x in numberReplacer(row)])
  else:
    returnrows.append(row)
  return returnrows
  