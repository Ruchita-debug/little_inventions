from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from dotenv import load_dotenv
import os

load_dotenv()
# Azure credentials
TENANT_ID = os.environ.get("AZURE_TENANT_ID")
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID")
RESOURCE_GROUP_NAME = os.environ.get("RESOURCE_GROUP")

# Authenticate to Azure
credential = ClientSecretCredential(
    tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

compute_client = ComputeManagementClient(
    credential=credential, subscription_id=SUBSCRIPTION_ID
)


# List all Virtual Machines in the specified subscription
def list_virtual_machines():
    str_ = ""
    d = dict()

    for i, vm in enumerate(compute_client.virtual_machines.list_all()):
        str_ += f"{i}: {vm.name}\n"
        d[i] = vm.name

    return str_, d


def get_current_state(vm_name):
    vm = compute_client.virtual_machines.get(
        RESOURCE_GROUP_NAME, vm_name, expand="instanceView"
    )
    vm_status = vm.instance_view.statuses[1].display_status

    return vm_status


vm_list, vm_dict = list_virtual_machines()

try:
    inp = int(input(f"Select your VM from below list:\n{vm_list}"))
    VM_NAME = vm_dict[inp]
    print(f"\nCURRENT STATE({VM_NAME}): {get_current_state(VM_NAME)}\n")
    try:
        action_ip = int(
            input("Select an action on VM:\n1: Start\n2: Stop\n3. No Action\n")
        )
        # Perform the action on the VM
        if action_ip == 1:
            print(f"\nStarting virtual machine... {VM_NAME}")
            compute_client.virtual_machines.begin_start(
                RESOURCE_GROUP_NAME, VM_NAME
            ).result()
        elif action_ip == 2:
            print(f"\nStopping virtual machine... {VM_NAME}")
            compute_client.virtual_machines.begin_power_off(
                RESOURCE_GROUP_NAME, VM_NAME
            ).result()
        elif action_ip == 3:
            print("No action taken!")
        else:
            print("Invalid action specified.")

        print(f"\nCURRENT STATE({VM_NAME}): {get_current_state(VM_NAME)}")
    except ValueError as e:
        print("Select an appropriate action for your VM.", e)
    except:
        print("Some error occured!")
except ValueError as e:
    print("Select an appropriate option for your VM.", e)
except:
    print("Some error occured!")
