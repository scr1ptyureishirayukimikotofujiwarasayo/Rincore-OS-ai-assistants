# AI Assistant — Linux · Windows · macOS

A terminal-based AI coding companion that connects to any LLM and can run commands, control a browser, automate your desktop, test programs, self-diagnose and fix errors, and more — across all three major operating systems.

---

## Quick Start

```bash
# 1. Extract the zip for your OS
# 2. Install dependencies
pip install -r requirements.txt
# 3. Install browser engine (for /browser mode)
python -m playwright install chromium
# 4. Launch!
python main.py
```

On first run you'll be guided through picking an AI provider and model.

---

## What It Can Do

| Capability | Description |
|---|---|
| **Chat + Code** | Natural language conversation, code block execution, auto-fix on errors |
| **Chat Mode** | Pure conversation mode (`/chat`) — no code, no tools, just talk |
| **Browser Control** | Full Playwright-powered browser — navigate, click, type, extract data, take screenshots |
| **Desktop Automation** | Mouse, keyboard, and window control via pyautogui (`/autotask` mode) |
| **Program Testing** | Open any program and have the AI test its functionality (`/test`) |
| **Program Automation** | Use any desktop program to accomplish a task (`/automate`) |
| **Process Monitoring** | Run a program and capture crash data — exit code, Event Log, output (`/monitor`) |
| **Autonomous Build** | AI plans, writes code, executes, debugs — no confirmation needed (`/build`, `/fullyauto`) |
| **Full Autonomy** | AI chooses the right tool (search, browse, autotask, test, automate, monitor, code) for each step |
| **Sandbox Testing** | Isolated temporary directory for testing scripts before running them for real (`/sandbox`) |
| **Structured Plans** | Break complex tasks into numbered steps, track progress (`/plan`, `/status`) |
| **Web Search** | Live DuckDuckGo search with auto-updating library — triggered by the AI or manually |
| **Self-Fixing** | AI diagnoses crash/error logs and auto-executes fixes (`/reviewerrorlogs`, `/selffix`) |
| **Deep Repair** | Full project scan — syntax checks, deps, error logs — AI fixes everything (`/deepfix`) |
| **Plan Notes** | AI saves goals & progress to disk; resumes where it left off (`/note`, `/takenote`, `/reviewnotes`) |
| **Conversation Save** | Save/load entire conversation history as JSON (`/saveconversation`, `/loadconversation`) |
| **Activity Logging** | Full timeline of every action — AI self-reviews via `[REVIEWACTIVITY]` in fullyauto |
| **Multi-Model Orchestration** | Pick 3 OpenRouter models — router classifies task difficulty, delegates planning + execution to the right model for cost efficiency |
| **Smart Context** | Auto-compacts conversation when too large — logs state to activity trail, clears old context, AI resumes from activity log without losing place |
| **Anti-Crash** | Auto-recovers from errors — logs, resets state, restarts up to 3 times before exiting |
| **Command Logging** | Every shell command logged with timestamp, exit code, and full output |
| **Error Logging** | All crashes and unhandled errors logged to `error_logs/` for diagnosis |
| **Cleanup** | `/cleanup` command or `cleanup.sh`/`cleanup.bat` to clear all logs for Git

---

## Providers

The assistant supports 4 AI backends:

| # | Provider | Type | Notes |
|---|---|---|---|
| 1 | **Ollama** | Local | Install / remove / list models from the menu |
| 2 | **OpenAI** | Cloud API | Auto-fetches models — key saved for reuse |
| 3 | **DeepSeek** | Cloud API | Auto-fetches models — key saved for reuse |
| 4 | **OpenRouter** | Cloud API | 200+ models — multi-model orchestration — key saved for reuse |

### Multi-Model Orchestration

With OpenRouter, pick 3 models — a cheap router that classifies task difficulty (easy/medium/hard) and delegates planning + execution to the right model. Easy tasks go to the cheap model, hard tasks to the heavy one — cutting API costs 3-5x.

---

## Commands

Press `s` at any time during autonomous modes to gracefully stop.

### Chat Commands

| Command | Description |
|---|---|
| `/help` | Show help |
| `/chat [topic]` | Pure conversation mode — no code, no tools. `exit` to leave |
| `/toggle` | Toggle auto web search |
| `/search <q>` | Force a web search |
| `/auto` | Toggle auto-execution (skip confirmations) |
| `/logs [N]` | Show last N command logs |
| `/clearcommandlogs` | Delete all command logs |
| `/clearerrorlogs` | Delete all error logs |
| `/clearapikeys` | Delete all saved API keys |
| `/cleanup` | Clear all logs (command, error, activity, notes) |
| `/review` | AI inspects recent logs for mistakes |
| `/reviewerrorlogs` | AI diagnoses crash/error logs AND auto-executes fixes |
| `/selffix` | Aggressive self-fixing — scans all logs, auto-diagnoses and fixes across 5 turns |
| `/deepfix` | Deep project-wide repair — scans files, syntax, deps, logs; fixes across 8 turns |
| `/note <text>` | Save a plan note for later recall |
| `/takenote <topic>` | AI analyzes a topic and saves a comprehensive note |
| `/reviewnotes` | AI reviews all plan notes and summarizes goals/progress |
| `/clearnotes` | Delete all plan note files |
| `/saveconversation` | Save current conversation to disk (prompts for name) |
| `/loadconversation` | List and load a previously saved conversation |
| `/clearconversations` | Delete all saved conversation files |
| `/reviewactivitylogs` | AI reviews full activity timeline — all actions, tool usage, events |
| `/clearactivitylogs` | Delete all activity log files |
| **Modes** | |
| `/build <desc>` | Auto-build — AI writes + executes autonomously |
| `/fullyauto [goal]` | Full autonomy — AI controls ALL tools. Press `s` to stop anytime |
| `/browser [--visible] [url]` | Browser automation (Playwright) |
| `/autotask [program]` | Desktop automation (mouse/keyboard) |
| `/test <program>` | Open a program and test its functionality |
| `/automate <program> <task>` | Open a program and automate a task with it |
| `/monitor <program>` | Run a program and capture crash data for AI diagnosis |
| `/sandbox [goal]` | Isolated test environment |
| `/plan <goal>` | Structured step-by-step plan |
| `/status` | Show plan progress |
| `/changemodel` | Switch the active model |
| `/mainmenu` | Reselect AI provider, fresh session |
| `/resetassistant` | Clear logs, wipe conversation history |
| `exit` | Quit the assistant |

