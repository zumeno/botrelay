import json
import yaml
from pathlib import Path
import subprocess

def create_new_ai(username, ai_name):
    dir_path = f"ais/{username}/{ai_name}"
    
    subprocess.run(["mkdir -p", dir_name])
    subprocess.run(["cp -r template", dir_path])

def train_ai(username, ai_name):
    dir_path = f"ais/{username}/{ai_name}"
    
    subprocess.run(
        ["rasa", "train"],
        cwd=dir_path,  
        check=True
    )


def clear_existing_rasa_files(dir_path):
    subprocess.run(["rm", "-f", "domain.yml", "data/nlu.yml", "data/stories.yml", "data/rules.yml"], 
                  cwd=dir_path)

def load_json_config(username, ai_name):
    config_path = Path(f"ais/{username}/{ai_name}/config.json")
    with open(config_path) as f:
        return json.load(f)

def create_domain_file(dir_path, json_data):
    domain_content = {
        "intents": json_data["domain"]["intents"],
        "entities": json_data["domain"]["entities"],
        "slots": json_data["domain"]["slots"],
        "responses": json_data["domain"]["responses"],
        "forms": json_data["domain"]["forms"]
    }
    
    domain_path = dir_path / "domain.yml"
    with open(domain_path, "w") as f:
        yaml.dump(domain_content, f, sort_keys=False)

def create_nlu_file(dir_path, json_data):
    nlu_content = {"nlu": []}
    for item in json_data["nlu"]:
        nlu_item = {
            "intent": item["intent"],
            "examples": "\n".join(f"- {ex}" for ex in item["examples"])
        }
        nlu_content["nlu"].append(nlu_item)
    
    nlu_path = dir_path / "data" / "nlu.yml"
    with open(nlu_path, "w") as f:
        yaml.dump(nlu_content, f, sort_keys=False, width=1000)

def create_stories_file(dir_path, json_data):
    stories_content = {"stories": []}
    for story in json_data["stories"]:
        story_item = {"story": story["name"], "steps": story["steps"]}
        stories_content["stories"].append(story_item)
    
    stories_path = dir_path / "data" / "stories.yml"
    with open(stories_path, "w") as f:
        yaml.dump(stories_content, f, sort_keys=False)

def create_rules_file(dir_path, json_data):
    rules_content = {"rules": []}
    for rule in json_data["rules"]:
        rule_item = {"rule": rule["rule"], "steps": rule["steps"]}
        rules_content["rules"].append(rule_item)
    
    rules_path = dir_path / "data" / "rules.yml"
    with open(rules_path, "w") as f:
        yaml.dump(rules_content, f, sort_keys=False)

def convert_json_to_rasa_ai(username, ai_name):
    dir_path = Path(f"ais/{username}/{ai_name}")
    
    (dir_path / "data").mkdir(exist_ok=True)
    
    clear_existing_rasa_files(dir_path)
    
    json_data = load_json_config(username, ai_name)
    
    create_domain_file(dir_path, json_data)
    create_nlu_file(dir_path, json_data)
    create_stories_file(dir_path, json_data)
    create_rules_file(dir_path, json_data)
    
    print(f"Successfully converted JSON to Rasa files in {dir_path}")
