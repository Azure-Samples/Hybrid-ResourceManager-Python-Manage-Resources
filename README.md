---
services: Azure-Stack
platforms: python
author: viananth
---

# Hybrid-ResourceManager-Python-Manage-Resources

This sample explains how to manage your
[resources and resource groups in Azure Stack](https://azure.microsoft.com/en-us/documentation/articles/resource-group-overview/#resource-groups)
using the Azure Python SDK.

**On this page**

- [Run this sample](#run)
- What is example.py doing?
    - List resource groups
    - Create a resource group
    - Update a resource group
    - Create a key vault in the resource group
    - List resources within the group
    - Export the resource group template
    - Delete a resource group

<a id="run"></a>
## Run this sample

1. If you don't already have it, [install Python](https://www.python.org/downloads/).

1. We recommend to use a [virtual environnement](https://docs.python.org/3/tutorial/venv.html) to run this example, but it's not mandatory. You can initialize a virtualenv this way:

    ```
    pip install virtualenv
    virtualenv mytestenv
    cd mytestenv
    source bin/activate
    ```

1. Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/Hybrid-ResourceManager-Python-Manage-Resources.git
    ```

1. Install the dependencies using pip.

    ```
    cd Hybrid-ResourceManager-Python-Manage-Resources
    pip install -r requirements.txt
    ```

1. Create a [service principal](https://docs.microsoft.com/en-us/azure/azure-stack/azure-stack-create-service-principals) to work against AzureStack. Make sure your service principal has [contributor/owner role](https://docs.microsoft.com/en-us/azure/azure-stack/azure-stack-create-service-principals#assign-role-to-service-principal) on your subscription.

1. Export these environment variables into your current shell. 

    ```
    export AZURE_RESOURCE_LOCATION={your resource location}
    export AZURE_TENANT_ID={your tenant id}
    export AZURE_CLIENT_ID={your client id}
    export AZURE_CLIENT_SECRET={your client secret}
    export AZURE_SUBSCRIPTION_ID={your subscription id}
    export ARM_ENDPOINT={your AzureStack Resource Manager Endpoint}
    ```

1. Run the sample.

    ```
    python example.py
    ```

