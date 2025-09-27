# ALwrity AI Business Name Generator

ALwrity is an AI-powered tool designed to assist you in generating creative and brandable business names effortlessly. Whether you're starting a new business or rebranding an existing one, ALwrity streamlines the process of crafting memorable business names that resonate with your audience and enhance your brand identity.

## Introduction

ALwrity leverages advanced AI technology to analyze your business description, target audience, and naming preferences, providing you with tailored business name suggestions that align with your brand vision. With ALwrity, you can save time and effort while ensuring your business names are unique, memorable, and suitable for branding.

## Getting Started

To get started with ALwrity, follow these simple steps:

1. **Describe Your Business:** Enter a clear description of your business, what you do, and your target market.
2. **Set Preferences:** Choose name length (short/medium/long) and style (professional/modern/creative/funny).
3. **Add Keywords (Optional):** Include specific words you want in the names or exclude words you want to avoid.
4. **Generate Names:** Click the "Generate Business Names" button to let ALwrity create unique business name suggestions.
5. **Refine (Optional):** Provide feedback to refine the suggestions based on your preferences.

## Running the Program with Streamlit

To run the ALwrity program using Streamlit, follow these steps:

1. **Install Streamlit:** If you haven't already installed Streamlit, you can do so using pip:  
   `pip install streamlit`

2. **Clone the Repository:** Clone the ALwrity repository from GitHub to your local machine:  
   `git clone https://github.com/your-username/alwrity-business-name-generator.git`

3. **Navigate to the Directory:** Change your current directory to the ALwrity project directory:  
   `cd alwrity-business-name-generator`

4. **Install Dependencies:** Install the required packages:  
   `pip install -r requirements.txt`

5. **Run the Program:** Use the `streamlit run` command to run the ALwrity program:  
   `streamlit run business_name_app.py`

6. **Access the Web App:** Once the program is running, open a web browser and navigate to the URL provided by Streamlit to access the ALwrity web application.

## Simple Local Installation Guide (For Non-Tech Users)

Follow these easy steps to install and use ALwrity on your Windows computer:

1. **Download & Install Python:**  
   * Go to python.org/downloads and download the latest version of Python for Windows.  
   * Run the installer and make sure to check the box that says **"Add Python to PATH"** before clicking Install.

2. **Download ALwrity Tool:**  
   * Click the green **Code** button on the GitHub page and choose **Download ZIP**.  
   * Unzip the downloaded file to a folder on your computer (e.g., `C:\Users\YourName\Downloads\alwrity-business-name-generator`).

3. **Open Command Prompt:**  
   * Press `Win + R`, type `cmd`, and press Enter.  
   * In the Command Prompt window, type:  
   ```  
   cd C:\Users\YourName\Downloads\alwrity-business-name-generator  
   ```  
   (Replace `YourName` with your Windows username if needed.)

4. **Install Required Packages:**  
   * Type the following command and press Enter:  
   ```  
   pip install -r requirements.txt  
   ```  
   * Wait for the installation to finish (you need an internet connection).

5. **Run the Tool:**  
   * In the same Command Prompt window, type:  
   ```  
   streamlit run business_name_app.py  
   ```  
   * Your web browser will open automatically. If not, copy the link shown in the Command Prompt and paste it into your browser.

6. **Use ALwrity:**  
   * Enter your business description and other details in the web app.  
   * (Optional) Enter your Gemini API key in the API Configuration section for best results.  
   * Click **Generate Business Names** and enjoy!

---

**No coding required!** If you get stuck, ask a friend or contact support on the GitHub Issues page.

## Features

- **AI-Powered Generation:** Uses Google's Gemini 2.5 Flash model for intelligent name generation
- **Customizable Preferences:** Choose name length, style, and include/exclude specific keywords
- **Refinement Capability:** Provide feedback to refine suggestions based on your preferences
- **Export Functionality:** Download generated names as Excel files for A/B testing
- **User-Friendly Interface:** Clean, intuitive design suitable for non-technical users
- **Offline-First Design:** Works without API keys using local generation as fallback

## API Configuration

For the best results, you can provide your own Gemini API key:

1. Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Enter it in the "API Configuration" section of the app
3. The tool will use your key for generation, otherwise it falls back to local generation

## About

ALwrity AI Business Name Generator - Free & open source by the ALwrity team.

### Resources

- [ALwrity Website](https://alwrity.com)
- [GitHub Repository](https://github.com/your-username/alwrity-business-name-generator)

---

**Made with ❤️ by the ALwrity team**