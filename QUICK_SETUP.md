# Quick Setup: Email Notifications for n8n Workflows

## 🎯 What This Does

Automatically sends you a detailed email with full logs when any n8n workflow fails. The email includes everything I (Claude) need to debug and fix the issue.

## ⚡ Quick Start (5 minutes)

### Step 1: Set Up SMTP in n8n

Choose ONE option:

**Option A: Gmail (Easiest)**
1. Go to your Google Account → Security
2. Enable 2-Factor Authentication
3. Generate an App Password: https://myaccount.google.com/apppasswords
4. In n8n: Settings → Credentials → Add Credential → SMTP
   - User: your.email@gmail.com
   - Password: [the 16-character app password]
   - Host: smtp.gmail.com
   - Port: 587
   - Enable SSL/TLS
   - Save and copy the credential ID

**Option B: SendGrid (Best for automation)**
1. Sign up at sendgrid.com (free tier: 100 emails/day)
2. Create API key
3. In n8n: Settings → Credentials → Add Credential → SMTP
   - User: apikey
   - Password: [your SendGrid API key]
   - Host: smtp.sendgrid.com
   - Port: 587
   - Save and copy the credential ID

### Step 2: Import Template Workflow

1. Open `20251222_1530_email_notification_template.json`
2. Find and replace these values:
   - `YOUR_EMAIL@example.com` → your actual email
   - `YOUR_SMTP_CREDENTIAL_ID` → credential ID from Step 1
3. Import to n8n (or copy-paste the JSON)

### Step 3: Test It

1. In the template workflow, uncomment this line in `MainProcessing-002`:
   ```javascript
   throw new Error('Test error - this will trigger email notification');
   ```
2. Execute the workflow
3. Check your email - you should receive a detailed error report

### Step 4: Add to Your Existing Workflows

For any existing workflow, add these 5 nodes from the template:
- `ErrorTrigger-901`
- `ReadCheckpoint-902`
- `FormatErrorLog-903`
- `SendErrorEmail-904`
- `LogEmailSent-905`

Copy the entire error handling chain and paste into your workflow.

## 📝 Workflow Naming Convention (REQUIRED)

Every workflow MUST follow this format:

**Filename:** `YYYYMMDD_HHMM_description.json`
**Workflow Name:** `Description - YYYYMMDD_HHMM`

Example:
- File: `20251222_1530_screenplay_classifier.json`
- Name: `Screenplay Classifier - 20251222_1530`

This makes it easy to track versions and debug issues.

## 🔧 Configuration Checklist

Before running any workflow in production:

- [ ] SMTP credentials configured and tested
- [ ] Email address updated in `SendErrorEmail-904` node
- [ ] Workflow has timestamp in filename AND internal name
- [ ] Error handling nodes added (5 nodes from template)
- [ ] Test email sent and received successfully
- [ ] Checkpoint path correct (if using checkpoints)

## 📧 What's in the Error Email

When a workflow fails, you'll receive an email with:

1. **Workflow identification** (name, ID, execution ID, timestamp)
2. **Failed node name** (exactly where it broke)
3. **Error message** (what went wrong)
4. **Stack trace** (technical details)
5. **Checkpoint data** (where to resume from)
6. **Full execution data** (complete context)
7. **Instructions** (how to send to Claude for fixing)

## 🚀 Using Error Emails with Claude Code

When you get an error email:

1. Copy the **entire email** (Ctrl+A, Ctrl+C)
2. In your Claude Code session, paste and say: "analyze and fix this"
3. I'll:
   - Identify the root cause
   - Provide the exact fix
   - Update your workflow JSON
   - Help you resume from checkpoint if applicable

## 🎓 Full Documentation

- **Detailed Guide:** `EMAIL_NOTIFICATION_GUIDE.md`
- **Template Workflow:** `20251222_1530_email_notification_template.json`
- **Project Context:** `CLAUDE.md`

## ⚠️ Troubleshooting

**Email not sending?**
- Check SMTP credentials are correct
- Test credentials in n8n (edit credential → Test)
- Check n8n Docker container can access internet
- Verify port 587 or 465 not blocked by firewall

**`require('fs')` error in Code node?**
- This is why we use `ReadCheckpoint-902` node instead
- The template already handles this correctly
- Never use `fs` directly in n8n Code nodes

**Checkpoint data missing?**
- Verify checkpoint file path: `/home/node/.n8n/checkpoint_[workflow-id].json`
- Check file permissions
- Node has `continueOnFail: true` so workflow won't break if checkpoint missing

**Email too large?**
- Gmail limit: 25MB
- SendGrid limit: 30MB
- Execution data is usually < 1MB
- If larger, consider truncating execution data in `FormatErrorLog-903`

## 💡 Pro Tips

1. **Use a dedicated email** for n8n notifications (create n8n@yourdomain.com)
2. **Set up email filter** to label n8n errors for easy finding
3. **Test before long runs** - always test error handling on small dataset first
4. **Keep templates** - save working configurations as templates
5. **Version control** - commit workflow JSON to git with timestamps

## 🆘 Need Help?

Send me:
- The error email (full text)
- Workflow JSON file
- What you expected to happen
- Any recent changes you made

I'll analyze and provide specific fixes.

---

**Questions about this setup?** Just ask!
