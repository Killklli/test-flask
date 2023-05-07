from flask import Flask, make_response
import argparse
import codecs
import json
import pickle
import random
import time
import os
import sys
import traceback

from randomizer.Enums.Settings import SettingsMap
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.SettingStrings import decrypt_settings_string_enum
from randomizer.Spoiler import Spoiler
app = Flask(__name__)



def generate(generate_settings, file_name, gen_spoiler):
    """Gen a seed and write the file to an output file."""
    settings = Settings(generate_settings)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    return spoiler

@app.route('/')
def lambda_function():
    """CLI Entrypoint for generating seeds."""
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
    # Convert string data to enums where possible.
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
                try:
                    setting_data[k] = SettingsMap[k][v]
                except Exception:
                    pass
    try:
        spoiler = generate(setting_data, 'test', True)
    except Exception as e:
        print(traceback.format_exc())
    response = make_response(json.dumps(spoiler.json), 200)
    response.mimetype = "text/plain"
    return response
