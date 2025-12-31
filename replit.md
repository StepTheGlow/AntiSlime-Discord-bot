# Replit.md

## Overview

This is a Discord bot built with discord.py that features scheduled video posting, countdown timers, and interactive commands. The bot uses a cog-based modular architecture for organizing functionality and includes a Flask web server for keep-alive functionality (commonly used for hosting on platforms like Replit).

The bot appears to be themed around an anime character (Urahara Kisuke from Bleach, based on the status messages) and serves a specific Discord community with scheduled content delivery.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Framework**: discord.py (v2.5.2) with commands extension
- **Command Style**: Hybrid approach using both prefix commands (`!`) and slash commands (application commands via `bot.tree`)
- **Architecture**: Cog-based modular system where features are organized into separate cog files in the `/cogs` directory

### Cog System
- Cogs are dynamically loaded from the `/cogs` directory on startup
- Files ending in `.disabled` are skipped during loading
- Each cog is a self-contained feature module with its own commands and background tasks

### Background Tasks
- **Status Rotation**: Cycles through predefined bot statuses every 10 seconds using `discord.ext.tasks`
- **Scheduled Tasks**: Uses `aiocron` library for cron-based scheduling (video posting at specific times)
- **Countdown Timer**: Uses `discord.ext.tasks` loop running every minute for countdown functionality

### Web Server (Keep-Alive)
- Simple Flask server on port 8080 serving a basic HTML page
- Runs in a separate thread to prevent blocking the bot
- Used for external uptime monitoring services to keep the bot running

### File Structure Pattern
```
/main.py          - Bot entry point and core setup
/web.py           - Flask keep-alive server
/cogs/            - Feature modules (countdown, video posting, etc.)
/assets/videos/   - Video files for scheduled posting
/templates/       - Flask HTML templates
```

## External Dependencies

### Discord API
- Uses Discord's API via discord.py for all bot functionality
- Requires bot token stored in environment variable (loaded via python-dotenv)
- Uses Discord's file upload for video sharing (subject to 25MB limit for non-boosted servers)

### Environment Variables
- Bot token loaded from `.env` file using `python-dotenv`
- Channel IDs are hardcoded in cog files (should be moved to environment variables)

### Scheduling
- `aiocron`: Cron-style task scheduling for timed events
- `pytz`: Timezone handling (currently using 'Etc/GMT-6')

### Known Limitations
- Discord file upload limit of 25MB causes issues with large video files (documented in attached error log)
- Video files stored locally in `/assets/videos/` directory