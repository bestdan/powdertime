# Setting Up Slack Notifications for Powdertime

This guide walks you through setting up Slack notifications so that powdertime snow alerts are sent directly to your personal Slack channel.

## Overview

Powdertime uses Slack's Incoming Webhooks feature to post messages to your channel. You'll create a Slack app, enable webhooks, choose your channel, and add the webhook URL to GitHub Secrets.

---

## Step 1: Create a Slack App

### 1.1 Go to Slack API Dashboard

1. Open your web browser and go to: https://api.slack.com/apps
2. Click the **"Create New App"** button (green button in top right)

### 1.2 Choose App Creation Method

You'll see two options:
- **"From scratch"** ← Choose this one
- "From an app manifest"

Click **"From scratch"**

### 1.3 Configure Basic App Info

You'll be prompted for:

- **App Name**: Enter something like `Powdertime Snow Alerts` or `Snow Bot`
- **Pick a workspace**: Select your Slack workspace from the dropdown

Click **"Create App"**

---

## Step 2: Enable Incoming Webhooks

### 2.1 Navigate to Incoming Webhooks

After creating your app, you'll be on the app's Basic Information page.

1. In the left sidebar, look for **"Features"** section
2. Click **"Incoming Webhooks"**

### 2.2 Activate Incoming Webhooks

1. You'll see a toggle switch at the top that says **"Activate Incoming Webhooks"**
2. Click the toggle to turn it **ON** (it will turn green)

---

## Step 3: Add Webhook to Your Channel

### 3.1 Add New Webhook to Workspace

1. Scroll down to the **"Webhook URLs for Your Workspace"** section
2. Click the **"Add New Webhook to Workspace"** button

### 3.2 Select Your Channel

You'll be redirected to a permission screen:

1. **Channel Selection**: Click the dropdown menu
2. Choose your personal channel from the list
   - Personal channels appear as `#your-channel-name`
   - Direct messages appear as `@your-name (you)`
   - You can also select any public/private channel you have access to

3. Click **"Allow"** to grant the app permission to post to this channel

### 3.3 Copy Your Webhook URL

After clicking "Allow", you'll be redirected back to the Incoming Webhooks page.

1. Scroll down to **"Webhook URLs for Your Workspace"**
2. You'll see your webhook URL - it looks like:
   ```
   https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
   ```
3. Click the **"Copy"** button to copy the URL to your clipboard

**⚠️ IMPORTANT**: Keep this URL secret! Anyone with this URL can post messages to your channel.

---

## Step 4: Add Webhook URL to GitHub Secrets

### 4.1 Navigate to Repository Settings

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/powdertime`
2. Click the **"Settings"** tab (near the top right)

### 4.2 Access Secrets Configuration

1. In the left sidebar, look for **"Security"** section
2. Click **"Secrets and variables"** to expand it
3. Click **"Actions"**

### 4.3 Create New Secret

1. Click the **"New repository secret"** button (green button)
2. Fill in the form:
   - **Name**: Enter exactly `POWDERTIME_WEBHOOK_URL` (all caps, no spaces)
   - **Secret**: Paste the webhook URL you copied from Slack
3. Click **"Add secret"**

You should see a confirmation message that the secret was added.

---

## Step 5: Test the Integration

### 5.1 Test with curl (Optional)

Before running the full workflow, test that your webhook works:

```bash
curl -X POST YOUR_WEBHOOK_URL_HERE \
  -H "Content-Type: application/json" \
  -d '{
    "text": "🧪 Test message from Powdertime",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Test Alert*\nIf you see this, your webhook is working! ✅"
        }
      }
    ]
  }'
```

Replace `YOUR_WEBHOOK_URL_HERE` with your actual webhook URL.

If successful, you should see this test message appear in your Slack channel immediately.

### 5.2 Test the GitHub Actions Workflow

Now test the full integration:

1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. Click **"Daily Snow Check"** in the left sidebar (under "Workflows")
4. Click the **"Run workflow"** button (gray button on the right)
5. Click **"Run workflow"** in the popup

Wait about 1 minute for the workflow to complete.

**What to expect**:
- ✅ If snow > 4 inches is detected: You'll receive a Slack notification
- ℹ️ If no significant snow: No Slack message (check workflow logs for results)

---

## Step 6: Verify Automated Daily Runs

### 6.1 Check Workflow Schedule

The workflow is configured to run automatically every day at 6 AM Mountain Time (13:00 UTC).

To verify it's enabled:
1. Go to **Actions** → **Daily Snow Check**
2. Look for the schedule indicator (should show next run time)

### 6.2 Monitor Workflow Runs

Check the Actions tab periodically to see workflow history:
- Green checkmark ✅ = Successful run
- Red X ❌ = Failed run (you'll receive email notification)
- Yellow circle 🟡 = Currently running

---

## Understanding Slack Notifications

### What the Message Looks Like

When powdertime detects significant snowfall (4+ inches), you'll receive a Slack message with:

**Example**:
```
❄️ POWDER ALERT! Significant Snow Forecasted ❄️

Found 2 location(s) with significant snowfall:

1. Hunter Mountain (NY): 8.5 inches total
   Period: 2026-01-15 to 2026-01-17
   Max daily: 4.2 inches

2. Killington (VT): 6.0 inches total
   Period: 2026-01-16 to 2026-01-18
   Max daily: 3.5 inches
