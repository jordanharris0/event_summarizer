# Event Log Summarizer

A powerful and user-friendly Python CLI tool to fetch, parse, and summarize Windows Event Viewer logs using OpenAI's GPT API. Export the results in multiple formats and gain quick insights into your system events with a clean and colorful terminal interface.

---

## 🚀 Features

- 🔍 **Fetch Logs**: Retrieve logs from Application, Security, Setup, System, or Forwarded Events.
- 🧠 **AI Summarization**: Automatically summarize event logs with OpenAI's GPT.
- 💾 **Export Formats**: Save results as `.txt`, `.json`, `.csv`, or `.md` files.
- 🎨 **Colored CLI Output**: Easy-to-read, styled terminal output using `colorama`.
- 🔁 **Restart or Quit**: Intuitive prompts allow users to keep exploring or exit smoothly.

---

## 📦 Installation

1. **Clone the Repository**

```bash
https://github.com/yourusername/event_summarizer.git
cd event_summarizer
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Create a .env File (optional)**
```env
OPENAI_API_KEY=your-api-key-here
```
If omitted, the program will prompt you for a key and offer to save it.

---

## 🛠 Usage

Cd into the root directory and run the program via PowerShell or terminal:
```bash
PS D:\VSProjects\Python\event_summarizer> python event_summarizer.py
```

## During runtime:
- Choose a log type

- Select filters (date range, level, etc.)

- View formatted logs

- Summarize with GPT (requires API key)

- Export to file or skip

---

## 📁 Export Behavior

- Exported files are saved in an ```exports/``` subfolder created automatically in the current directory.

- You will be shown the full path after export completes.

---

## 🔑 API Key

To use AI summarization:

- Get an API key from [OpenAI](https://platform.openai.com)

- Add it to your .env file OR paste it at runtime

---

## 🧪 Example Output
```
=======================================================
              🔍  Event Log Summarizer
     Analyze Windows Event Logs with GPT Assistance
                 June 25, 2025 10:59 AM
=======================================================

Would you like to export the logs to a specific file? (yes/no): yes

Enter the output filename ending in .txt, .md, .json, .csv: logs.md

✅ Export complete. 📁 File saved to: exports/logs.md
```

---
