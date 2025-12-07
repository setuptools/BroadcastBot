# 📡 BroadCastBot

A powerful Telegram bot for broadcasting messages to multiple channels with an intuitive **button-based interface**. Send text, media, and interactive buttons to your channels with ease.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![aiogram](https://img.shields.io/badge/aiogram-v3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🎯 Button-Based Interface** - Easy-to-use menu system (no commands needed)
- **📤 Multi-Channel Broadcasting** - Send to multiple channels simultaneously
- **📝 Rich Content** - Support for text, photos, videos, and animations
- **🔘 Interactive Buttons** - Add clickable buttons to broadcasts
- **⏱️ Scheduled Broadcasts** - Send messages at specific times
- **💾 Broadcast History** - Track all sent broadcasts in database
- **🔐 Channel Management** - Organize and control your channels

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Interface Guide](#interface-guide)
- [Buttons](#buttons)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd BroadCastBot
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file**
```bash
echo TOKEN=your_bot_token_here > .env
```

5. **Run the bot**
```bash
python bot.py
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
TOKEN=your_telegram_bot_token_here
```

### Database

The bot uses SQLite (`db.db`) for storing:
- Broadcasting schedules
- Channel information
- User preferences

Database is automatically created on first run.

## 📖 Usage

### Starting the Bot

Simply start the bot in Telegram and press `/start` or tap **🏡 Main menu** button. The entire interface is button-driven — no commands needed!

### Main Menu

The bot presents you with three main buttons:

| Button | Description |
|--------|-------------|
| **⭐ My channels** | Manage your Telegram channels |
| **📊 My broadcast** | Create and send broadcasts |
| **🆘 Help** | View help and instructions |

## 🎯 Interface Guide

### Broadcasting Workflow

1. **⭐ My channels** - First, set up your channels
   - ➕ **Add channel** - Add a new channel to broadcast to
   - **Edit** - Modify channel details (name, image, link)
   - **Toggle Status** - Enable/disable channel for broadcasts
   - **🗑 Delete** - Remove channel

2. **📊 My broadcast** - Create your broadcasts
   - ➕ **Add broadcast** - Create new message
   - **✒️ Title** - Set broadcast title
   - **📃 Description** - Write main message text
   - **🖼️ Image** - Add photo, video, or animation
   - **▶️ Buttons** - Add interactive buttons
   - **⏰ Date** - Schedule send time
   - **✅ Save** - Publish broadcast

### Content You Can Broadcast

| Content Type | Support |
|-------------|---------|
| **Text** | ✅ Messages with formatting |
| **Photos** | ✅ Images and graphics |
| **Videos** | ✅ Video files |
| **Animations** | ✅ GIF files |
| **Interactive Buttons** | ✅ Links and callbacks |

## 🔘 Buttons

### Adding Buttons to Broadcasts

When editing a broadcast, press **▶️ Buttons** to add interactive buttons.

**Format Examples:**

**Single button:**
```
Subscribe | https://t.me/mychannel
```

**Multiple buttons on one row** (comma-separated):
```
Button 1 | url1, Button 2 | url2
```

**Multiple rows:**
```
Top Button | url1
Bottom Left | url2, Bottom Right | url3
```

## 💡 Examples

### Example 1: Create Your First Broadcast

1. Press **📊 My broadcast**
2. Press **➕ Add broadcast**
3. Press **✒️ Title** → Type: `"Special Announcement"`
4. Press **📃 Description** → Type: `"Join us tomorrow!"`
5. Press **✅ Save**

### Example 2: Broadcast with Buttons

1. Press **📊 My broadcast**
2. Press **➕ Add broadcast**
3. Press **✒️ Title** → `"Check This Out"`
4. Press **📃 Description** → `"Click the buttons below"`
5. Press **▶️ Buttons** → Type:
```
Subscribe | https://t.me/mychannel
Visit Website | https://example.com
Download Guide | https://example.com/guide.pdf
```
6. Press **✅ Save**

### Example 3: Schedule a Broadcast

1. Press **📊 My broadcast**
2. Press **➕ Add broadcast**
3. Add your content (title, description, image)
4. Press **⏰ Date** → Set date and time
5. Press **✅ Save** → Message will be sent automatically at scheduled time

### Example 4: Manage Channels

1. Press **⭐ My channels**
2. Press **➕ Add channel** → Enter channel link: `https://t.me/mychannel`
3. Press **✒️ Edit name** → Set display name
4. Press **🖼️ Edit image** → Upload channel cover photo
5. Press **✅/❌ status** → Enable/disable for broadcasts

## 📁 Project Structure

```
BroadCastBot/
├── routes/                 # Telegram command handlers
│   ├── start.py          # /start command
│   ├── broadcast.py      # /broadcast command
│   ├── channels.py       # /channels command
│   ├── help.py           # /help command
│
├── utils/                 # Utility functions
│   ├── broadcast.py      # Broadcasting logic
│   ├── keyboard.py       # Telegram keyboard layouts
│   ├── filters.py        # Message filters
│   └── cleaner.py        # Cleanup utilities
│
├── middleware/            # Request middleware
│   └── midddleware.py     # Broadcast middleware
│
├── bot.py                 # Main bot class
├── db.db                  # SQLite database
├── buttons.json           # Button configurations
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md              # This file
```

## 🔧 Development

### Hot Reload

The bot supports hot reloading during development:

```
/reload              # Reload modules
/reload init_again   # Reload with database re-initialization
```

### Database Schema

**broadcasts table:**
```sql
- id (INTEGER PRIMARY KEY)
- title (TEXT)
- description (TEXT)
- image (TEXT)
- buttons (JSON)
- channel (TEXT)
- user_id (INT)
- send_at (INT)
- status (BOOLEAN)
```

**channels table:**
```sql
- id (INTEGER PRIMARY KEY)
- active (BOOLEAN)
- name (TEXT)
- channel (TEXT)
- image (TEXT)
- bot_in (BOOLEAN)
- user_id (INT)
- created_at (DATETIME)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📞 Support

For help using the bot, use the `/help` command in Telegram.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Important Notes

- ✅ Set up channels before creating broadcasts
- ✅ Add descriptive titles for easy tracking
- ✅ Preview broadcasts before saving
- ✅ Schedule broadcasts for optimal engagement
- ⚠️ **Bot must be administrator** in all target channels
- ⚠️ Respect Telegram's rate limits (don't spam channels)
- ⚠️ Test buttons before publishing to large audiences
- ⚠️ Keep channel information up-to-date

## 🎓 Quick Start

1. Start the bot → Press `/start` or **🏡 Main menu**
2. Set up channels → **⭐ My channels** → **➕ Add channel**
3. Create broadcast → **📊 My broadcast** → **➕ Add broadcast**
4. Add content → Use **✒️**, **📃**, **🖼️**, **▶️**, **⏰** buttons
5. Publish → Press **✅ Save**

For detailed help in Telegram, press **🆘 Help** button anytime!