### Direct Commands

| Command | Description |
|---|---|
| `!bash <cmd>` | Execute shell directly *(Linux: `!bash`, Windows: `!ps`/`!cmd`, macOS: `!bash`)* |
| `!read <path>` | Read a file |
| `!write <path>` | Write to a file (paste content, end with `EOF`) |
| `!cd <dir>` | Change working directory |
| `!run <lang>` | Execute code (paste content, end with `EOF`) |
| `!npm <args>` | Run npm |
| `!pip <args>` | Run pip |
| `!browse <action>` | Direct browser command |
| `!autotask <action>` | Direct desktop automation |

### Browser Actions

`navigate`, `go`, `search`, `click`, `type`, `extract`, `html`, `scroll`, `screenshot`, `url`, `title`, `press`, `script`, `wait`, `select`, `close`, `popups`, `captcha`, `solve-captcha`

### Autotask Actions

`open`, `launch`, `find`, `window`, `windows`, `move`, `click`, `doubleclick`, `rightclick`, `drag`, `type`, `press`, `key`, `hotkey`, `scroll`, `screenshot`, `locate`, `locateall`, `pos`, `resolution`, `wait`, `close`

---

## OS Differences

| Feature | Linux | Windows | macOS |
|---|---|---|---|
| Shell | `bash` (`!bash`) | `powershell` (`!ps`) or `cmd` (`!cmd`) | `zsh` (`!bash`) |
| Package hints | `apt` | `winget` / `choco` | `brew` |
| Sudo prompt | Yes | No (admin handled by shell) | Yes |
| Autotask | pyautogui | pyautogui + pygetwindow | pyautogui (needs accessibility permissions) |
| Paths | `/home/` | `C:\Users\` | `/Users/` |
| Cleanup script | `cleanup.sh` | `cleanup.bat` | `cleanup.sh` |
| Anti-crash | Yes (3 retries) | Yes (3 retries) | Yes (3 retries) |

---

## Project Structure

```
assistant/
├── main.py                  # Entry point + chat loop + all mode handlers
├── executor.py              # OS command execution + logging + monitoring
├── browser_agent.py         # Playwright browser automation
├── autotask_agent.py        # Mouse/keyboard/window control
├── planner.py               # Structured task planning
├── cleanup.sh / cleanup.bat # Clear all logs for Git-ready state
├── requirements.txt
├── COMMANDS.txt
├── MODEL_RECOMMENDATIONS.md
├── .gitignore
├── command_logs/            # Per-command structured logs
├── error_logs/              # Crash and unhandled error logs
├── plan_notes/              # AI plan notes (persistent memory)
├── conversations/           # Saved conversation JSON files
├── activity_logs/           # Full activity timeline — every action logged
├── autotask_screenshots/    # Desktop automation screenshots
├── browser_screenshots/     # Browser automation screenshots
└── assistant_core/
    ├── __init__.py
    ├── config.json          # Auto-update settings
    ├── llm.py               # LLM communication (Ollama + cloud APIs)
    ├── provider.py          # Provider selection + model management
    ├── platform_utils.py    # OS detection, shell config
    ├── search.py            # DuckDuckGo search
    ├── search_engine.py     # Search with auto-update
    └── update_manager.py    # PyPI version checker
```

---

## Model Recommendations

For complex OS automation tasks, use larger models. See [`MODEL_RECOMMENDATIONS.md`](MODEL_RECOMMENDATIONS.md) in any assistant zip for detailed guidance.

**Quick picks:**
- **Best overall**: Claude Sonnet 4 via OpenRouter
- **Best free**: Qwen3-Coder-32B via OpenRouter / Ollama
- **Best local**: Any 7B–70B model via Ollama
- **Cheapest cloud**: DeepSeek-V3 at $0.27/M tokens
- **Cost tip**: MoE models activate only a fraction of parameters per token — 5-10x cheaper than dense models on API credits
- **Multi-model tip**: With OpenRouter, pick 3 models (cheap router + mid + heavy) — the assistant auto-routes easy tasks to the cheap model and hard tasks to the heavy one, cutting costs 3-5x

---

## License

MIT — see `LICENSE` in each assistant zip.
