# AC Controller Telegram Bot Setup

## Overview
This script allows you to control your AC through a Telegram bot with the following features:
- Manual AC toggle via `/toggle` command
- Automatic AC toggling with configurable intervals
- Status checking with `/status` command
- Start/stop auto-toggle remotely

## Prerequisites
1. **Python packages**: Install the required package first
   ```bash
   pip install python-telegram-bot
   ```

2. **Telegram Bot**: Create a new bot through BotFather on Telegram
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` command
   - Follow the instructions to create your bot
   - Copy the bot token (format: `123456789:ABCDEF...`)

## Setup Instructions

### 1. Configure the Bot Token
1. Open `config.json` in your project folder
2. Replace `"YOUR_BOT_TOKEN_HERE"` with your actual bot token from BotFather
3. Optionally configure:
   - `auto_start_enabled`: Set to `true` to start auto-toggle on script startup
   - `default_interval_minutes`: Default interval for auto-toggle (in minutes)

Example config.json:
```json
{
    "bot_token": "123456789:ABCDEF1234567890abcdef1234567890ABC",
    "auto_start_enabled": false,
    "default_interval_minutes": 10
}
```

### 2. Run the Script
```bash
python main.py
```

### 3. Browser Login
- The script will open a Chrome browser window
- Log in manually to the AC control website
- Once logged in, the bot will be ready to receive commands

## Telegram Bot Commands

### Available Commands:
- `/start` or `/help` - Show help message with all commands
- `/status` - Check current AC status and auto-toggle state
- `/toggle` - Manually toggle the AC on/off
- `/auto_start [minutes]` - Start auto-toggle (default: 10 minutes)
  - Example: `/auto_start 15` (toggle every 15 minutes)
- `/auto_stop` - Stop automatic toggling

### Usage Examples:
1. **Check AC status**: Send `/status`
2. **Toggle AC once**: Send `/toggle`
3. **Start auto-toggle every 10 minutes**: Send `/auto_start 10`
4. **Stop auto-toggle**: Send `/auto_stop`

## Features

### Automatic AC Control
- The bot can automatically toggle the AC at specified intervals
- Default interval is 10 minutes (600 seconds)
- You can change the interval using `/auto_start [minutes]`
- Auto-toggle runs in a separate thread, so the bot remains responsive

### Manual Control
- Use `/toggle` to manually turn the AC on/off at any time
- Manual toggles work even when auto-toggle is active

### Status Monitoring
- `/status` shows:
  - Current AC state (ON/OFF)
  - Auto-toggle status (ACTIVE/STOPPED)
  - Current interval setting

### Safety Features
- The script automatically turns off the AC when exiting
- Handles browser popups automatically
- Threaded operation prevents blocking

## Troubleshooting

### Common Issues:

1. **"Please update your bot token" error**
   - Make sure you've replaced `YOUR_BOT_TOKEN_HERE` in `config.json` with your actual bot token

2. **Bot not responding**
   - Check that the bot token is correct
   - Ensure the script is running and connected
   - Verify your internet connection

3. **AC control not working**
   - Make sure you're logged into the AC control website in the browser
   - Check that the browser window is still open
   - Verify the website is accessible

4. **Import errors**
   - Install required packages: `pip install python-telegram-bot selenium`
   - Make sure you have Chrome browser installed

### Getting Your Bot Token:
1. Open Telegram
2. Search for "@BotFather"
3. Send `/newbot`
4. Choose a name for your bot
5. Choose a username (must end with "bot")
6. Copy the token provided by BotFather
7. Paste it in your `config.json` file

## Security Notes
- Keep your bot token private
- Don't share your `config.json` file
- The bot will only respond to commands sent directly to it
- Consider using Telegram's privacy settings to restrict who can message your bot

## Running the Bot 24/7
To keep the bot running continuously:
- Use a VPS or cloud server
- Consider using screen/tmux sessions
- Set up proper logging for monitoring
- Ensure stable internet connection

For any issues, check the console output for error messages and debugging information.