```

### Notification Payload Structure

The webhook sends JSON with this structure:
```json
{
  "alert_type": "powder_alert",
  "event_count": 2,
  "events": [
    {
      "resort_name": "Hunter Mountain",
      "resort_state": "NY",
      "total_snowfall_inches": 8.5,
      "max_daily_snowfall_inches": 4.2,
      "start_date": "2026-01-15",
      "end_date": "2026-01-17"
    }
  ]
}
```

**Note**: The current implementation sends the JSON payload directly. If you want formatted Slack messages with blocks and formatting, you can customize the webhook payload in `powdertime/notifier.py`.

---

## Troubleshooting

### Issue: "No webhook URL configured" Error

**Cause**: The GitHub Secret isn't set or is named incorrectly.

**Solution**:
1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Verify the secret is named exactly: `POWDERTIME_WEBHOOK_URL`
3. If missing or wrong name, delete and recreate it

### Issue: Webhook Returns 404 Error

**Cause**: The webhook URL is invalid or the Slack app was deleted.

**Solution**:
1. Go back to https://api.slack.com/apps
2. Select your Powdertime app
3. Go to Incoming Webhooks
4. Copy the webhook URL again (make sure it's complete)
5. Update the GitHub Secret with the new URL

### Issue: Messages Not Appearing in Slack

**Possible causes and solutions**:

1. **Wrong channel selected**
   - Go to Slack API → Your App → Incoming Webhooks
   - Check which channel the webhook is posting to
   - If wrong, remove the webhook and add a new one to correct channel

2. **Slack notifications muted**
   - Check your Slack notification settings
   - Ensure the channel isn't muted

3. **No snow detected**
   - Check GitHub Actions logs
   - Look for "No significant snowfall forecasted" message
   - Lower threshold in `config.github-actions.yaml` if needed:
     ```yaml
     snow_threshold:
       min_inches: 2  # Lower threshold for more alerts
     ```

### Issue: Workflow Fails with "Permission denied"

**Cause**: GitHub Actions doesn't have permission to read secrets.

**Solution**:
1. Go to repo Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Ensure "Read and write permissions" is selected
4. Click "Save"

### Issue: Want to Change Target Channel

**Solution**:
1. Go to https://api.slack.com/apps
2. Select your Powdertime app
3. Click "Incoming Webhooks"
4. Scroll to "Webhook URLs for Your Workspace"
5. Click "Add New Webhook to Workspace"
6. Select new channel
7. Copy the new webhook URL
8. Update GitHub Secret with new URL

---

## Customizing Notifications

### Change Alert Threshold

Edit `config.github-actions.yaml`:
```yaml
snow_threshold:
  min_inches: 6  # Only alert for 6+ inches
```

Commit and push the change.

### Change Monitored Resorts

Edit `config.github-actions.yaml`:
```yaml
resorts:
  - name: "Hunter"
  - name: "Killington"
  - name: "Stowe"
  # Add more from available list in CLAUDE.md
```

### Change Notification Frequency

Edit `.github/workflows/daily-snow-check.yml`:
```yaml
schedule:
  - cron: '0 13,20 * * *'  # Twice daily: 6 AM and 1 PM MT
```

---

## Advanced: Formatting Slack Messages

If you want rich formatted Slack messages (with sections, buttons, colors), you'll need to modify the webhook payload in `powdertime/notifier.py` to use Slack's [Block Kit](https://api.slack.com/block-kit).

Example formatted message:
```python
payload = {
    "text": "Powder Alert!",
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "❄️ Powder Alert!"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{event.resort.name}* ({event.resort.state})\n*{event.total_snowfall:.1f} inches* forecasted"
            }
        }
    ]
}
```

See Slack's [Block Kit Builder](https://app.slack.com/block-kit-builder) for designing custom layouts.

---

## Security Best Practices

1. **Never commit webhook URLs**: Always use GitHub Secrets
2. **Rotate webhooks periodically**: Create new webhooks every 6-12 months
3. **Limit app permissions**: Only grant webhook posting (no reading messages)
4. **Monitor webhook usage**: Check Slack app dashboard for suspicious activity
5. **Use private repository**: Keep your config and webhook setup private

---

## FAQ

### Q: Can I send to multiple channels?

A: Not directly with one webhook. Options:
1. Create multiple webhooks (one per channel) and call them sequentially
2. Use a Slack bot with `chat.postMessage` API (more complex)
3. Use a single channel and mention users with `@username`

### Q: Can I send to direct messages?

A: Yes! When adding the webhook to workspace, select "Slackbot" or your own DM channel from the dropdown.

### Q: Will this work with Slack free tier?

A: Yes! Incoming Webhooks work on all Slack plans including free.

### Q: How many messages will I receive?

A: Only when significant snow (4+ inches by default) is detected at one or more resorts. If no snow, no message is sent. Typically 0-3 alerts per week during ski season.

### Q: Can I use this with Slack Enterprise Grid?

A: Yes, but you may need admin approval to create apps. Contact your Slack workspace admin.

---

## Next Steps

✅ Slack app created
✅ Incoming webhook enabled
✅ Channel selected
✅ Webhook URL copied
✅ GitHub Secret configured
✅ Workflow tested

**You're all set!** You'll start receiving powder alerts at 6 AM MT daily whenever significant snow is forecasted at your monitored resorts.

---

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section above
2. Review GitHub Actions logs for error messages
3. Test webhook with curl to isolate the issue
4. Verify GitHub Secret is named correctly: `POWDERTIME_WEBHOOK_URL`

For Slack-specific issues, see:
- [Slack API Documentation](https://api.slack.com/messaging/webhooks)
- [Slack API Community](https://api.slack.com/community)
