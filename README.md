# 🤖 DBot - Discord Bot Python

A simple Discord bot built with Python using the `discord.py` library.

## ✨ Features

- 🏓 **Ping** - Test bot latency
- ℹ️ **Info** - Bot information and statistics
- 🏠 **Server** - Discord server information
- 👤 **User** - User/member information
- 🗑️ **Clear** - Delete messages (requires permission)
- 📚 **Help** - List of available commands
- 💬 **Say** - Bot sends a message
- 📝 **Embed** - Create custom embeds
- 🎉 **Welcome Message** - Automatic welcome messages
- 👋 **Leave Message** - Messages when members leave

## 🚀 Setup Guide

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Discord Bot

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" tab and click "Add Bot"
4. Copy the **Token** (click "Copy" or "Reset Token")
5. Enable **Message Content Intent** under "Privileged Gateway Intents"

### 3. Invite Bot to Server

1. Go to "OAuth2" > "URL Generator"
2. Select scope: **bot**
3. Select required permissions:
   - Send Messages
   - Embed Links
   - Manage Messages
   - Read Message History
   - Use Slash Commands
4. Copy the generated URL and open in browser
5. Select server and authorize bot

### 4. Setup Environment Variables

Create `.env` file in root directory:

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

**⚠️ Never share your bot token!**

### 5. Run Bot

```bash
python bot.py
```

## 📋 Command List

| Command | Description | Example |
|---------|-------------|---------|
| `!ping` | Test bot latency | `!ping` |
| `!info` | Bot information | `!info` |
| `!server` | Server information | `!server` |
| `!user [@user]` | User information | `!user @username` |
| `!clear [amount]` | Delete messages | `!clear 10` |
| `!help` | Command list | `!help` |
| `!say [message]` | Bot sends message | `!say Hello World!` |
| `!embed [title] [desc]` | Create embed | `!embed Title Description` |

## 🔧 Configuration

File `config.py` contains bot settings:

```python
BOT_PREFIX = "!"  # Command prefix
BOT_NAME = "DBot"  # Bot name
BOT_VERSION = "1.0.0"  # Bot version
```

## 📁 Struktur File

```
dbot/
├── bot.py          # File utama bot
├── config.py       # Konfigurasi bot
├── requirements.txt # Dependencies
├── README.md       # Dokumentasi
└── .env           # Environment variables (buat sendiri)
```

## 🛠️ Development

### Adding New Commands

```python
@bot.command(name='command_name')
async def command_function(ctx, parameter):
    """Command description"""
    # Command logic
    await ctx.send("Response")
```

### Adding Events

```python
@bot.event
async def on_event_name(parameter):
    """Handle event"""
    # Event logic
    pass
```

## 🔒 Permissions

Bot requires the following permissions:
- **Send Messages** - Send messages
- **Embed Links** - Send embeds
- **Manage Messages** - Delete messages
- **Read Message History** - Read message history
- **Use Slash Commands** - Use slash commands

## 🐛 Troubleshooting

### Bot not responding
- Make sure bot is online and connected
- Check if command prefix is correct (`!`)
- Ensure bot has required permissions

### "Invalid token" error
- Check `.env` file and ensure token is correct
- Never share token with anyone
- Reset token in Discord Developer Portal if needed

### Bot cannot delete messages
- Make sure bot has "Manage Messages" permission
- Ensure bot role is higher than messages to be deleted

## 📝 License

This project is open source and can be used for learning purposes.

## 🤝 Contributing

Feel free to create pull requests or issues for contributions!

---

**Built with ❤️ using discord.py** 