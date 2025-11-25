# Generative Shell-composer (Gensh)


* A natural-language to shell command converter CLI tool. It allows you to type instructions in plain English, and it generates OS-specific shell commands safely. It also includes diagnostic tools, command explanation, history tracking, and configuration management.

---

## Features

```markdown
- Convert natural-language instructions into shell commands
- Supports multiple OS modes: Windows, Linux, macOS
- Risk analysis for potentially dangerous commands
- Command history tracking (last 50 commands)
- Configure API key, model, OS, and temperature
- Diagnostic tools for verifying API and model connectivity
- Explain shell commands with detailed breakdowns
- Version command to check current Gensh version
```

---

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd gensh
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the environment:

* **Windows:**

```bash
venv\Scripts\activate
```

* **Linux/macOS:**

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -e .
```

This will install `typer`, `rich`, `google-generativeai`, and other required packages.

---

## Usage

All commands use the `gensh` CLI.

### Run Commands

Generate shell commands from natural language:

```bash
gensh run "<instruction>" [--dry-run/--run]
```

* `--dry-run` (default) – shows the command without executing it.
* `--run` – executes the command.

**Example:**

```bash
gensh run "count the number of files in the folder"
```

Output:

```
Generated command: (Get-ChildItem -File | Measure-Object).Count
Explanation: Counts the number of files in the current directory.
Risk level: LOW
Dry run: Command not executed.
```

---

### Configuration

Manage Gensh configuration:

```bash
gensh config show           # Show all config values
gensh config get <key>      # Get a single config key
gensh config set <key> <value>  # Update a config value
gensh config reset          # Reset to defaults
```
* Defalut OS Configuration : Windows

* Keys include `api_key`, `model`, `os`, `temperature`. 
* Temperature is a float value (0.0–1.0) controlling command generation randomness.

**Example:**

```bash
gensh config set os linux
gensh config set temperature 0.3
```

---

### OS Quick Commands

Switch OS modes quickly:

```bash
gensh os windows
gensh os linux
gensh os mac
```

Or use:

```bash
gensh os set <os>
```

---

### History

Track your commands:

```bash
gensh history show   # Show last 50 commands
gensh history clear  # Clear command history
```

---

### Tools

Diagnostic and reverse-analysis tools:

```bash
gensh tools diagnose         # Verify config, API, and model
gensh tools models           # List available Gemini models
gensh tools explain "<command>"  # Explain a shell command
```

---

### Version

Check the current Gensh version:

```bash
gensh version
```

---

## Command Reference

| Command                                       | Description                                                  |
| --------------------------------------------- | ------------------------------------------------------------ |
| `gensh run "<instruction>" [--dry-run/--run]` | Generate shell commands from natural language.               |
| `gensh version`                               | Show the current Gensh version.                              |
| `gensh config show`                           | Display all configuration values.                            |
| `gensh config get <key>`                      | Get a single configuration value.                            |
| `gensh config set <key> <value>`              | Update a configuration value (e.g., OS, model, temperature). |
| `gensh config reset`                          | Reset configuration to defaults.                             |
| `gensh os set <os>`                           | Set OS mode explicitly.                                      |
| `gensh os windows`                            | Quick set OS to Windows.                                     |
| `gensh os linux`                              | Quick set OS to Linux.                                       |
| `gensh os mac`                                | Quick set OS to macOS.                                       |
| `gensh history show`                          | Show the last 50 commands executed.                          |
| `gensh history clear`                         | Clear all command history.                                   |
| `gensh tools diagnose`                        | Check configuration, API key, and model.                     |
| `gensh tools models`                          | List available Gemini models for your API key.               |
| `gensh tools explain "<command>"`             | Ask Gemini to explain what a shell command does.             |

---

## Supported OS

* Windows (PowerShell)
* Linux (bash, sh)
* macOS (zsh, bash)

Gensh ensures commands are OS-specific and safe to run.

---

## Safety

* All generated commands are analyzed for risk.
* Risk levels: `LOW`, `MEDIUM`, `HIGH`.
* Dangerous commands (like `rm -rf`) are flagged.

---

## Requirements

* Python >= 3.10 (3.11 recommended)
* Gemini API key (`gemini_api_key`) for command generation
* Internet connection for API requests

---

## Development

* Source code is under `cli/` and `core/`.
* Config file: `config/settings.json`
* Virtual environment recommended (`venv/`)

```markdown
Happy scripting with Gensh — turning your instructions into shell commands!  

Powered by Python, fueled by coffee, guided by late-night curiosity ☕🚀
```

---