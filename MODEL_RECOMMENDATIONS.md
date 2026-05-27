# Model Recommendations for OS Automation

Small models (3B–14B parameters) are **not recommended** for OS-level automation. They tend to generate incorrect shell commands, misunderstand system paths, fail multi-step instructions, and hallucinate flags or package names.

For reliable automation, use a model that can reason step by step and understand system internals.

---

## Quick Picks

| Use Case | Recommendation | Via |
|---|---|---|
| **Best overall** | Claude Sonnet 4 | OpenRouter |
| **Best free** | Qwen3-Coder-32B | OpenRouter / Ollama / AirLLM |
| **Best local large** | Llama 3.3 70B Instruct | AirLLM (8 GB VRAM) |
| **Best coding** | DeepSeek-V3 / Qwen3-Coder-480B | OpenRouter / API |
| **Cheapest cloud** | DeepSeek-V3 | API ($0.27/M tokens) |
| **Fast + cheap** | Claude Haiku 3.5 / GPT-4o-mini | OpenRouter / API |

---

## Cloud Models (API Key)

Cloud models run on powerful remote hardware, require no local GPU, and give you access to the largest models. Even a small cloud model will generally outperform a large local model on OS tasks due to full-precision inference.

| Model | Provider | Size | Notes |
|---|---|---|---|
| **Claude Sonnet 4** | Anthropic (via OpenRouter) | Unknown | Best all-around — excellent at shell, reasoning, tool use |
| **GPT-4o** | OpenAI | Unknown | Strong generalist, good command generation |
| **DeepSeek-V3** | DeepSeek | ~660B | Very large, competitive with top closed models, cheap |
| **Qwen3-Coder-480B** | Alibaba (via OpenRouter) | 480B | Specialized for coding — excellent output quality |
| **Claude Haiku 3.5** | Anthropic (via OpenRouter) | Unknown | Fast, cheap, good for simple tasks |
| **GPT-4o-mini** | OpenAI | Unknown | Cheapest OpenAI option, decent for quick tasks |
| **Llama 3.3 70B** | Meta (via OpenRouter) | 70B | Strong open-weight model |

**API key sources:**
- [OpenRouter](https://openrouter.ai) — unified access to 200+ models, pay-as-you-go
- [OpenAI](https://platform.openai.com) — GPT-4o, GPT-4o-mini
- [DeepSeek](https://platform.deepseek.com) — DeepSeek-V3, DeepSeek-R1
- [HuggingFace](https://huggingface.co) — Serverless Inference API

---

## Local Models (Ollama / LM Studio)

If you have a GPU with enough VRAM, you can run models locally. Quantization (Q4, Q8) reduces VRAM needs with minimal quality loss.

| Model | Size | Min VRAM | Quality |
|---|---|---|---|
| **Qwen3-Coder-32B** (Q4) | ~18 GB | 24 GB | Best local option for OS automation |
| **Llama 3.3 70B** (Q4) | ~40 GB | 48 GB | Excellent — near cloud quality |
| **DeepSeek-Coder-V2-Lite** (Q4) | ~16 GB | 20 GB | Good coding, decent commands |
| **Mistral 7B** / **Llama 3.1 8B** | ~5 GB | 8 GB | Usable for simple tasks only |
| **Phi-4 14B** (Q4) | ~8 GB | 12 GB | Decent for basic automation |

### What You Can Run by VRAM

| VRAM | Practical range |
|---|---|
| 4–8 GB | 7B–8B models (simple tasks) |
| 8–12 GB | 7B–14B models (basic automation) |
| 12–16 GB | 14B–22B models (usable) |
| 16–24 GB | 22B–32B models (good, recommended minimum) |
| 24–48 GB | 32B–70B models (excellent) |
| 48 GB+ | 70B+ models (near cloud quality) |

---

## AirLLM — Large Models on Consumer Hardware

AirLLM uses **layer-by-layer inference** — loads one layer at a time into GPU, runs it, then offloads and loads the next. This lets you run 70B+ models on as little as 8 GB VRAM (or CPU only, slowly).

**Pros:**
- 70B models on a laptop GPU
- No massive VRAM required
- Supports 4-bit compression for even lower memory

**Cons:**
- Not as fast as full-GPU inference
- Only supports certain architectures (Llama, Mistral, Mixtral, Qwen, ChatGLM, Baichuan, InternLM)
- Python-only — no OpenAI-compatible server

```bash
pip install airllm bitsandbytes
```

**Recommended AirLLM models:**

| Model | HuggingFace Repo | Why |
|---|---|---|
| Llama 3.3 70B Instruct | `meta-llama/Llama-3.3-70B-Instruct` | Best all-around open model |
| Qwen2.5 72B Instruct | `Qwen/Qwen2.5-72B-Instruct` | Excellent coding |
| Mixtral 8x22B | `mistralai/Mixtral-8x22B-Instruct-v0.1` | Good MoE model |
| DeepSeek-R1 Distill 70B | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B` | Strong reasoning |

---

## Why Size Matters

OS automation is harder than casual chat:

1. **Command precision** — one wrong flag can delete files or break services
2. **Multi-step reasoning** — installs involve repos, dependencies, PATH config
3. **Error recovery** — the model must read error output and adjust
4. **System awareness** — paths, permissions, environment variables, OS quirks

Larger models (70B+) handle all of these significantly better than small models.

---

## OS-Specific Tips

### Linux
- Package manager: `apt` (Debian/Ubuntu), `dnf` (Fedora), `pacman` (Arch)
- Paths: `/home/`, `/etc/`, `/usr/local/`
- Sudo available for privileged operations

### Windows
- Shell: PowerShell (`!ps`) or Command Prompt (`!cmd`)
- Package managers: `winget`, `choco`
- Paths: `C:\Users\`, `C:\Program Files\`
- Admin elevation handled by the shell

### macOS
- Package manager: Homebrew (`brew`)
- Shell: zsh (default), bash 3.2 also available
- Paths: `/Users/`, `/Applications/`, `~/Library/`
- pyautogui needs Accessibility permissions in System Settings
- Gatekeeper and SIP can block some operations
