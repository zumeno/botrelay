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
