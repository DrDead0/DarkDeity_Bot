
# DarkDeity Discord Bot 
![DarkDeity Discord Bot Logo](https://github.com/DrDead0/Deity_Discord-Bot/blob/main/Logo/logo-2.png)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Contents

- [DarkDeity Discord Bot](#darkdeity-discord-bot)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Commands](#commands)
  - [Support](#support)
  - [Contact](#contact)
  - [License](#license)

## Introduction

DarkDeity Discord Bot is designed to elevate your Discord server experience with a wide range of features, including music playback, server management, and fun interactive commands. Whether you're looking for entertainment or useful tools, DarkDeity is here to help!

## Features

- Automated welcome messages and goodbye messages for members.
- Music playback powered by `yt-dlp` and FFmpeg.
- Slash commands for modern Discord interaction.
- Fun features like polls, jokes, fun facts, and mini-games.
- Moderation tools: kick, ban, and unban commands.
- Custom help menu for user guidance.
- Interactive commands like number guessing and coin flipping.
- Detailed server and user information displays.

## Installation

To set up the DarkDeity Discord Bot, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/DrDead0/Deity_Discord-Bot.git
    ```

2. Navigate to the project directory:
 
    ```bash
    cd Deity_Discord-Bot
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables for your Discord bot token. Create a `.env` file in the root directory:

    ```
    DISCORD_TOKEN=your_discord_bot_token
    ```

## Usage

To start the bot, run:

```bash
python bot.py
```

## Configuration

The bot can be customized through hardcoded settings in the script or a `config.json` file (if implemented in future updates). You can modify:
- Prefix for commands.
- Welcome and rules channels.
- Custom responses for some commands.

## Commands

Here is the updated list of available commands:

### Prefix Commands (`!`)
- `!play <url>`: Plays music from a YouTube URL.
- `!kick <user> [reason]`: Kicks a user from the server.
- `!ban <user> [reason]`: Bans a user from the server.
- `!unban <user>`: Unbans a previously banned user.
- `!help-bot`: Displays the custom help menu.

### Slash Commands (`/`)
- `/play <url>`: Plays music from a YouTube URL.
- `/coinflip`: Flips a coin (Heads or Tails).
- `/poll <question> <options>`: Creates a poll with up to 10 options.
- `/serverinfo`: Displays detailed information about the server.
- `/userinfo <user>`: Displays detailed information about a user.
- `/guessnumber`: Starts a number guessing game.
- `/funfact`: Shares a random fun fact.
- `/joke`: Tells a random joke.

### Interactive Features
- Number guessing game: `/guessnumber` allows players to guess numbers until they get it right.
- Poll creation: `/poll` lets you create fully customizable polls for community engagement.
- Fun content: `/funfact` and `/joke` provide entertainment.

## Support

If you encounter any issues or have questions, please create an issue on the [GitHub repository](https://github.com/DrDead0/Deity_Discord-Bot/issues) or contact the developers.

## Contact

Created by [Ashish Chaurasiya](https://github.com/DrDead0) & [Varchsava Khare](https://github.com/varchasvakhare2022). Feel free to reach out to us for support or collaboration!

## License

This project is licensed under the MIT License. [Read the full license here](https://github.com/DrDead0/Deity_Discord-Bot/blob/main/LICENSE).

---

This update reflects the current functionality of your bot, including the latest slash commands and interactive features.
