from flask import Flask
from randomizer.Enums.Settings import SettingsMap
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler
import json
import random
app = Flask(__name__)

@app.route('/')
def hello():
    presets = json.load(open("static/presets/preset_files.json"))
    default = json.load(open("static/presets/default.json"))
    found = False
    for file in presets.get("progression"):
        with open("static/presets/" + file, "r") as preset_file:
            data = json.load(preset_file)
            if "Season 1 Race Settings" == data.get("name"):
                setting_data = default
                for key in data:
                    setting_data[key] = data[key]
                setting_data.pop("name")
                setting_data.pop("description")
                found = True
    setting_data["seed"] = random.randint(0, 100000000)
    for k, v in setting_data.items():
        if k in SettingsMap:
            if type(v) is list:
                values = []
                for val in v:
                    if type(val) is int:
                        values.append(SettingsMap[k](val))
                    else:
                        values.append(SettingsMap[k][val])
                setting_data[k] = values
            elif type(v) is int:
                setting_data[k] = SettingsMap[k](v)
            else:
                setting_data[k] = SettingsMap[k][v]
    settings = Settings(setting_data)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    return spoiler.json