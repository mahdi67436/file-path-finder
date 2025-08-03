README.md
markdown
Copy
Edit
# 🔍 Advanced File Path Finder (Multithreaded)

A terminal-based multi-threaded file searcher built in Python. Supports extension filtering, folder exclusion, time-limited search, and auto-opening folder locations.

![screenshot](https://i.imgur.com/DykEc0O.png) <!-- Optional Screenshot -->

---

## 🚀 Features

- Multithreaded file search
- Exact or partial match
- Extension filter (e.g., `.txt`, `.pdf`)
- Folder exclusion (e.g., `node_modules`, `.git`)
- Rich terminal UI with `rich` + `pyfiglet`
- Auto open matched folders
- Save results to `.txt`

---

## 🛠 Requirements

- Python 3.7+
- Install dependencies:

```bash
pip install -r requirements.txt
📦 Usage
bash
Copy
Edit
python file_finder.py
📸 Example
sql
Copy
Edit
Search type:
1. Exact match
2. Contains
Choose 1 or 2: 2
Filter by extensions? .txt,.pdf
Exclude folders? node_modules,.git
How many seconds to search? 20
💻 Cross Platform
✅ Windows
✅ Linux (Tested on Kali Linux)
✅ macOS

👨‍💻 Author
Made by H4X

yaml
Copy
Edit

---

## ✅ 6. GitHub-এ আপলোড করার কমান্ড (CLI)

```bash
cd advanced-file-finder
git init
git add .
git commit -m "Initial commit - Advanced File Path Finder"
git branch -M main
git remote add origin https://github.com/YourGitHubUsername/advanced-file-finder.git
git push -u origin main
