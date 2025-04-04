import json
import yaml
from pathlib import Path
import subprocess

def create_new_ai(username, ai_name):
    dir_path = f"ais/{username}/{ai_name}"
    
    subprocess.run(["mkdir", "-p", dir_path])
    subprocess.run(["cp", "-r", "template", dir_path])

def train_ai(username, ai_name):
    dir_path = f"ais/{username}/{ai_name}"
    
    subprocess.run(
        ["rasa", "train"],
        cwd=dir_path,  
        check=True
    )

def run_ai(username, ai_name):
    dir_path = f"ais/{username}/{ai_name}"
    
    subprocess.run(
        ["rasa", "shell"],
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
        "version": "3.1",
        "intents": json_data["domain"]["intents"],
        "entities": json_data["domain"]["entities"],
        "slots": json_data["domain"]["slots"],
        "responses": json_data["domain"]["responses"],
        "forms": json_data["domain"]["forms"]
    }
    
    domain_path = dir_path / "domain.yml"
    with open(domain_path, "w") as f:
        yaml.dump(domain_content, f, sort_keys=False)

def create_nlu_file(dir_path: Path, json_data: dict):
    nlu_content = {
        "version": "3.1",
        "nlu": [
            {
                "intent": item["intent"],
                "examples": "\n".join(f"- {ex}" for ex in item["examples"])
            }
            for item in json_data["nlu"]
        ]
    }
    nlu_path = dir_path / "data" / "nlu.yml"
    nlu_path.write_text(yaml.dump(nlu_content, sort_keys=False, width=1000))

def create_stories_file(dir_path: Path, json_data: dict):
    stories_content = {
        "version": "3.1",
        "stories": [
            {"story": story["name"], "steps": story["steps"]}
            for story in json_data["stories"]
        ]
    }
    (dir_path / "data" / "stories.yml").write_text(
        yaml.dump(stories_content, sort_keys=False))

def create_rules_file(dir_path: Path, json_data: dict):
    rules_content = {
        "version": "3.1",
        "rules": [
            {"rule": rule["rule"], "steps": rule["steps"]}
            for rule in json_data["rules"]
        ]
    }
    (dir_path / "data" / "rules.yml").write_text(
        yaml.dump(rules_content, sort_keys=False))

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
