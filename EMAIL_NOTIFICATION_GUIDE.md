# n8n Email Notification Setup Guide

## Overview
This guide explains how to add email notifications to n8n workflows that send full execution logs when failures occur. This is critical for long-running workflows where debugging requires detailed error context.

## Prerequisites

### SMTP Configuration
You'll need to configure an SMTP account in n8n. Common options:

1. **Gmail** (requires App Password)
   - SMTP Host: smtp.gmail.com
   - Port: 465 (SSL) or 587 (TLS)
   - Enable 2FA and create App Password

2. **Outlook/Office365**
   - SMTP Host: smtp.office365.com
   - Port: 587
   - Use your Microsoft account credentials

3. **SendGrid** (recommended for automation)
   - SMTP Host: smtp.sendgrid.com
   - Port: 587
   - Use API key as password

4. **Custom SMTP Server**
   - Configure according to your provider

## Implementation Steps

### Step 1: Add Error Trigger Node

Add this node structure to your workflow:

```json
{
  "name": "ErrorTrigger-001",
  "type": "n8n-nodes-base.errorTrigger",
  "typeVersion": 1,
  "position": [x, y],
  "parameters": {}
}
```

### Step 2: Create Error Log Formatter (Code Node)

This node collects all relevant error information:

```json
{
  "name": "FormatErrorLog-002",
  "type": "n8n-nodes-base.code",
  "typeVersion": 1,
  "position": [x, y],
  "parameters": {
    "mode": "runOnceForAllItems",
    "jsCode": "// Generate timestamp\nconst timestamp = new Date().toISOString();\nconst timestampFile = new Date().toISOString().replace(/:/g, '-').split('.')[0];\n\n// Get workflow information\nconst workflowName = $workflow.name;\nconst workflowId = $workflow.id;\nconst executionId = $execution.id;\n\n// Extract error details\nconst errorNode = $input.first().json.node?.name || 'Unknown Node';\nconst errorMessage = $input.first().json.error?.message || 'No error message';\nconst errorStack = $input.first().json.error?.stack || 'No stack trace';\n\n// Try to get checkpoint data if it exists\nlet checkpointData = 'No checkpoint data available';\ntry {\n  // This assumes you have checkpoint data accessible\n  // Adjust path based on your checkpoint implementation\n  const fs = require('fs');\n  const checkpointPath = `/home/node/.n8n/checkpoint_${workflowId}.json`;\n  if (fs.existsSync(checkpointPath)) {\n    checkpointData = fs.readFileSync(checkpointPath, 'utf8');\n  }\n} catch (e) {\n  checkpointData = `Could not read checkpoint: ${e.message}`;\n}\n\n// Format the complete error log\nconst errorLog = {\n  timestamp: timestamp,\n  workflowName: workflowName,\n  workflowId: workflowId,\n  executionId: executionId,\n  failedNode: errorNode,\n  errorMessage: errorMessage,\n  errorStack: errorStack,\n  checkpointData: checkpointData,\n  emailSubject: `n8n Workflow Failed: ${workflowName} - ${timestamp}`,\n  emailBody: `\n=================================================\nn8n WORKFLOW EXECUTION FAILURE\n=================================================\n\nWorkflow: ${workflowName}\nWorkflow ID: ${workflowId}\nExecution ID: ${executionId}\nTimestamp: ${timestamp}\n\n-------------------------------------------------\nFAILED NODE\n-------------------------------------------------\n${errorNode}\n\n-------------------------------------------------\nERROR MESSAGE\n-------------------------------------------------\n${errorMessage}\n\n-------------------------------------------------\nSTACK TRACE\n-------------------------------------------------\n${errorStack}\n\n-------------------------------------------------\nCHECKPOINT DATA\n-------------------------------------------------\n${checkpointData}\n\n-------------------------------------------------\nEXECUTION DATA\n-------------------------------------------------\n${JSON.stringify($input.all(), null, 2)}\n\n=================================================\nTO DEBUG:\n1. Copy this entire email\n2. Send to Claude Code\n3. Claude will analyze and provide fixes\n=================================================\n  `\n};\n\nreturn [errorLog];"
  }
}
```

### Step 3: Add Send Email Node

Configure the email sender:

```json
{
  "name": "SendErrorEmail-003",
  "type": "n8n-nodes-base.emailSend",
  "typeVersion": 2,
  "position": [x, y],
  "parameters": {
    "fromEmail": "your-n8n-bot@example.com",
    "toEmail": "your-email@example.com",
    "subject": "={{ $json.emailSubject }}",
    "message": "={{ $json.emailBody }}",
    "options": {
      "allowUnauthorizedCerts": false
    }
  },
  "credentials": {
    "smtp": {
      "id": "YOUR_SMTP_CREDENTIAL_ID",
      "name": "Your SMTP Account"
    }
  }
}
```

### Step 4: Connect the Nodes

Add these connections:

