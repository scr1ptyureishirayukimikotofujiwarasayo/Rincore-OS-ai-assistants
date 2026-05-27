# 🖥️ AI Assistant — Linux · Windows · macOS

A terminal-based AI coding companion that connects to any LLM and can run commands, control a browser, automate your desktop, and test scripts in a sandbox — across all three major operating systems.


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
| **Chat + Code** | Natural language conversation with the AI, code block execution, auto-fix on errors |
| **Browser Control** | Full Playwright-powered browser — navigate, click, type, extract data, take screenshots |
| **Desktop Automation** | Mouse, keyboard, and window control via pyautogui (`/autotask` mode) |
| **Autonomous Build** | AI plans, writes code, executes, debugs — no confirmation needed (`/build`, `/fullyauto`) |
| **Sandbox Testing** | Isolated temporary directory for testing scripts before running them for real (`/sandbox`) |
| **Structured Plans** | Break complex tasks into numbered steps, track progress (`/plan`, `/status`) |
| **Web Search** | Live DuckDuckGo search with auto-updating library — triggered by the AI or manually |
| **Command Logging** | Every shell command is logged with timestamp, exit code, and full output |
| **Save & Restore** | Export/import conversation state as JSON — store on any cloud drive |

---

## Providers

The assistant supports 7 AI backends out of the box:

| # | Provider | Type | Model Management |
|---|---|---|---|
| 1 | **Ollama** | Local | Install / remove / list models from the menu |
| 2 | **LM Studio** | Local | List models, install via GUI |
| 3 | **OpenAI** | Cloud API | Fetch available models, or type manually |
| 4 | **DeepSeek** | Cloud API | Fetch available models, or type manually |
| 5 | **OpenRouter** | Cloud API | Type model ID (proxies 200+ models: Claude, Llama, Qwen...) |
| 6 | **HuggingFace** | Cloud API | Type model ID (Inference API) |
| 7 | **AirLLM** | Local | Run 70B+ models on consumer GPU via layer-by-layer offloading |

### AirLLM — Run Large Models Locally

Uses [airllm](https://github.com/lyogavin/airllm) to load models one layer at a time into GPU — a 70B model can run on a laptop with 8 GB VRAM. Pick a model from a local folder, a HuggingFace repo ID, or a download URL. Supports 4-bit compression via bitsandbytes.

```bash
pip install airllm bitsandbytes   # optional for 4-bit
```

---

## Commands

### Chat Commands

| Command | Description |
|---|---|
| `/help` | Show help |
| `/toggle` | Toggle auto web search |
| `/search <q>` | Force a web search |
| `/auto` | Toggle auto-execution (skip confirmations) |
| `/logs [N]` | Show last N command logs |
| `/clearcommandlogs` | Delete all logs |
| `/review` | AI inspects recent logs for mistakes |
| **Modes** | |
| `/build <desc>` | Auto-build — AI writes + executes autonomously |
| `/fullyauto [goal]` | Full autonomy — AI controls everything |
| `/browser [--visible] [url]` | Browser automation (Playwright) |
| `/autotask [program]` | Desktop automation (mouse/keyboard) |
| `/sandbox [goal]` | Isolated test environment |
| `/plan <goal>` | Structured step-by-step plan |
| `/status` | Show plan progress |
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
| Autotask | pyautogui | pyautogui + pygetwindow | pyautogui |
| Paths | `/home/` | `C:\Users\` | `/Users/` |

---

## Project Structure

```
assistant/
├── main.py                  # Entry point + chat loop
├── executor.py              # OS command execution
├── browser_agent.py         # Playwright browser automation
├── autotask_agent.py        # Mouse/keyboard/window control
├── planner.py               # Structured task planning
├── save_load.py             # Export/import conversation state
├── requirements.txt
├── COMMANDS.txt
├── MODEL_RECOMMENDATIONS.md
├── command_logs/            # Per-command structured logs
│   └── .gitkeep
└── assistant_core/
    ├── __init__.py
    ├── config.json          # Auto-update settings
    ├── llm.py               # LLM communication (7 providers)
    ├── provider.py          # Provider selection + model management
    ├── search.py            # DuckDuckGo search
    ├── search_engine.py     # Search with auto-update
    └── update_manager.py    # PyPI version checker
```

---

## Model Recommendations

For complex OS automation tasks, use larger models. See [`MODEL_RECOMMENDATIONS.md`](MODEL_RECOMMENDATIONS.md) in any assistant zip for detailed guidance.

**Quick picks:**
- **Best overall**: Claude Sonnet 4 via OpenRouter
- **Best free**: Qwen3-Coder-32B via OpenRouter / Ollama / AirLLM
- **Best local large**: Any 70B+ model via AirLLM (runs on 8 GB VRAM)
- **Cheapest cloud**: DeepSeek-V3 at $0.27/M tokens

---

## License

MIT — see `LICENSE` in each assistant zip.
