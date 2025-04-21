import json
from pathlib import Path

# Define project folders
project_path = Path.cwd()
schema_path = project_path / "schema"
flows_path = project_path / "flows"
scripts_path = project_path / "scripts"

# Create necessary directories
for path in [schema_path, flows_path, scripts_path]:
    path.mkdir(parents=True, exist_ok=True)

# --------------------
# 1. Power Automate Flow Definition
# --------------------
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

# Write flow core files
(project_path / "definition.json").write_text(json.dumps(definition, indent=2))
(project_path / "manifest.json").write_text(json.dumps(manifest, indent=2))
(project_path / "README.md").write_text(
    "# PD Geek: Project Folder Creation Flow\n\n"
    "This Power Automate flow creates a structured set of folders in SharePoint "
    "for each new project added to the ProjectTracker Dataverse table."
)

# --------------------
# 2. Extended Flow Logic Description (for documentation or GitOps)
# --------------------
flow_logic = {
    "name": "AutomatedFolderCreation",
    "trigger": "Dataverse: When a row is added to ProjectTracker",
    "actions": [
        "Create folder: /Projects/{Title}",
        "Create subfolder: Proposals",
        "Create subfolder: Contracts",
        "Create subfolder: Subcontractors",
        "Create subfolder: Subcontractors/Across Industries",
        "Create subfolder: Subcontractors/C-J Systems",
        "Create subfolder: Invoices",
        "Create subfolder: Photos & As-Builts",
        "Create subfolder: Closeout Docs"
    ],
    "notification": "Send Teams or Email confirmation"
}
(flows_path / "automated-folder-creation.json").write_text(json.dumps(flow_logic, indent=2))

# --------------------
# 3. Dataverse Schema: ProjectTracker Table
# --------------------
project_tracker_schema = {
    "name": "ProjectTracker",
    "displayName": "Project Tracker",
    "description": "Tracks AV and MSP projects for PD Geek",
    "fields": [
        {"name": "Title", "type": "Text", "isPrimary": True},
        {"name": "Client", "type": "Text"},
        {"name": "Status", "type": "Choice", "choices": ["Planning", "Active", "Completed", "On Hold", "Cancelled"]},
        {"name": "KickoffDate", "type": "DateOnly"},
        {"name": "SubcontractorAssigned", "type": "Text"},
        {"name": "EstimatedLabor", "type": "Number"},
        {"name": "PermitsRequired", "type": "Boolean"},
        {"name": "LinkedQuoteID", "type": "Text"},
        {"name": "AutoFolderCreated", "type": "Boolean"}
    ]
}
(schema_path / "ProjectTracker.table.json").write_text(json.dumps(project_tracker_schema, indent=2))

# --------------------
# 4. Deployment Scripts
# --------------------
powershell_script = '''\
# PowerShell script to import solution using Power Platform CLI
pac auth create --url https://yourorg.crm.dynamics.com
pac solution import --path ./ --publisher-name "PD Geek" --overwrite
'''

bash_script = '''\
#!/bin/bash
# Shell script to import solution using Power Platform CLI
pac auth create --url https://yourorg.crm.dynamics.com
pac solution import --path ./ --publisher-name "PD Geek" --overwrite
'''

(scripts_path / "deploy.ps1").write_text(powershell_script)
(scripts_path / "deploy.sh").write_text(bash_script)

print("✅ Project folder structure and automation files created successfully.")
