# ThreadMind

A powerful Discord bot for managing and analyzing conversations in your server. ThreadMind helps you organize discussions, extract insights, and maintain better communication through advanced thread management features.

## Features

- **Thread Management**: Create, organize, and manage Discord threads efficiently
- **AI-Powered Summaries**: Generate intelligent summaries of long conversations
- **Action Items Extraction**: Automatically identify and track action items from discussions
- **Sentiment Analysis**: Analyze the emotional tone of conversations
- **Search & Recall**: Find specific messages and information across threads
- **Timeline Visualization**: View conversation timelines and statistics
- **Export Capabilities**: Export thread data in various formats
- **Participant Tracking**: Monitor and analyze user participation

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js (for frontend components)
- Discord bot token
- Google Gemini API key (for AI features)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shafisma/threadmind.git
   cd threadmind
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory with the following variables:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   DATABASE_URL=sqlite:///data.db
   ```

5. **Initialize the database:**
   ```bash
   python -c "from storage.db import init_db; init_db()"
   ```

6. **Run the bot:**
   ```bash
   python bot/main.py
   ```

## Usage

### Basic Commands

- `/summarize [thread]` - Generate a summary of a thread
- `/action-items [thread]` - Extract action items from a thread
- `/sentiment [thread]` - Analyze sentiment of a thread
- `/search [query]` - Search for messages across threads
- `/timeline [thread]` - View conversation timeline
- `/participants [thread]` - Show thread participants
- `/statistics [thread]` - Get thread statistics
- `/export [thread] [format]` - Export thread data

### Configuration

The bot can be configured through the `/settings` command to customize:
- AI model preferences
- Summary length
- Sentiment analysis sensitivity
- Export formats
- Notification preferences

## Project Structure

```
threadmind/
├── bot/                    # Discord bot implementation
│   ├── main.py            # Bot entry point
│   ├── commands/          # Command implementations
│   ├── ai/               # AI integration (Gemini)
│   └── storage/          # Database management
├── storage/              # Database models and utilities
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
├── .env                  # Environment variables
└── README.md            # This file
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run tests:
   ```bash
   python -m pytest
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please:
- Check the [Issues](https://github.com/shafisma/threadmind/issues) section
- Create a new issue if your problem isn't already addressed
- Join our Discord server for community support

## Contributing Organizations

This project is maintained by:
- [ShafisMa](https://github.com/shafisma)

## Acknowledgments

- Discord.py library for Discord bot functionality
- Google Gemini for AI capabilities
- SQLite for database management
- All contributors and testers
