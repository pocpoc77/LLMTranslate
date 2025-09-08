# 🌍 LLM Translate: Your Smart PDF Translator! 🚀
<img width="450" alt="Config tab" src="https://github.com/user-attachments/assets/dcb5c800-bab9-4dbf-a227-9ae60893b540" />

<img width="450" alt="Translation tab" src="https://github.com/user-attachments/assets/6bf71429-25fe-4c6a-9410-1702b3cfed00" />

Translate your large PDF files with ease using the power of Large Language Models! This project leverages OpenAI-compatible and Mistral APIs to provide accurate, context-aware translations to your language of choice.
* You can see an example OCR and translation result in [Example.md](https://github.com/smahdink/LLMTranslate/blob/main/Example.md)

---

## ✨ Key Features

* **OCR Integration:** Processes PDF files by first performing Optical Character Recognition to extract text. 📄➡️💻
* **Easy to use GUI:** The GUI provides an accessible way for everyone, regardless of their technical skills, to configure and use the app!
* **Specialized Translation:** Leveraging the power of LLMs, the translations done by this method are highly specialized and context-aware! 🧠
* **Structure Preservation:** Maintains the original document's formatting, numbers, measurements, and proper nouns. 📏
* **Configurable API:** Supports both OpenAI-compatible and Mistral API endpoints, with API key management through a local configuration file, so that you can use your favourite LLM or even self-host! ⚙️
* **Cost Reduction:** By using services like **OpenRouter** that provide free APIs for some models like the new `deepseek-r1-0528`, you can get great results with almost no expenses! 🤑


---

## 🛠️ Installation Guide
### Release versions (GUI)
No installation required! just download the latest version for your OS from [Releases](https://github.com/smahdink/LLMTranslate/releases), extract and run.
* you can find the instructions down below.

### The CLI version
  * The commands you see in this guide can be executed inside a **Terminal** regardless of the OS (Linux, Windows, MacOS). But you need Python3 and pip installed beforehand.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/LLM-Translate.git
    cd LLM-Translate
    ```
    * You can use the download zip button instead of cloning

2.  **Install dependencies:**
    * You may want to create a Python virtual environment for this project to manage dependencies.
    ```bash
    pip install openai mistralai
    ```

---

## 🚀 How to Use

### THE GUI

1. **Initial configuration:**
   * After launching the app, at the configuration tab, enter your Mistral API key that you generate from [here](console.mistral.ai/api-keys) and the Mistral model name you like to use for translation (not OCR) e.g. 'mistral-large-latest'
   * Enter openai compatible url, api key and, model name, you can either use a local model with Ollama or LM-Studio, or you can use services like OpenRouter.
   * Enter your custom system prompt to perform the translation, this step is crucial for getting the best results.

2. **OCR and Translation**
   * Swtitch to the translation tab, choose your desired PDF file, select your model of choice, click start and wait patiently.
### THE CLI

1.  **Customize URL and System Prompt:**
    Before running the application, open the `LLMTranslate.py` file in a text editor and customize the `system_prompt` and `base_url` parameters.

    * I highly recommend using **OpenRouter** which is the default URL. You only need to create an account on their website and generate an API key.
    * Customize the system prompt to provide the model with your **target language** and any additional contextual information relevant to your document. This helps ensure more accurate and tailored translations!

2.  **Run the script for the first time:**
    The first time you execute `LLMTranslate.py`, it will prompt you to enter your API keys for OpenAI-compatible and Mistral servers. These keys will be securely saved in `LLM-translate-config.ini`.

    ```bash
    python LLMTranslate.py your_document.pdf
    ```

    * *Remember to replace `your_document.pdf` with the actual path to your PDF file.*

3.  **Specify the LLM Model (Optional):**
    You have the flexibility to choose between `openai-compatible` (the default) and `mistral` models for translation. Use the `-m` or `--model` flag:

    ```bash
    python LLMTranslate.py your_document.pdf -m mistral
    ```

    *Alternatively:*

    ```bash
    python LLMTranslate.py your_document.pdf --model openai-compatible
    ```

4.  **Check the Output:**
    The translated content will be saved in a new Markdown file. The filename will follow the pattern `[original_filename] [model] translated.md` and will be located in the same directory as your input PDF. For example: `your_document mistral translated.md`. 📄✨

---

## 🤝 Contribute to LLM Translate!

I welcome contributions to LLM Translate! If you have suggestions, found a bug, or want to contribute to the code, please feel free to:

* Open a new issue for bug reports or feature requests.
* Submit a pull request with your improvements.

Let's build a better translation tool together! Your input is highly valued. 🎉

---

## 📝 TODO

* [x] Improve code structre. This wasn't meant to be released at first :P
* [x] Seperate the system prompt and move it somewhere easier to edit
* [ ] Implement an intermediate data structure (maybe json) to keep track of pages and different translations
* [x] GUI and packaging into an installable app
