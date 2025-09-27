# ALwrity AI Business Name Generator

ALwrity is an AI-powered tool designed to assist you in generating creative and brandable business names effortlessly. Whether you're starting a new business or rebranding an existing one, ALwrity streamlines the process of crafting memorable business names that resonate with your audience and enhance your brand identity.

## Introduction

ALwrity leverages advanced AI technology (Gemini 2.5 Flash) to analyze your business description, target audience, and naming preferences, providing you with tailored business name suggestions that align with your brand vision. With ALwrity, you can save time and effort while ensuring your business names are unique, memorable, and suitable for branding.

## Features

- **🤖 AI-Powered Generation:** Uses Google's Gemini 2.5 Flash model for intelligent name generation
- **🔄 Smart Fallback:** Local generation when API is unavailable
- **🎨 Multiple Styles:** Professional, Modern, Creative, Funny, and Custom styles
- **📏 Length Options:** Short (4-7 chars), Medium (7-11 chars), Long (11-16 chars)
- **🔧 Customization:** Include/exclude keywords, alliteration preferences
- **💬 Refinement System:** Provide feedback to improve suggestions
- **🛡️ Safety Filters:** Input sanitization to avoid API blocks
- **📱 User-Friendly:** Clean interface designed for non-technical users

## Quick Start

### Option 1: Run Locally
```bash
# Clone the repository
git clone https://github.com/uniqueumesh/ALwrity-AI-Business-Name-Generator.git
cd ALwrity-AI-Business-Name-Generator

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run business_name_app.py
```

### Option 2: Streamlit Cloud (Recommended)
1. Fork this repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub account
4. Deploy the `business_name_app.py` file
5. Your app will be live at `https://your-app-name.streamlit.app`

## How to Use

1. **Describe Your Business:** Enter a clear description of your business, what you do, and your target market.
2. **Set Preferences:** Choose name length (short/medium/long) and style (professional/modern/creative/funny).
3. **Add Keywords (Optional):** Include specific words you want in the names or exclude words you want to avoid.
4. **Generate Names:** Click the "Generate Business Names" button to let ALwrity create unique business name suggestions.
5. **Refine (Optional):** Provide feedback to refine the suggestions based on your preferences.

## API Configuration

For the best results, you can provide your own Gemini API key:

1. Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Enter it in the "API Configuration" section of the app
3. The tool will use your key for generation, otherwise it falls back to local generation

## Simple Installation Guide (For Non-Tech Users)

1. **Download & Install Python:**  
   * Go to [python.org/downloads](https://python.org/downloads) and download the latest version of Python for Windows.  
   * Run the installer and make sure to check the box that says **"Add Python to PATH"** before clicking Install.

2. **Download ALwrity Tool:**  
   * Click the green **Code** button on the GitHub page and choose **Download ZIP**.  
   * Unzip the downloaded file to a folder on your computer.

3. **Open Command Prompt:**  
   * Press `Win + R`, type `cmd`, and press Enter.  
   * Navigate to the downloaded folder using `cd` command.

4. **Install & Run:**  
   ```bash
   pip install -r requirements.txt
   streamlit run business_name_app.py
   ```

## Repository Structure

```
ALwrity-AI-Business-Name-Generator/
├── business_name_app.py    # Complete single-file application
├── requirements.txt        # Dependencies (3 packages only)
├── README.md              # This documentation
└── LICENSE                # MIT License
```

## Dependencies

- `streamlit>=1.37.0` - Web application framework
- `google-generativeai>=0.7.2` - Gemini AI integration
- `tenacity>=8.2.0` - Retry logic for API calls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## About

ALwrity AI Business Name Generator - Free & open source by the ALwrity team.

### Resources

- [ALwrity Website](https://alwrity.com)
- [GitHub Repository](https://github.com/uniqueumesh/ALwrity-AI-Business-Name-Generator)

---

**Made with ❤️ by the ALwrity team**