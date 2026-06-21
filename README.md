<div align="center">

# ⚡ Commit-Sense

<img src="https://img.shields.io/badge/Security-Strict-red?style=for-the-badge&logo=shield" />
<img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge&logo=gnu" />

**The AI-Powered Git Hook & Security Guardian for Senior Developers.**

</div>

## 💡 What is Commit-Sense?

Commit-Sense is a blazing fast, terminal-based CLI tool designed to protect your codebase and automate your git workflow. It acts as a gatekeeper between you and `git commit`.

### Key Features:
*   **🛡️ Anti-Leak Engine**: Scans your staged files (`git diff --cached`) for accidental inclusions of AWS Access Keys, GitHub Tokens, OpenAI API Keys, and RSA Private Keys. It aborts the commit instantly if a leak is detected.
*   **🤖 AI Commit Generator**: If your code is secure, it analyzes your diff heuristically to generate a perfectly formatted `Conventional Commit` message (e.g., `feat(core): update main.py`).
*   **🎨 Cyberpunk TUI**: Beautiful, colorful terminal interface built with `rich`.

## 🚀 Installation

```bash
git clone https://github.com/mehmetxkrkmz/commit-sense.git
cd commit-sense
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 💻 Usage

Instead of running `git commit`, simply run:
```bash
python3 main.py
```
If your code is clean, it will suggest a commit message for you to use!

## 📜 License
This project is licensed under the **GNU GPLv3 License**. See the `LICENSE` file for details. This ensures the tool remains free and open-source forever.
