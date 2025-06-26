import importlib.util, json, os

CONFIG_FILE = "config.json"

def charger_config():
  if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  else:
    # Valeurs par défaut
    return {
      "langue": "FR",
      "volume": 1.0,
      "width": 1280,
      "height": 720
    }

def sauvegarder_config(config):
  with open(CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

def load_phrases(lang_code):
  path = f"Phrases{lang_code}.py"
  spec = importlib.util.spec_from_file_location("phrases_module", path)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module.phrasesClass