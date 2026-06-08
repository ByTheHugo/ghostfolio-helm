import pytest
import logging
from conftest import helm_render, get_manifest_by_type_and_name, get_deployment_env_by_name
from pathlib import Path

HELM_RELEASE_NAME = Path(__file__).stem.replace("_", "-")
HELM_POSTGRESQL_SECRET = f"{HELM_RELEASE_NAME}-ghostfolio-configuration-postgresql"
HELM_REDIS_SECRET = f"{HELM_RELEASE_NAME}-ghostfolio-configuration-redis"
HELM_DEPLOYMENT = f"{HELM_RELEASE_NAME}-ghostfolio"

logging.info(f"> Rendering chart using default values and release name {HELM_RELEASE_NAME}...")
manifests = helm_render(HELM_RELEASE_NAME)

def TP_default_postgresql():
    logging.info(
        "Validating generated manifests with default PostgreSQL server"
    )

    logging.info(f"> Validating Secret/{HELM_POSTGRESQL_SECRET} keys...")
    postgresql_secret = get_manifest_by_type_and_name(manifests, "Secret", HELM_POSTGRESQL_SECRET)
    assert len(postgresql_secret) > 0, f"PostgreSQL configuration Secret not found! Expected to found {HELM_POSTGRESQL_SECRET}..."
    assert "POSTGRES_PASSWORD" in postgresql_secret[0]["stringData"], f"The POSTGRES_PASSWORD key is not defined in the Secret/{HELM_POSTGRESQL_SECRET}!"

    logging.info(f"> Validating Deployment/{HELM_DEPLOYMENT} specs...")
    deployment = get_manifest_by_type_and_name(manifests, "Deployment", HELM_DEPLOYMENT)
    assert len(deployment) > 0, f"Deployment not found! Expected to found {HELM_DEPLOYMENT}..."
    env_key = get_deployment_env_by_name(deployment[0], "POSTGRES_PASSWORD")
    assert env_key, f"Environment value POSTGRES_PASSWORD is not defined in Deployment/{HELM_DEPLOYMENT}!"
    assert env_key["valueFrom"]["secretKeyRef"]["name"] == HELM_POSTGRESQL_SECRET, f"Environment value POSTGRES_PASSWORD not loaded from correct Secret/{HELM_POSTGRESQL_SECRET}!"

def TP_default_redis():
    logging.info(
        "Validating generated manifests with default Redis server"
    )

    logging.info(f"> Validating Secret/{HELM_REDIS_SECRET} keys...")
    redis_secret = get_manifest_by_type_and_name(manifests, "Secret", HELM_REDIS_SECRET)
    assert len(redis_secret) > 0, f"PostgreSQL configuration Secret not found! Expected to found {HELM_REDIS_SECRET}..."
    assert "REDIS_PASSWORD" in redis_secret[0]["stringData"], f"The REDIS_PASSWORD key is not defined in the Secret/{HELM_REDIS_SECRET}!"

    logging.info(f"> Validating Deployment/{HELM_DEPLOYMENT} specs...")
    deployment = get_manifest_by_type_and_name(manifests, "Deployment", HELM_DEPLOYMENT)
    assert len(deployment) > 0, f"Deployment not found! Expected to found {HELM_DEPLOYMENT}..."
    env_key = get_deployment_env_by_name(deployment[0], "REDIS_PASSWORD")
    assert not env_key, f"Environment value REDIS_PASSWORD is defined in Deployment/{HELM_DEPLOYMENT} and not loaded from Secret/{HELM_REDIS_SECRET}!"
