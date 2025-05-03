# Ghostfolio Helm Chart
<!-- markdownlint-disable MD033 MD024 -->

This project provides a _Helm_ chart for deploying **[Ghostfolio: the Open Source Wealth Management Software](https://github.com/ghostfolio/ghostfolio)** into any _Kubernetes_ cluster. It integrates the official _Docker_ images built by the _Ghostfolio_ team and hosted on _[DockerHub](https://hub.docker.com/r/ghostfolio/ghostfolio)_

The charts are built and then published to these project _GitHub Pages_, allowing anyone to quickly deploy and test the application.

<!-- omit in toc -->
## Table of content

- [Prerequisite](#prerequisite)
- [Configure the application](#configure-the-application)
- [Install the application](#install-the-application)
  - [Add the GitHub Helm repository (optional)](#add-the-github-helm-repository-optional)
  - [Install the chart](#install-the-chart)
  - [Verify the deployment](#verify-the-deployment)
- [Uninstall the application](#uninstall-the-application)
- [License](#license)
- [Contact](#contact)

## Prerequisite

- A **Kubernetes** cluster,
- A **PostgreSQL** server,
- A **Redis** instance,
- The **Helm** client installed locally (see _[Quickstart Guide](https://helm.sh/docs/intro/quickstart/)_),
- The `kubectl` command-line tool installed locally (optionnal, see _[Install Tools](https://kubernetes.io/docs/tasks/tools/)_)

<p align="right">(<a href="#ghostfolio-helm-chart">back to top</a>)</p>

## Configure the application

Like any other _Helm_ chart, the available configuration options can be found in the `charts/ghostfolio/values.yaml` configuration file. I recommend you to override any values in a dedicated `ghostfolio.values.yaml` file before deploying the chart:

1. Start by retrieving the chart default values: `helm show values charts/ghostfolio > ghostfolio.values.yaml`

2. Edit the `ghostfolio.values.yaml` values, and specially the following ones:

    ```yaml
    ghostfolio:
      accessTokenSalt: mysuperrandomstring
      jwtSecretKey: mysuperrandomstring
      baseCurrency: EUR # or USD

    postgresql:
      database: ghostfolio
      user: ghostfolio
      password: ghostfolio
      host: postgresql.domain.tld
      port: 5432
      options: connect_timeout=300&sslmode=prefer

    redis:
      host: redis.domain.tld
      port: 6379
      password: ""

    ingress:
      enabled: true
      hosts:
        - host: ghostfolio.domain.tld
          paths:
            - path: /
              pathType: ImplementationSpecific
    ```

<p align="right">(<a href="#ghostfolio-helm-chart">back to top</a>)</p>

## Install the application

To deploy the application using Helm, follow these steps:

### Add the GitHub Helm repository (optional)

```bash
helm repo add ghostfolio https://bythehugo.github.io/ghostfolio-helm/
helm repo update
```

### Install the chart

```bash
helm install ghostfolio ghostfolio/ghostfolio -f ghostfolio.values.yaml
```

You can also install the chart directly from sources:

```bash
helm install ghostfolio charts/ghostfolio -f ghostfolio.values.yaml
```

### Verify the deployment

```bash
kubectl get all -l app=ghostfolio
```

Replace <namespace> with your target namespace if you specified one.

<p align="right">(<a href="#ghostfolio-helm-chart">back to top</a>)</p>

## Uninstall the application

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

<p align="right">(<a href="#ghostfolio-helm-chart">back to top</a>)</p>

## License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

<p align="right">(<a href="#ghostfolio-helm-chart">back to top</a>)</p>

## Contact

Hugo CHUPIN - <hugo@chupin.xyz> - [hugo.chupin.xyz](https://hugo.chupin.xyz) - [@hugo.chupin.xyz](https://bsky.app/profile/hugo.chupin.xyz)

Project link: [https://github.com/ByTheHugo/ghostfolio-helm](https://github.com/ByTheHugo/ghostfolio-helm)

<p align="right">(<a href="#ghostfolio-helm-chart">back to top</a>)</p>
