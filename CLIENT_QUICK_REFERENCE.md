# Quick Reference Card for Clients

## What is LinkedIn Automation?

This system **automatically generates and posts professional crypto content** to your LinkedIn profile on a schedule you choose.

✓ Generates posts using AI  
✓ Posts automatically at your scheduled time  
✓ Maintains content quality and engagement  
✓ No manual work required  

---

## Getting Started (30 minutes)

### Step 1: Install (5 minutes)
**Windows:**
- Download Docker Desktop: https://docker.com/products/docker-desktop
- Double-click `setup.bat`

**Mac/Linux:**
- Download Docker Desktop: https://docker.com/products/docker-desktop
- Run: `bash setup.sh`

### Step 2: Get API Keys (10 minutes)

**Option A: Google Gemini (Free)**
- Go to: https://aistudio.google.com/app/apikeys
- Click "Create API Key"
- Copy the key

**Option B: Anthropic Claude (Paid)**
- Go to: https://console.anthropic.com
- Create account & get API key
- Add billing method

### Step 3: Get LinkedIn Credentials (10 minutes)
- Go to: https://linkedin.com/developers/apps
- Create new app (takes 2-3 days for approval)
- Once approved, get these:
  - **Access Token**
  - **Your LinkedIn ID** (looks like: `vvQE2g2rkz`)
  - **Client ID**
  - **Client Secret**

### Step 4: Configure Dashboard (5 minutes)
- Open: http://localhost:5000
- Go to "Setup" tab
- Paste your API keys
- Click "Test" buttons
- Go to "Schedule" tab
- Set posting time
- Uncheck "Test Mode"

---

## How It Works

```
Every day at your scheduled time:
  1. AI generates a professional LinkedIn post
  2. Adds relevant hashtags
  3. Posts to your LinkedIn profile
  4. Records post history
```

**That's it!** No manual work. Just set it once and it runs forever.

---

## Dashboard Tabs Explained

| Tab | What It Does |
|-----|-------------|
| **Setup** | Add API keys and LinkedIn credentials |
| **Generate Post** | Preview posts before they go live |
| **Post History** | See all posts that were published |
| **Schedule** | Set posting time and enable/disable |

---

## FAQ

**Q: Do I need to know coding?**
A: No! Dashboard is completely visual. No code required.

**Q: How much does it cost?**
A: Usually $10-20/month for hosting + AI API
- Free: Google Gemini API (20 posts/day limit)
- Paid: Anthropic ($1-5/month), OpenAI ($5-20/month)

**Q: How often are posts generated?**
A: You choose! Setup tab → Schedule → pick time.

**Q: Can I edit posts before they post?**
A: Yes! Go to "Generate Post" tab, review, then enable posting.

**Q: What if I want to stop?**
A: Just uncheck "Test Mode" in Schedule tab. Or run:
```
docker-compose down
```

**Q: What if the system breaks?**
A: Run this command:
```
docker-compose down
docker-compose up
```

**Q: Can I change the posting schedule?**
A: Yes! Just change the time in Schedule tab. Takes effect immediately.

**Q: Who has access to my LinkedIn account?**
A: Only your system (running on your computer/server). Your credentials never leave your machine.

---

## Getting Help

**Dashboard isn't loading?**
- Make sure Docker is running (Windows: Docker Desktop app)
- Restart: Run `docker-compose down` then `setup.bat` (or `setup.sh`)

**API keys not working?**
- Copy-paste your key exactly (no extra spaces)
- Click "Test API Connection" to verify

**LinkedIn posts not appearing?**
- Check "Test Mode" is **unchecked** in Schedule tab
- Verify LinkedIn token is correct
- Check post history tab

**Want to change content style?**
- Go to "Setup" tab
- Change "Content Profile" (if available)
- Or contact support to customize

---

## Cost Breakdown

| Component | Cost/Month |
|-----------|-----------|
| Hosting | $0-15 |
| AI API | $0-20 |
| LinkedIn (free) | $0 |
| **Total** | **$0-35** |

Most clients spend **$10-20/month**.

---

## Next Steps

1. ☐ Install Docker Desktop
2. ☐ Run setup.bat / setup.sh
3. ☐ Get Google Gemini or Anthropic API key
4. ☐ Get LinkedIn app credentials
5. ☐ Open http://localhost:5000
6. ☐ Configure all API keys
7. ☐ Test connections
8. ☐ Set posting schedule
9. ☐ Uncheck "Test Mode"
10. ☐ Start generating posts!

---

## Support Contact

If you get stuck, provide this information:
1. **Operating System:** Windows / Mac / Linux
2. **Docker version:** Run `docker --version`
3. **Error message:** Copy-paste the error text
4. **What were you trying to do:** Describe the action

Email: support@arabglobalcrypto.com

---

## Keep It Simple

Remember:
- **Setup Tab** = Add credentials
- **Generate Tab** = Preview posts
- **Schedule Tab** = Set when to post
- **History Tab** = See what posted

That's all you need to know!

