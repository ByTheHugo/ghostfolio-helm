import os
import subprocess
import yaml
import logging
import pytest

HELM_TEMPLATES_FILEPATH = "tmp/manifests.yaml"
HELM_FILEPATH = f"{os.path.dirname(os.path.abspath(__file__))}/../chart"

def helm_render(release_name: str, values_file: str = "") -> dict:
    templates_directory = os.path.dirname(HELM_TEMPLATES_FILEPATH)
    if not os.path.exists(templates_directory):
      os.makedirs(templates_directory)

    if os.path.exists(HELM_TEMPLATES_FILEPATH):
      os.remove(HELM_TEMPLATES_FILEPATH)

    # Build the helm template command
    helm_cmd = ["helm", "template", release_name, HELM_FILEPATH]
    if values_file:
      helm_cmd.extend(["-f", values_file])

    try:
        # Run the command and capture output
        result = subprocess.run(
            helm_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Parse the multi-document YAML output
        parsed_manifests = list(yaml.safe_load_all(result.stdout))

        # Filter out any None values (which happen if there are empty documents or trailing '---')
        parsed_manifests = [doc for doc in parsed_manifests if doc]

        return parsed_manifests

    except subprocess.CalledProcessError as e:
        logging.error(f"Error running helm template: {e.stderr}")
        return None
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML: {e}")
        return None

def get_manifest_by_type_and_name(manifests: list(), kind: str, name: str = ""):
    matching_manifests = []
    for manifest in manifests:
      if (name and manifest["metadata"]["name"] == name and manifest["kind"] == kind) or (not name and manifest["kind"] == kind):
        matching_manifests.append(manifest)
    return matching_manifests

def get_deployment_env_by_name(manifest: dict, name: str):
    env_map = manifest["spec"]["template"]["spec"]["containers"][0]["env"]
    for env in env_map:
      if env["name"] == name:
        return env