```json
{
  "connections": {
    "ErrorTrigger-001": {
      "main": [
        [
          {
            "node": "FormatErrorLog-002",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "FormatErrorLog-002": {
      "main": [
        [
          {
            "node": "SendErrorEmail-003",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## Alternative: Read Checkpoint from Disk

If `require('fs')` is blocked in Code nodes, use this approach:

### Step 2a: Read Checkpoint File (Alternative)

```json
{
  "name": "ReadCheckpoint-002a",
  "type": "n8n-nodes-base.readBinaryFile",
  "typeVersion": 1,
  "position": [x, y],
  "parameters": {
    "filePath": "/home/node/.n8n/checkpoint_{{ $workflow.id }}.json",
    "options": {}
  },
  "continueOnFail": true
}
```

### Step 2b: Format Error Log (Without fs)

```json
{
  "name": "FormatErrorLog-002b",
  "type": "n8n-nodes-base.code",
  "typeVersion": 1,
  "position": [x, y],
  "parameters": {
    "mode": "runOnceForAllItems",
    "jsCode": "const timestamp = new Date().toISOString();\nconst workflowName = $workflow.name;\nconst executionId = $execution.id;\n\nconst errorNode = $('ErrorTrigger-001').first().json.node?.name || 'Unknown';\nconst errorMessage = $('ErrorTrigger-001').first().json.error?.message || 'No error';\nconst errorStack = $('ErrorTrigger-001').first().json.error?.stack || 'No stack';\n\n// Get checkpoint data from previous node\nlet checkpointData = 'No checkpoint available';\ntry {\n  const checkpointInput = $('ReadCheckpoint-002a').first();\n  if (checkpointInput && checkpointInput.binary) {\n    checkpointData = Buffer.from(checkpointInput.binary.data.data).toString('utf8');\n  }\n} catch (e) {\n  checkpointData = `Checkpoint read failed: ${e.message}`;\n}\n\nreturn [{\n  emailSubject: `n8n Failed: ${workflowName} - ${timestamp}`,\n  emailBody: `\nWORKFLOW FAILURE\n================\nWorkflow: ${workflowName}\nTime: ${timestamp}\nExecution: ${executionId}\n\nFailed Node: ${errorNode}\n\nError:\n${errorMessage}\n\nStack Trace:\n${errorStack}\n\nCheckpoint:\n${checkpointData}\n\nSend this entire email to Claude Code for analysis.\n  `\n}];"
  }
}
```

## Setting Up SMTP Credentials in n8n

1. Go to **Settings** → **Credentials** in n8n
2. Click **Add Credential**
3. Select **SMTP** (not "Send Email")
4. Configure:
   - **Credential Name**: e.g., "Gmail SMTP" or "SendGrid"
   - **User**: Your email or username
   - **Password**: Your password or app password
   - **Host**: SMTP server address
   - **Port**: 587 (TLS) or 465 (SSL)
   - **SSL/TLS**: Enable if using port 465
5. Click **Create**
6. Copy the credential ID for use in workflow

## Testing the Email System

### Test Workflow Structure

Create a simple test workflow:

1. Manual Trigger node
2. Function node that throws an error: `throw new Error('Test error for email notification');`
3. Error Trigger + Email notification nodes (as described above)

### Test Execution

1. Execute the workflow manually
2. Verify you receive an email
3. Check that email contains:
   - Workflow name with timestamp
   - Error message
   - Stack trace
   - Execution details

## Integration with Existing Workflows

To add email notifications to existing workflows:

1. **Identify workflow file** (e.g., `screenplay_classifier.json`)
2. **Add Error Trigger node** to workflow nodes array
3. **Add Format Error Log node** to workflow nodes array
4. **Add Send Email node** to workflow nodes array
5. **Update connections** to link Error Trigger → Format → Email
6. **Update workflow metadata**:
   - Update `name` field with timestamp
   - Update filename with timestamp

### Example Workflow Name Update

```json
{
  "name": "Screenplay Classifier - 20251222_1530",
  "nodes": [
    // ... existing nodes ...
    // ... add error handling nodes ...
  ],
  "connections": {
    // ... existing connections ...
    // ... add error handling connections ...
  }
}
```

## Troubleshooting

### Email Not Sending

1. **Check SMTP Credentials**: Verify host, port, username, password
2. **Check Firewall**: Ensure n8n Docker container can access SMTP port
3. **Check Email Provider**: Some require "less secure apps" or app passwords
4. **Check n8n Logs**: View Docker logs for SMTP connection errors

### Code Node `require('fs')` Blocked

- Use the alternative approach with **Read Binary File** node
- This is safer and follows n8n's security model

### Checkpoint Data Not Available

- Ensure checkpoint file path is correct
- Verify permissions on checkpoint directory
- Use `continueOnFail: true` on Read Checkpoint node

### Missing Error Details

- Error Trigger only captures errors from nodes it's connected to
- Ensure Error Trigger is at workflow level (not inside sub-workflows)
- Some nodes may suppress errors - check node settings

## Best Practices

1. **Always use timestamp naming** for workflows and files
2. **Include checkpoint state** in error emails for resume capability
3. **Set up retry logic** before error handling (try 3 times, then email)
4. **Use a dedicated email** for n8n notifications (don't use personal email)
5. **Test email notifications** before running long workflows
6. **Keep email formatting clean** for easy copy-paste to Claude Code
7. **Include execution ID** for n8n UI correlation

## Quick Reference Template

For quick copy-paste, see the complete workflow template in: `email_notification_template.json` (to be created)

## Questions?

When sending error emails to Claude Code, include:
- Full email body (everything)
- Workflow JSON file if available
- Any additional context about what the workflow was doing
- Expected vs. actual behavior

Claude will analyze the logs and provide specific fixes.
