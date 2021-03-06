# description: train fastai resnet18 model on mnist data

# imports
import git

from pathlib import Path
from azureml.core import Workspace
from azureml.core import ScriptRunConfig, Experiment, Environment

# get workspace
ws = Workspace.from_config()

# get root of git repo
prefix = Path(git.Repo(".", search_parent_directories=True).working_tree_dir)

# training script
script_dir = prefix.joinpath("code", "models", "fastai", "mnist-resnet18")
script_name = "train.py"

# environment file
environment_file = prefix.joinpath("environments", "fastai-example.yml")

# azure ml settings
environment_name = "fastai-mnist-example"
experiment_name = "fastai-mnist-example"
compute_target = "cpu-cluster"

# create environment
env = Environment.from_conda_specification(environment_name, environment_file)

# create job config
src = ScriptRunConfig(
    source_directory=script_dir,
    script=script_name,
    environment=env,
    compute_target=compute_target,
)

# submit job
run = Experiment(ws, experiment_name).submit(src)
print(run)
run.wait_for_completion(show_output=True)
