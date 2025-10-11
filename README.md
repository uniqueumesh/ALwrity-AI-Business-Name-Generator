# 🚀 Alwrity - AI Business Name Generator

A streamlined, AI-powered business name generator that researches similar businesses and creates unique, brandable names using advanced language models.

## ✨ Features

- **AI-Powered Research**: Uses Exa API to research similar businesses in your niche
- **Smart Name Generation**: Leverages Google Gemini 2.0 Flash LLM to create unique, memorable business names
- **Multiple Naming Styles**: Choose from modern, professional, creative, or descriptive styles
- **Export Options**: Download results as Excel or CSV files
- **User-Friendly Interface**: Clean, intuitive Streamlit interface
- **Secure Configuration**: API keys managed through .env file

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd ALwrity-AI-Business-Name-Generator
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up API keys (Required)

Create a `.env` file in the project root with your API keys:

```env
# Required API Keys
GEMINI_API_KEY=your_gemini_api_key_here
EXA_API_KEY=your_exa_api_key_here
```

**Get your API keys:**
- **Gemini API**: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) (Free tier available - uses Gemini 2.0 Flash)
- **Exa API**: [https://exa.ai/](https://exa.ai/) (Sign up for API access)

**Note**: API keys must be configured in the `.env` file. There is no UI option to enter keys for security reasons.

## 🚀 Usage

### 1. Run the application

```bash
streamlit run app.py
```

### 2. Using the tool

1. **Enter Business Keywords**: Describe your business in 2-4 words (e.g., "AI productivity tools", "eco-friendly fashion")

2. **Provide Details** (Optional):
   - Business description
   - Industry
   - Name style preference
   - Target audience

3. **Configure Settings**:
   - Choose number of names to generate (5-20)

4. **Generate Names**: Click the "Generate Business Names" button

5. **Export Results**: Download your favorite names as Excel or CSV

## 📋 How It Works

```
User Input (Keywords & Preferences)
    ↓
Exa API Research (Find similar businesses)
    ↓
Context Building (Analyze competitors)
    ↓
Gemini LLM Generation (Create unique names)
    ↓
Results Display & Export
```

## 🎨 Naming Strategies

The tool uses multiple naming strategies:
- **Invented Words**: Unique coined terms (like Spotify, Xerox)
- **Compound Words**: Combining two words (like Facebook, Netflix)
- **Modified Words**: Creative spelling variations (like Flickr, Tumblr)
- **Metaphorical Names**: Evocative brand names (like Amazon, Apple)

## 🔑 API Configuration

All API keys must be configured in the `.env` file in the project root. The application uses:
- **Gemini 2.0 Flash** for AI-powered name generation
- **Exa API** for business research and competitive analysis

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This tool generates name suggestions but does not:
- Perform trademark searches
- Check domain availability
- Provide legal clearance

Always perform proper trademark searches, domain checks, and legal clearance before using a business name commercially.

## 🐛 Troubleshooting

### "API Key Missing" Error
- Ensure your `.env` file is in the project root
- Check that API keys are properly formatted (no extra spaces)
- Verify the .env file is not gitignored or excluded from loading
- Restart the Streamlit app after adding/updating .env

### Rate Limit Errors
- Wait a few minutes and try again
- Check your API quota limits (Gemini, Exa)
- Reduce the number of names to generate

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

Made with ❤️ using Streamlit, Google Gemini 2.0 Flash, and Exa AI

