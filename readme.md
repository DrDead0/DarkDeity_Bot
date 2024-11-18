# Deity Discord Bot 
![Deity Discord Bot Logo](https://github.com/DrDead0/Deity_Discord-Bot/blob/main/Logo/logo-2.png)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Contents

- [Deity Discord Bot](#deity-discord-bot)
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

Deity Discord Bot is designed to help manage basic server tasks such as setting up rules, sending welcome messages, providing help posts, and more. This bot aims to simplify server administration and enhance the user experience for Discord server members.

## Features

- Automated welcome messages for new members.
- Rules posting and management.
- Help command to guide users.
- Echo command to repeat user input.
- Support and contact information.
- Basic server management commands.

## Installation

To set up the Deity Discord Bot on your server, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/DrDead0/Deity_Discord-Bot.git
    ```
3. Navigate to the project directory:
 
    ```bash
    cd Deity_Discord-Bot
    ```
5. Install the required dependencies:
 
    ```bash
    pip install -r requirements.txt
    ```
7. Set up environment variables for your Discord bot token:
 
    ```bash
    export DISCORD_TOKEN='your_discord_bot_token'
    ```

## Usage

To start the bot, run:

```bash
python bot.py
```
Configuration
-------------

You can configure the bot using a `config.json` file located in the root directory. This file includes settings like welcome messages, rule texts, and more.

Example `config.json`:

```json
{
  "welcome_channel": "welcome",
  "rules_channel": "rules",
  "help_command": "!help",
  "prefix": "!"
}
```
# Commands

Here is a list of available commands:

- `!welcome`: Sends a welcome message to the designated channel.
- `!rules`: Posts the server rules.
- `!help`: Displays the help message with a list of available commands.
- `!echo [message]`: Repeats the message back to the channel.
- `!hello`: Greets the user.
- `!support`: Provides support contact information.
- `!contact`: Displays contact information for the server admin.
- `!info`: Provides information about the server.
- `!ping`: Checks the bot's response time to Discord.
- `!clear [number]`: Deletes a specified number of messages from a channel.
- `!kick [user] [reason]`: Kicks a user from the server.
- `!ban [user] [reason]`: Bans a user from the server.
- `!unban [user]`: Unbans a user from the server.



# Support

If you encounter any issues or have questions, please create an issue on the [GitHub repository](https://github.com/DrDead0/Deity_Discord-Bot/issues) or reach out for support.

# Contact

Created by [Ashish Chaurasiya](https://github.com/DrDead0) & [Varchsava Khare](https://github.com/varchasvakhare2022) - Feel Free To contact Us!

# License

This project is licensed under the MIT License - [To See The LICENSE Click Here](https://github.com/DrDead0/Deity_Discord-Bot/blob/main/LICENSE)

