import json

definition = {
    "definition": {
        "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
        "triggers": {
            "When_a_row_is_added": {
                "type": "OpenApiConnectionWebhook",
                "inputs": {
                    "host": {
                        "connectionName": "shared_commondataserviceforapps",
                        "operationId": "SubscribeWebhookTrigger",
                        "apiId": "/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps"
                    },
                    "parameters": {
                        "entityName": "ProjectTracker",
                        "scope": "organization"
                    }
                }
            }
        },
        "actions": {},
        "contentVersion": "1.0.0.0"
    }
}

manifest = {
    "packageVersion": "1.0.0.0",
    "creator": "PD Geek Automations",
    "sourceEnvironment": "Default-PDGeek",
    "flows": [
        {
            "name": "Create_Project_Folder_Structure",
            "displayName": "Create Project Folder Structure",
            "description": "Automatically create project folder structure in SharePoint for new projects.",
            "definition": "definition.json"
        }
    ]
}

with open("definition.json", "w") as f:
    json.dump(definition, f, indent=2)

with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

with open("README.md", "w") as f:
    f.write("# PD Geek: Project Folder Creation Flow\n\nThis Power Automate flow creates a structured set of folders in SharePoint for each new project added to the ProjectTracker Dataverse table.")
