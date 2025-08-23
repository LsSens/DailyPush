# DailyPush 🚀

**Automated daily commits to keep your GitHub stats always active and green!**

## ✨ What it does

- 🤖 **Automatically creates** 25-30 commits daily
- 📝 **Generates unique files** with timestamps
- 🚀 **Pushes to GitHub** automatically
- 📊 **Keeps your stats** always active

## 🚀 Quick Setup

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/DailyPush.git
cd DailyPush
pip install -r requirements.txt
```

### 2. Configure
```bash
# Copy example config
cp env.example .env

# Edit .env with your info
GIT_USER_NAME=Your Name
GIT_USER_EMAIL=your.email@example.com
```

### 3. Test
```bash
# Option 1: Main script (recommended)
python run.py

# Option 2: Direct module
python src/main.py

# Option 3: Local scheduler
python scheduler.py
```

## 🌐 GitHub Actions (Recommended)

**Already configured!** The workflow runs automatically every day at 9:00 AM UTC.

### To activate:
1. Push to GitHub: `git push -u origin main`
2. Go to Actions tab
3. Enable workflows
4. Done! 🎉

## 📁 Project Structure

```
DailyPush/
├── src/                  # Source code
│   ├── __init__.py      # Package initialization
│   ├── main.py          # Main entry point
│   ├── daily_push.py    # Core DailyPush class
│   ├── git_manager.py   # Git operations
│   ├── commit_manager.py # Commit management
│   └── file_manager.py  # File creation
├── run.py               # Main script (recommended)
├── scheduler.py         # Local scheduler
├── requirements.txt     # Python dependencies
├── .env                # Your configuration (create from env.example)
├── env.example         # Configuration template
├── .github/workflows/  # GitHub Actions (auto-deployment)
└── README.md          # This file
```

## ⚙️ Configuration

Edit `.env` file to customize:

```env
# Git settings
GIT_USER_NAME=Your Name
GIT_USER_EMAIL=your.email@example.com

# DailyPush settings
COMMITS_MIN=25
COMMITS_MAX=30
EXECUTION_TIME=09:00
```

## 🔄 How it works

1. **Daily execution** (9:00 AM UTC)
2. **Creates 25-30 commits** with unique files
3. **Automatic push** to GitHub
4. **Your stats stay active** 🎯

## 📊 Result

- **GitHub profile**: Always green and active
- **Commit history**: Rich and diverse
- **Zero maintenance**: Fully automated
- **Daily activity**: Guaranteed

## 🆘 Need help?

- **Local test**: `python run.py`
- **Manual execution**: GitHub Actions → Run workflow
- **Check logs**: Actions tab → View logs

---

**Keep your GitHub alive with DailyPush! 🚀✨**
