#!/usr/bin/env python3
import json

# Load workflow
with open('/home/user/Claude/20251225_0029_GDRIVE_Dedup_Ollama_v003_FIXED.json') as f:
    workflow = json.load(f)

# Add merge node between Create Google Doc and Add Content
merge_node = {
    "parameters": {
        "jsCode": "const docResponse = $input.first().json;\nconst originalData = $('Build Document Content').first().json;\n\nreturn [{\n  json: {\n    ...originalData,\n    ...docResponse\n  }\n}];"
    },
    "id": "d99317f9-f01d-470e-9ac0-1f5f71007193",
    "name": "Merge Doc Data",
    "type": "n8n-nodes-base.code",
    "position": [1536, 1344],
    "typeVersion": 2
}

workflow['nodes'].append(merge_node)

# Update connections:
# Create Google Doc → Merge Doc Data → Add Content

# Find and update Create Google Doc connection
for node_name, connections in workflow['connections'].items():
    if node_name == "Create Google Doc":
        # Change connection from Add Content to Merge Doc Data
        workflow['connections']['Create Google Doc'] = {
            "main": [
                [
                    {
                        "node": "Merge Doc Data",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }

# Add Merge Doc Data → Add Content connection
workflow['connections']['Merge Doc Data'] = {
    "main": [
        [
            {
                "node": "Add Content",
                "type": "main",
                "index": 0
            }
        ]
    ]
}

# Write updated workflow
with open('/home/user/Claude/20251225_0029_GDRIVE_Dedup_Ollama_v003_FIXED.json', 'w') as f:
    json.dump(workflow, f, indent=2)

print("✅ Added Merge Doc Data node")
print("✅ Updated connections: Create Google Doc → Merge Doc Data → Add Content")
print("✅ Now $json.content will work in Add Content node")
