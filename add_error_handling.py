#!/usr/bin/env python3
import json

# Load workflow
with open('/home/user/Claude/20251225_0029_GDRIVE_Dedup_Ollama_v003_FIXED.json') as f:
    workflow = json.load(f)

# Find critical nodes and add error handling
critical_nodes = [
    "Classify with Ollama",
    "Create Google Doc",
    "Add Content",
    "Execute a SQL query"
]

for node in workflow['nodes']:
    if node['name'] in critical_nodes:
        # Enable continueOnFail so errors are passed to next node
        node['continueOnFail'] = True
        node['onError'] = 'continueErrorOutput'
        print(f"✓ Added error handling to: {node['name']}")

# Add error detection node after classification loop
error_detector_node = {
    "parameters": {
        "conditions": {
            "boolean": [
                {
                    "value1": "={{ $json.error !== undefined || $json.code === 400 || $json.code === 500 }}",
                    "value2": True
                }
            ]
        }
    },
    "id": "3f7b8c9d-1e2f-4a5b-9c8d-7e6f5a4b3c2d",
    "name": "Detect Errors",
    "type": "n8n-nodes-base.if",
    "position": [1424, 944],
    "typeVersion": 2
}

workflow['nodes'].append(error_detector_node)

# Add connection from Classify with Ollama to Detect Errors (error branch)
# We need to update the Classify with Ollama node to have an error output

# Find and update connections
# Parse Classification should check for errors and route to error handler
for node in workflow['nodes']:
    if node['name'] == "Parse Classification":
        # Update the code to detect and handle errors
        old_code = node['parameters']['jsCode']
        new_code = '''const response = $input.first().json;
const paraData = $('Prepare Classification').first().json;

// Check for errors from previous node
if (response.error || response.code >= 400) {
  console.error('❌ Classification API error:', response.error || response.message);
  return [{ json: {
    error: true,
    errorMessage: response.error?.message || response.message || 'Classification failed',
    sourceFile: paraData.sourceFile,
    category: 'ERROR',
    episodeNum: null
  } }];
}

let category = 'OTHER';
let episodeNum = null;

try {
  // Ollama returns response.response field
  const rawContent = response.response || '';
  const answer = String(rawContent).trim().toUpperCase();

  if (answer.includes('SCENE')) {
    category = 'SCENE';
    const epMatch = paraData.sourceFile.match(/e?(\\d{1,2})/i) || paraData.paragraphText.match(/episode\\s+(\\d{1,2})/i);
    if (epMatch) episodeNum = parseInt(epMatch[1]);
  } else if (answer.includes('EPISODE')) {
    category = 'EPISODE';
    const epMatch = paraData.sourceFile.match(/e?(\\d{1,2})/i) || paraData.paragraphText.match(/episode\\s+(\\d{1,2})/i);
    if (epMatch) episodeNum = parseInt(epMatch[1]);
  }

  // Log progress every 50 items
const loopNode = $('Loop for Classification');
const currentBatch = loopNode.context?.nodesExecuted || 0;
if (currentBatch > 0 && currentBatch % 50 === 0) {
  console.log(`💾 Progress: ${currentBatch} items processed`);
}

console.log('Classified:', category, episodeNum ? `E${episodeNum}` : '');
} catch (e) {
  console.error('Error:', e.message);
  return [{ json: {
    error: true,
    errorMessage: e.message,
    sourceFile: paraData.sourceFile,
    category: 'ERROR',
    episodeNum: null
  } }];
}

return [{ json: {
  sourceFile: paraData.sourceFile,
  paragraphText: paraData.paragraphText,
  category,
  episodeNum,
  error: false
} }];'''

        node['parameters']['jsCode'] = new_code
        print(f"✓ Updated error detection in: {node['name']}")

# Add error counter and email trigger
error_counter_node = {
    "parameters": {
        "jsCode": '''const items = $input.all();
const errors = items.filter(item => item.json.error === true);
const errorCount = errors.length;
const totalCount = items.length;

console.log(`⚠️  Errors detected: ${errorCount} of ${totalCount} items`);

if (errorCount > 0) {
  const errorMessages = errors.slice(0, 10).map(e =>
    `- ${e.json.sourceFile}: ${e.json.errorMessage}`
  ).join('\\n');

  return [{ json: {
    hasErrors: true,
    errorCount,
    totalCount,
    errorRate: (errorCount / totalCount * 100).toFixed(2),
    errorSample: errorMessages,
    timestamp: new Date().toISOString()
  }}];
}

return [];'''
    },
    "id": "9a8b7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d",
    "name": "Check For Errors",
    "type": "n8n-nodes-base.code",
    "position": [1200, 1520],
    "typeVersion": 2
}

workflow['nodes'].append(error_counter_node)

# Connect Loop for Classification completion to error checker
if 'Loop for Classification' in workflow['connections']:
    # When loop completes (output 0), also check for errors
    existing = workflow['connections']['Loop for Classification']['main'][0]
    existing.append({
        "node": "Check For Errors",
        "type": "main",
        "index": 0
    })

# Connect error checker to error email
workflow['connections']['Check For Errors'] = {
    "main": [
        [
            {
                "node": "Prepare Error Email",
                "type": "main",
                "index": 0
            }
        ]
    ]
}

# Update Prepare Error Email to use the error data
for node in workflow['nodes']:
    if node['name'] == "Prepare Error Email":
        node['parameters']['jsCode'] = '''const errorData = $input.first().json;

let message;
if (errorData.hasErrors) {
  message = `Workflow completed with ERRORS!

Workflow: GDRIVE Dedup Ollama - v003
Execution ID: Unknown
Timestamp: ${errorData.timestamp}

Error Summary:
- Total items: ${errorData.totalCount}
- Failed items: ${errorData.errorCount}
- Error rate: ${errorData.errorRate}%

Sample errors:
${errorData.errorSample}

Please check n8n for full details.`;
} else {
  const error = errorData.error || {};
  message = `Workflow execution failed!

Workflow: GDRIVE Dedup Ollama - v003
Failed at: ${new Date().toISOString()}

Error: ${error.message || 'Unknown error'}

Please check n8n for details.`;
}

return [{
  json: {
    subject: `❌ n8n Workflow ERROR - GDRIVE Dedup Ollama`,
    message: message
  }
}];'''
        print(f"✓ Updated: {node['name']}")

# Write updated workflow
with open('/home/user/Claude/20251225_0029_GDRIVE_Dedup_Ollama_v003_FIXED.json', 'w') as f:
    json.dump(workflow, f, indent=2)

print("\n✅ Error handling added successfully")
print("\nError handling features:")
print("  - Critical nodes continue on error")
print("  - Errors are detected and counted")
print("  - Email sent if errors occur during processing")
print("  - Error rate and sample errors included in notification")
