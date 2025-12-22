# Gmail SMTP Setup for n8n - Quick Guide

## Your Configuration
- **Email:** mac.caruso@gmail.com
- **Workflow:** 20251222_1038_LADV_Dedup_Ollama.json
- **Status:** Email address configured ✓ | SMTP credential needs setup

## Step-by-Step SMTP Setup in n8n

### 1. Create Gmail App Password (5 minutes)

Since you have Gmail, you need an **App Password** (not your regular password):

1. Go to: https://myaccount.google.com/apppasswords
2. You'll be asked to sign in with your regular password
3. Click "Select app" → Choose "Mail"
4. Click "Select device" → Choose "Other (Custom name)"
5. Type: "n8n workflow notifications"
6. Click **Generate**
7. **COPY THE 16-CHARACTER PASSWORD** (it will look like: `abcd efgh ijkl mnop`)
8. Save it somewhere safe - you'll need it in the next step

### 2. Configure SMTP Credential in n8n

1. Open your n8n instance
2. Click **Settings** (gear icon) → **Credentials**
3. Click **Add Credential**
4. Search for and select **SMTP**
5. Fill in these values:

```
Credential Name: Gmail SMTP
User: mac.caruso@gmail.com
Password: [paste the 16-character app password from step 1]
Host: smtp.gmail.com
Port: 587
SSL/TLS: Enable (check the box)
```

6. Click **Create**
7. **COPY THE CREDENTIAL ID** (it will be shown in the credentials list - something like "XYz123AbC456")

### 3. Update Workflow with Credential ID

1. Open the workflow file: `20251222_1038_LADV_Dedup_Ollama.json`
2. Find line 619: `"id": "YOUR_SMTP_CREDENTIAL_ID"`
3. Replace `YOUR_SMTP_CREDENTIAL_ID` with the actual ID from step 2.7
4. Save the file

### 4. Import to n8n

1. In n8n, click **Workflows** → **Add Workflow**
2. Click the **three dots menu** (⋮) → **Import from File**
3. Select: `20251222_1038_LADV_Dedup_Ollama.json`
4. Click **Import**

### 5. Test Email Notifications

Create a simple test workflow:

1. **Manual Trigger** node
2. **Code** node with this code:
   ```javascript
   throw new Error('Test error for email notification');
   ```
3. Add the 5 error notification nodes from the template
4. Execute the workflow
5. **Check your email** (mac.caruso@gmail.com)

You should receive an email with subject: "🚨 n8n Workflow Failed: [workflow name] - [timestamp]"

## Quick Reference

**Email configured in workflow:**
- From: n8n-bot@gmail.com
- To: mac.caruso@gmail.com ✓

**Gmail SMTP Settings:**
```
Host: smtp.gmail.com
Port: 587
SSL/TLS: Enabled
User: mac.caruso@gmail.com
Password: [16-char app password]
```

## Troubleshooting

**"Less secure app access" error:**
- This is old Gmail terminology
- Use App Password instead (see step 1 above)

**Can't find App Passwords option:**
- Make sure 2-Factor Authentication is enabled on your Google Account
- App Passwords only show up when 2FA is enabled

**Email not sending:**
- Check n8n Docker logs: `docker logs n8n`
- Verify SMTP credential is saved correctly
- Test credential by editing it and clicking "Test"
- Check Gmail "Sent" folder to confirm emails sent

**Email goes to spam:**
- This is normal for first few emails
- Mark as "Not Spam" in Gmail
- Set up filter to always deliver to inbox

## What Happens When Workflow Fails

1. Workflow error occurs
2. ErrorTrigger-901 catches it
3. Reads PostgreSQL checkpoint data
4. Formats comprehensive error report
5. Sends email to mac.caruso@gmail.com with:
   - Failed node name
   - Error message
   - Stack trace
   - Checkpoint data
   - Full execution logs
   - Instructions for Claude Code debugging
6. You copy the email and send to Claude Code
7. Claude analyzes and provides fixes

## Password Security Note

⚠️ **IMPORTANT:**
- Your Gmail password (`Wh08m1..2019?!`) should NEVER be put in workflow files
- Only the App Password goes into n8n SMTP credentials
- The workflow file only references the credential ID
- Never commit passwords to git repositories

---

**Ready to go!** Just complete the SMTP setup above and you're all set.

File ready for import: `20251222_1038_LADV_Dedup_Ollama.json`
