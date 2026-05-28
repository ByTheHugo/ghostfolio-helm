<!-- markdownlint-disable MD033 MD024 -->

[![Latest Tag](https://img.shields.io/github/v/tag/ByTheHugo/ghostfolio-helm)](https://github.com/ByTheHugo/ghostfolio-helm/tags)
[![Project License](https://img.shields.io/github/license/ByTheHugo/ghostfolio-helm)](https://github.com/ByTheHugo/ghostfolio-helm/blob/master/LICENSE)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/bythehugo/ghostfolio-helm)](https://github.com/ByTheHugo/ghostfolio-helm/commits/master/)
[![GitHub Commit Activity](https://img.shields.io/github/commit-activity/m/bythehugo/ghostfolio-helm)](https://github.com/ByTheHugo/ghostfolio-helm/commits/master/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-ghostfolio--helm-lightgrey)](https://github.com/ByTheHugo/ghostfolio-helm)
[![ArtifactHub Package](https://img.shields.io/badge/ArtifactHub.io-ghostfolio--helm-lightblue)](https://artifacthub.io/packages/helm/ghostfolio/ghostfolio)

![Ghostfolio Helm banner](docs/ghostfolio-helm-banner.png)

# Ghostfolio Helm Chart

This project provides a _Helm_ chart for deploying **[Ghostfolio: the Open Source Wealth Management Software](https://github.com/ghostfolio/ghostfolio)** into any _Kubernetes_ cluster. It integrates the official _Docker_ images built by the _Ghostfolio_ team and hosted on _[DockerHub](https://hub.docker.com/r/ghostfolio/ghostfolio)_. It also includes _[PostgreSQL](https://artifacthub.io/packages/helm/bitnami/postgresql)_ and _[Redis](https://artifacthub.io/packages/helm/bitnami/redis)_ servers that use the **Bitnami** charts, but it is easy to provide your own.

The charts are built and then published to these project _GitHub Pages_, allowing anyone to quickly deploy and test the application.

<!-- omit in toc -->
## Table of content

- [Ghostfolio Helm Chart](#ghostfolio-helm-chart)
  - [1.1. Prerequisite](#11-prerequisite)
  - [1.2. Configure the application](#12-configure-the-application)
    - [1.2.1. Secret management](#121-secret-management)
    - [1.2.2. Use an external PostgreSQL server](#122-use-an-external-postgresql-server)
    - [1.2.3. Use an external Redis server](#123-use-an-external-redis-server)
    - [1.2.4. Extra manifests](#124-extra-manifests)
  - [1.3. Install the application](#13-install-the-application)
    - [1.3.1. Add the GitHub Helm repository (optional)](#131-add-the-github-helm-repository-optional)
    - [1.3.2. Install the chart](#132-install-the-chart)
      - [1.3.2.1. Install a specific version of Ghostfolio](#1321-install-a-specific-version-of-ghostfolio)
    - [1.3.3. Verify the deployment](#133-verify-the-deployment)
  - [1.4. Uninstall the application](#14-uninstall-the-application)
  - [1.5. License](#15-license)
  - [1.6. Contact](#16-contact)

## 1.1. Prerequisite

- A **Kubernetes** cluster,
- A **PostgreSQL** server (optional),
- A **Redis** instance (optional),
- The **Helm** client installed locally (see _[Quickstart Guide](https://helm.sh/docs/intro/quickstart/)_),
- The `kubectl` command-line tool installed locally (optionnal, see _[Install Tools](https://kubernetes.io/docs/tasks/tools/)_)

<p align="right"><a href="#ghostfolio-helm-chart">back to top</a></p>

## 1.2. Configure the application

Like any other _Helm_ chart, the available configuration options can be found in the `charts/ghostfolio/values.yaml` configuration file. I recommend you to override any values in a dedicated `ghostfolio.values.yaml` file before deploying the chart:

1. Start by retrieving the chart default values: `helm show values charts/ghostfolio > ghostfolio.values.yaml`

2. Edit the `ghostfolio.values.yaml` values, and specially the following ones:

    ```yaml
    ghostfolio:
      # ACCESS_TOKEN_SALT and JWT_SECRET_KEY are auto-generated if left empty.
      # See section 1.2.1 for more options.
      ACCESS_TOKEN_SALT: ""
      JWT_SECRET_KEY: ""

    # For more information checkout: https://artifacthub.io/packages/helm/bitnami/postgresql
    postgresql:
      enabled: true
      auth:
        username: ghostfolio-user
        password: ghostfolio-password
        database: ghostfolio-db
        secretRef:
          name: "" # When defined, override the .postgresql.auth.username and .postgresql.auth.password keys
          usernameKey: "username"
          passwordKey: "password"

    # For more information checkout: https://artifacthub.io/packages/helm/bitnami/redis
    redis:
      enabled: true
      architecture: standalone
      auth:
        enabled: true
        password: redis-password
        secretRef:
          name: "" # When defined, override the .redis.auth.password key
          passwordKey: "password"

    ingress:
      enabled: true
      hosts:
        - host: ghostfolio.domain.tld
          paths:
            - path: /
              pathType: ImplementationSpecific
    ```

### 1.2.1. Secret management

By default, `ACCESS_TOKEN_SALT` and `JWT_SECRET_KEY` are **automatically generated** (64-character random strings) on first install. They are preserved across upgrades — if the values are left empty and a secret already exists in the cluster, the existing values are reused.

You have three options:

1. **Auto-generated (default)**: leave `ACCESS_TOKEN_SALT` and `JWT_SECRET_KEY` empty.

    ```yaml
    ghostfolio:
      ACCESS_TOKEN_SALT: ""
      JWT_SECRET_KEY: ""
    ```

2. **Explicit values**: provide your own strings.

    ```yaml
    ghostfolio:
      ACCESS_TOKEN_SALT: mysuperrandomstring
      JWT_SECRET_KEY: mysuperrandomstring
    ```

3. **Existing secret**: reference a pre-existing Kubernetes Secret (e.g. managed by ExternalSecrets, SealedSecrets, or Vault). When set, the chart does **not** create its own Secret resource. The existing secret must contain at least `ACCESS_TOKEN_SALT` and `JWT_SECRET_KEY` keys, plus all other keys the deployment expects (e.g. `REDIS_HOST`, `POSTGRES_HOST`, etc.).

    ```yaml
    ghostfolio:
      existingSecret: my-ghostfolio-secret
      # Override key names if your secret uses different keys:
      # existingSecretAccessTokenSaltKey: ACCESS_TOKEN_SALT
      # existingSecretJwtSecretKeyKey: JWT_SECRET_KEY
    ```

### 1.2.2. Use an external PostgreSQL server

By default, the chart deploys a _PostgreSQL_ server via a subchart dependency. However, if want to use your own instance, you can set the following values:

```yaml
postgresql:
  enabled: false
externalPostgresql:
  host: postgres.domain.tld
  port: 5432
  auth:
    username: external-ghostfolio-user
    password: external-ghostfolio-password
    database: external-ghostfolio-db
    secretRef:
      name: "" # When defined, override the .postgresql.auth.username and .postgresql.auth.password keys
      usernameKey: "username"
      passwordKey: "password"
  options: connect_timeout=300&sslmode=prefer
```

### 1.2.3. Use an external Redis server

By default, the chart deploys a _Redis_ server via a subchart dependency. However, if want to use your own instance, you can set the following values:

```yaml
redis:
  enabled: false
externalRedis:
  host: redis.domain.fqdn
  port: 6379
  auth:
    enabled: false
    password: ""
    secretRef:
      name: "" # When defined, override the .redis.auth.password key
      passwordKey: "password"
```

<p align="right"><a href="#ghostfolio-helm-chart">back to top</a></p>

### 1.2.4. Extra manifests

You can deploy additional Kubernetes resources alongside the chart by using the `extraManifests` value. Each entry is a raw Kubernetes manifest that is templated through Helm:

```yaml
extraManifests:
  - apiVersion: external-secrets.io/v1beta1
    kind: ExternalSecret
    metadata:
      name: ghostfolio-secrets
    spec:
      refreshInterval: 1h
      secretStoreRef:
        name: vault
        kind: SecretStore
      target:
        name: ghostfolio-secrets
      data:
        - secretKey: ACCESS_TOKEN_SALT
          remoteRef:
            key: ghostfolio
            property: access_token_salt
        - secretKey: JWT_SECRET_KEY
          remoteRef:
            key: ghostfolio
            property: jwt_secret_key
```

When using `extraManifests` to create a secret that holds `ACCESS_TOKEN_SALT` and `JWT_SECRET_KEY`, combine it with the `existingSecret` option:

```yaml
ghostfolio:
  existingSecret: ghostfolio-secrets
  existingSecretAccessTokenSaltKey: ACCESS_TOKEN_SALT
  existingSecretJwtSecretKeyKey: JWT_SECRET_KEY
```

<p align="right"><a href="#ghostfolio-helm-chart">back to top</a></p>

## 1.3. Install the application

To deploy the application using Helm, follow these steps:

### 1.3.1. Add the GitHub Helm repository (optional)

```bash
helm repo add ghostfolio https://bythehugo.github.io/ghostfolio-helm/
helm repo update
```

### 1.3.2. Install the chart

```bash
helm upgrade --install ghostfolio ghostfolio/ghostfolio -f ghostfolio.values.yaml
```

You can also install the chart directly from sources:

```bash
helm upgrade --install ghostfolio charts/ghostfolio -f ghostfolio.values.yaml
```

#### 1.3.2.1. Install a specific version of Ghostfolio

If you want to install a specific version of _Ghostfolio_, you must define the `.image.tag` key in the `values.yaml` file or directly inline:

```bash
helm upgrade --install --set "image.tag=3.0.1" ghostfolio ghostfolio/ghostfolio
```

### 1.3.3. Verify the deployment

```bash
kubectl get all -l app=ghostfolio
```

Replace <namespace> with your target namespace if you specified one.

<p align="right"><a href="#ghostfolio-helm-chart">back to top</a></p>

## 1.4. Uninstall the application

To uninstall the _Helm_ chart and remove all associated resources from your _Kubernetes_ cluster, follow these steps:

1. Identify the release name you used when installing the chart. If you haven't changed the release name, it may be the default or the one you specified during installation.

2. Run the following command to uninstall the release:

    ```bash
    helm uninstall ghostfolio
    ```

3. Verify that the resources have been removed:

    ```bash
    kubectl get all -l app=ghostfolio
    ```

    This should return no resources related to the uninstalled release.

**Note:** If you used custom namespaces during installation, include the `-n <namespace>` flag in the commands:

```bash
helm uninstall ghostfolio -n <namespace>
kubectl get all -n <namespace> -l app=ghostfolio
```

<p align="right"><a href="#ghostfolio-helm-chart">back to top</a></p>

## 1.5. License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

<p align="right"><a href="#ghostfolio-helm-chart">back to top</a></p>

## 1.6. Contact

Hugo CHUPIN - <hugo@chupin.xyz> - [hugo.chupin.xyz](https://hugo.chupin.xyz) - [@hugo.chupin.xyz](https://bsky.app/profile/hugo.chupin.xyz)

Project link: [https://github.com/ByTheHugo/ghostfolio-helm](https://github.com/ByTheHugo/ghostfolio-helm)

<p align="right"><a href="#ghostfolio-helm-chart">back to top</a></p>
