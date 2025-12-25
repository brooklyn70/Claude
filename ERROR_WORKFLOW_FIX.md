# Why Email Notifications Didn't Work in v001/v002

## The Problem

When a workflow **CRASHES** (like with the insertText error), n8n **STOPS EXECUTION IMMEDIATELY**.

Any email nodes inside the workflow **NEVER RUN** because the workflow is dead.

## What You Had in v001/v002

You probably had email notification nodes inside the workflow, but they were unreachable when the workflow crashed at the "Add Content" node.

## The Real Fix: n8n Error Workflow

n8n has a separate feature called **Error Workflows** that run OUTSIDE the failed workflow.

### How to Set It Up:

1. **Create a new workflow** called "Error Notification Workflow"
2. **Add these nodes:**
   - Error Trigger node (n8n-nodes-base.errorTrigger)
   - Gmail node to send email

3. **In your main workflow settings:**
   - Go to Workflow Settings
   - Set "Error Workflow" to "Error Notification Workflow"

4. **Now when ANY workflow fails:**
   - Error Notification Workflow triggers automatically
   - You get an email with the error details

## Alternative: Workflow Execution Events via n8n API

If you have n8n Enterprise or self-hosted, you can also:
- Use webhooks on workflow completion/failure
- Set up external monitoring
- Use n8n's built-in notification settings (if available)

## Why In-Workflow Emails Don't Work for Crashes

```
Workflow Start → ... → [CRASH HERE] → Email Node (NEVER REACHED)
```

The workflow dies at the crash. Email node never executes.

## Why Error Workflow DOES Work

```
Main Workflow: Start → ... → [CRASH]
                                ↓
Error Workflow: [AUTO TRIGGERED] → Email Node → ✓ Email Sent
```

Error Workflow is a separate execution triggered by n8n when main workflow fails.

