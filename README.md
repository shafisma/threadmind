# ThreadMind

A powerful Discord bot for managing and analyzing conversations in your server. ThreadMind helps you organize discussions, extract insights, and maintain better communication through advanced thread management features.

## 🚀 Features

- **AI-Powered Summaries**: Generate intelligent summaries of long conversations
- **Action Items Extraction**: Automatically identify and track action items
- **Sentiment Analysis**: Analyze the emotional tone of conversations
- **Search & Recall**: Find specific messages and information across threads
- **Timeline Visualization**: View conversation timelines and statistics
- **Participant Tracking**: Monitor and analyze user participation
- **Decision Tracking**: Extract and monitor finalized decisions
- **Auto-Summarization**: Scheduled summaries for ongoing channels
- **Multi-format Export**: Export summaries to Markdown and PDF formats
- **Server Statistics**: View activity metrics and decision-making patterns

## 📋 Commands

### Core Commands
- `/summarize [thread]` - Generate a summary of a thread
- `/action-items [thread]` - Extract action items from a thread
- `/sentiment [thread]` - Analyze sentiment of a thread
- `/search [query]` - Search for messages across threads
- `/timeline [thread]` - View conversation timeline
- `/participants [thread]` - Show thread participants
- `/statistics [thread]` - Get thread statistics
- `/export [thread] [format]` - Export thread data

### Advanced Commands
- `/recall` - Get the latest channel summary
- `/compare [channel1] [channel2]` - Compare summaries from two channels
- `/settings [tone]` - Configure AI tone and server preferences

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
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

3. **Configure environment variables:**
   Create a `.env` file in the root directory with:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

4. **Initialize the database:**
   ```bash
   python -c "from storage.db import init_db; init_db()"
   ```

5. **Run the bot:**
   ```bash
   python bot/main.py
   ```

## 🤖 AI Integration

ThreadMind uses Google Gemini for advanced AI capabilities including:
- Natural language understanding
- Summarization
- Sentiment analysis
- Decision extraction
- Action item identification

**Bot Invite**: https://discord.com/oauth2/authorize?client_id=1452527298124316672&scope=bot%20applications.commands&permissions=534723982656

## 🚀 Future Roadmap

- Web dashboard for enhanced visualization
- Multi-server analytics and comparison
- Integration with external productivity tools
- Advanced machine learning for better insights
- Mobile application for on-the-go access

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
