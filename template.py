import os
from pathlib import Path

project_name = "us_visa_approval"

list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/componets/__init__.py",
    f"src/{project_name}/componets/data_ingestion.py",
    f"src/{project_name}/componets/data_validation.py",
    f"src/{project_name}/componets/data_transformation.py",
    f"src/{project_name}/componets/model_trainer.py",
    f"src/{project_name}/componets/model_evaluation.py",
    f"src/{project_name}/componets/model_pusher.py",
    f"src/{project_name}/configuration/__init__.py",
    f"src/{project_name}/constant/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/entity/artifact_entity.py",
    f"src/{project_name}/logger/__init__.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/pipeline/training_pipeline.py",
    f"src/{project_name}/pipeline/prediction_pipeline.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/main_utils.py",
    "app.py",
    "Dockerfile",
    ".dockerignore",
    "demo.py",
    "setup.py",
    "config/model.yaml",
    "config/schema.yaml",
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w")as f:
            pass
    else:
        print(f"file is already exist at: {filepath}")