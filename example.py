"""Create and manage resources and resource groups.
Manage resources and resource groups - create, update and delete a resource group,
deploy a solution into a resource group, export an ARM template. Create, read, update
and delete a resource.

This script expects that the following environment vars are set:

AZURE_TENANT_ID: your Azure Active Directory tenant id or domain
AZURE_CLIENT_ID: your Azure Active Directory Application Client ID
AZURE_CLIENT_SECRET: your Azure Active Directory Application Secret
AZURE_SUBSCRIPTION_ID: your Azure Subscription Id
AZURE_RESOURCE_LOCATION: your resource location
ARM_ENDPOINT: your cloud's resource manager endpoint
"""
import os
import random
import logging
import json
from datetime import datetime

from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential, DefaultAzureCredential

from msrestazure.azure_cloud import get_cloud_from_metadata_endpoint
from azure.profiles import KnownProfiles

# Azure Datacenter
LOCATION = os.environ['AZURE_RESOURCE_LOCATION']

# Resource Group
postfix = random.randint(100, 500)
GROUP_NAME = 'azure-sample-group-resources-{}'.format(postfix)

def run_example():
    """Resource Group management example."""
    #
    # Create the Resource Manager Client with an Application (service principal) token provider
    #
    mystack_cloud = get_cloud_from_metadata_endpoint(
        os.environ['ARM_ENDPOINT'])
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']

    credentials = ClientSecretCredential(
        client_id=os.environ['AZURE_CLIENT_ID'],
        client_secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant_id=os.environ['AZURE_TENANT_ID'],
        authority=mystack_cloud.endpoints.active_directory
    )

    KnownProfiles.default.use(KnownProfiles.v2020_09_01_hybrid)
    logging.basicConfig(level=logging.ERROR)
    scope = "openid profile offline_access" + " " + mystack_cloud.endpoints.active_directory_resource_id + "/.default"
    client = ResourceManagementClient(
        credentials , subscription_id,
        base_url=mystack_cloud.endpoints.resource_manager,
        #profile=KnownProfiles.v2020_09_01_hybrid,
        credential_scopes=[scope])

    #
    # Managing resource groups
    #
    resource_group_params = {'location': LOCATION}

    # List Resource Groups
    print('List Resource Groups')
    for item in client.resource_groups.list():
        print_item(item)

    # Create Resource group
    print('Create Resource Group')
    print_item(client.resource_groups.create_or_update(GROUP_NAME, resource_group_params))

    # Modify the Resource group
    print('Modify Resource Group')
    resource_group_params.update(tags={'hello': 'world'})
    print_item(client.resource_groups.create_or_update(GROUP_NAME, resource_group_params))

    # Create a Key Vault in the Resource Group
    print('Create a Key Vault via a Generic Resource Put')
    key_vault_params = {
        'location': LOCATION,
        'properties': {
            'sku': {'family': 'A', 'name': 'standard'},
            'tenantId': os.environ['AZURE_TENANT_ID'],
            'accessPolicies': [],
            'enabledForDeployment': True,
            'enabledForTemplateDeployment': True,
            'enabledForDiskEncryption': True
        }
    }

    client.resources.begin_create_or_update(
        resource_group_name=GROUP_NAME,
        resource_provider_namespace="Microsoft.KeyVault",
        parent_resource_path="",
        resource_type="vaults",
        resource_name='azureSampleVault' + datetime.utcnow().strftime("-%H%M%S"),
        parameters = key_vault_params,
        api_version="2016-10-01"
    ).result()

    # List Resources within the group
    print('List all of the resources within the group')
    for item in client.resources.list_by_resource_group(GROUP_NAME):
        print_item(item)

    # Export the Resource group template
    print('Export Resource Group Template')
    BODY = {
        'resources': ['*']
    }
    rgTemplate = client.resource_groups.begin_export_template(GROUP_NAME, BODY).result()
    print(rgTemplate.template)
    print('\n\n')

    # Delete Resource group and everything in it
    print('Delete Resource Group')
    client.resource_groups.begin_delete(GROUP_NAME).result()
    print("\nDeleted: {}".format(GROUP_NAME))


def print_item(group):
    """Print ResourceGroup instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    print("\tLocation: {}".format(group.location))
    print("\tTags: {}".format(group.tags))
    print_properties(group.properties)


def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and props.provisioning_state:
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")


if __name__ == "__main__":
    run_example()
