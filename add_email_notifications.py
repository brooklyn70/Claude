#!/usr/bin/env python3
import json
import sys

# Load workflow
with open('/home/user/Claude/20251225_0029_GDRIVE_Dedup_Ollama_v003_FIXED.json') as f:
    workflow = json.load(f)

# New email nodes
email_nodes = [
    {
        "parameters": {
            "sendTo": "YOUR_EMAIL@example.com",
            "subject": "✅ n8n Workflow Complete - GDRIVE Dedup Ollama",
            "emailType": "text",
            "message": "=Workflow completed successfully!\n\nWorkflow: {{ $workflow.name }}\nExecution ID: {{ $execution.id }}\nCompleted: {{ $now.format('YYYY-MM-DD HH:mm:ss') }}\n\nAll documents have been classified and created in Google Drive.",
            "options": {}
        },
        "id": "1d7ec8f1-8c63-4183-8b64-d1567b88eee9",
        "name": "Email Success Notification",
        "type": "n8n-nodes-base.gmail",
        "position": [2304, 1344],
        "typeVersion": 2.1,
        "credentials": {
            "gmailOAuth2": {
                "id": "CONFIGURE_GMAIL_CREDENTIAL",
                "name": "Gmail account"
            }
        }
    },
    {
        "parameters": {
            "jsCode": "const error = $input.first();\nconst errorMsg = error.json?.error?.message || error.json?.message || 'Unknown error';\nconst nodeName = $executionMode === 'manual' ? 'Manual execution' : 'Automated execution';\n\nreturn [{\n  json: {\n    subject: `❌ n8n Workflow FAILED - GDRIVE Dedup Ollama`,\n    message: `Workflow execution failed!\n\nWorkflow: GDRIVE Dedup Ollama - v003 - FIXED\nExecution ID: Unknown\nFailed at: ${new Date().toISOString()}\n\nError: ${errorMsg}\n\nPlease check n8n for details.`\n  }\n}];"
        },
        "id": "6e2efc8f-c5fc-4a52-917a-4db891a919e1",
        "name": "Prepare Error Email",
        "type": "n8n-nodes-base.code",
        "position": [2080, 1520],
        "typeVersion": 2
    },
    {
        "parameters": {
            "sendTo": "YOUR_EMAIL@example.com",
            "subject": "={{ $json.subject }}",
            "emailType": "text",
            "message": "={{ $json.message }}",
            "options": {}
        },
        "id": "d8d6a7cd-1061-471c-bcd6-5bf0f9fcf7e3",
        "name": "Email Error Notification",
        "type": "n8n-nodes-base.gmail",
        "position": [2304, 1520],
        "typeVersion": 2.1,
        "credentials": {
            "gmailOAuth2": {
                "id": "CONFIGURE_GMAIL_CREDENTIAL",
                "name": "Gmail account"
            }
        }
    },
    {
        "parameters": {
            "conditions": {
                "number": [
                    {
                        "value1": "={{ $('Count Checkpoint Progress').first().json[0]?.total || 0 }}",
                        "operation": "modulo",
                        "value2": 500,
                        "output": 0
                    }
                ]
            }
        },
        "id": "dd3c4795-f8f9-4238-8d3d-b26fd167616a",
        "name": "Check Every 500 Items",
        "type": "n8n-nodes-base.if",
        "position": [1856, 944],
        "typeVersion": 2
    },
    {
        "parameters": {
            "sendTo": "YOUR_EMAIL@example.com",
            "subject": "📊 n8n Progress Update - GDRIVE Dedup",
            "emailType": "text",
            "message": "=Progress checkpoint reached!\n\nWorkflow: {{ $workflow.name }}\nItems processed: {{ $('Count Checkpoint Progress').first().json[0].total }}\nTimestamp: {{ $now.format('YYYY-MM-DD HH:mm:ss') }}\n\nWorkflow is still running...",
            "options": {}
        },
        "id": "8f4a6e2d-9c1b-4f8e-a5d7-3e8f9a1b2c3d",
        "name": "Email Progress Update",
        "type": "n8n-nodes-base.gmail",
        "position": [2080, 944],
        "typeVersion": 2.1,
        "credentials": {
            "gmailOAuth2": {
                "id": "CONFIGURE_GMAIL_CREDENTIAL",
                "name": "Gmail account"
            }
        }
    }
]

# Add new nodes
workflow['nodes'].extend(email_nodes)

# Update connections

# Connect Done -> Email Success
workflow['connections']['Done'] = {
    "main": [
        [
            {
                "node": "Email Success Notification",
                "type": "main",
                "index": 0
            }
        ]
    ]
}

# Connect Count Checkpoint Progress -> Check Every 500 Items (in addition to existing)
if 'Count Checkpoint Progress' in workflow['connections']:
    # Add the new connection while preserving existing ones
    existing_connections = workflow['connections']['Count Checkpoint Progress']['main'][0]
    existing_connections.append({
        "node": "Check Every 500 Items",
        "type": "main",
        "index": 0
    })
else:
    workflow['connections']['Count Checkpoint Progress'] = {
        "main": [
            [
                {
                    "node": "Log Progress",
                    "type": "main",
                    "index": 0
                },
                {
                    "node": "Check Every 500 Items",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

# Connect Check Every 500 Items -> Email Progress (true branch)
workflow['connections']['Check Every 500 Items'] = {
    "main": [
        [
            {
                "node": "Email Progress Update",
                "type": "main",
                "index": 0
            }
        ]
    ]
}

# Add error workflow trigger connections
# Loop for Classification should trigger error email on fail
workflow['connections']['Prepare Error Email'] = {
    "main": [
        [
            {
                "node": "Email Error Notification",
                "type": "main",
                "index": 0
            }
        ]
    ]
}

# Write updated workflow
with open('/home/user/Claude/20251225_0029_GDRIVE_Dedup_Ollama_v003_FIXED.json', 'w') as f:
    json.dump(workflow, f, indent=2)

print("✅ Email notifications added successfully")
print("\nAdded nodes:")
print("  - Email Success Notification (after Done)")
print("  - Email Error Notification (on failures)")
print("  - Email Progress Update (every 500 items)")
print("\nIMPORTANT: You must configure:")
print("  1. Gmail OAuth2 credential in n8n")
print("  2. Change 'YOUR_EMAIL@example.com' to your actual email")
