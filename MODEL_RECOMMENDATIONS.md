# Model Recommendations for OS Automation

Small models (3B–14B parameters) are **not recommended** for OS-level automation. They tend to generate incorrect shell commands, misunderstand system paths, fail multi-step instructions, and hallucinate flags or package names.

For reliable automation, use a model that can reason step by step and understand system internals.

---

## Quick Picks

| Use Case | Recommendation | Via | Why |
|---|---|---|---|
| **Best overall** | Claude Sonnet 4 / DeepSeek-V4 Pro | OpenRouter / API | Top reasoning + current knowledge, excellent tool use |
| **Best reasoning** | Claude Opus 4 / DeepSeek-R1-0528 | OpenRouter / API | Deep chain-of-thought, current knowledge |
| **Best free** | Qwen3-Coder-32B | OpenRouter / Ollama / AirLLM | Best open coding model at 32B, 2025 cutoff |
| **Best local large** | Llama 3.3 70B Instruct | AirLLM (8 GB VRAM) | Strong open model (note: late 2023 cutoff) |
| **Best coding** | Qwen3-Coder-480B / DeepSeek-V3 | OpenRouter / API | Top-tier code generation, 2025 knowledge |
| **Cheapest cloud** | DeepSeek-V3 | API ($0.27/M tokens) | MoE — 660B quality at 37B active cost, 2025 cutoff |
| **Cheapest current** | Qwen3-MoE-30B / Gemini 2.5 Flash | OpenRouter | Sub-$0.30/M, recent knowledge |
| **Fast + cheap + current** | Claude Haiku 3.5 / Gemini 2.5 Flash | OpenRouter / API | Sub-second responses, 2025 knowledge |
| **Best cost/quality** | Mixtral 8x22B | OpenRouter | 141B MoE — near-top quality at mid pricing |
| **Avoid for current tasks** | GPT-4o / GPT-4o-mini / Llama 3.3 70B | — | Late 2023 cutoff — outdated for modern APIs/libs |

---

## Cloud Models (API Key)

Cloud models run on powerful remote hardware, require no local GPU, and give you access to the largest models. Even a small cloud model will generally outperform a large local model on OS tasks due to full-precision inference.

### MoE Models — Best Cost-to-Performance on API Credits

**Mixture-of-Experts (MoE)** models contain many "expert" sub-networks but only activate a small fraction per token. This means you get the quality of a massive model at a fraction of the per-token cost. If you're paying per API credit, MoE models are the ideal choice — you pay for active parameters, not total parameters.

| MoE Model | Total Params | Active Per Token | Via | Pricing |
|---|---|---|---|---|
| **DeepSeek-V3** | ~660B | ~37B | DeepSeek API / OpenRouter | $0.27/M input, $1.10/M output |
| **Mixtral 8x22B** | 141B | 39B | OpenRouter / Ollama | ~$0.65/M input |
| **Mixtral 8x7B** | 47B | 13B | OpenRouter / Ollama | ~$0.25/M input |
| **Qwen3-MoE-30B** | 30B | 3.7B | OpenRouter | Very cheap |
| **DBRX 132B** | 132B | 36B | OpenRouter | ~$1.10/M input |
| **Claude 3.5 Sonnet** | Unknown (MoE) | Unknown | OpenRouter / Anthropic | $3/M input |

**Why MoE for OS automation:** OS tasks require reasoning but not massive token output — commands are typically short. An MoE model gives you the reasoning quality of a 600B+ model while charging you based on ~37B active parameters. On OpenRouter, this can mean 5-10x savings vs. equivalently-capable dense models.

### Dense vs. MoE — Choosing the Right Architecture

| | Dense Models | MoE Models |
|---|---|---|
| **How it works** | Every parameter is used for every token | Only a subset of "experts" activate per token |
| **Examples** | Claude Sonnet 4, GPT-4o, Llama 3.3 70B, Qwen3-Coder-480B | DeepSeek-V3, Mixtral 8x22B, DBRX, Qwen3-MoE |

**Dense models — advantages:**
- **Consistent quality** — every layer is always active, so output is predictable and uniform across all prompt types
- **Better at single-domain depth** — all parameters focus on one problem; excels at deeply technical, narrow tasks
- **Simpler to run locally** — no expert routing overhead; better VRAM predictability
- **Lower latency** — no gating/routing computation; faster per-token generation at the same active parameter count
- **Better at creative/lateral thinking** — full model capacity available for unusual prompts that don't fit an expert's specialty

**Dense models — disadvantages:**
- **Linear cost scaling** — you pay for ALL parameters on every token; a 480B dense model costs per token like a 480B model
- **High VRAM requirement** — must load entire model; 70B+ dense models need 40 GB+ VRAM even quantized
- **Diminishing returns** — beyond ~70B, quality gains per parameter slow down while cost keeps climbing

**MoE models — advantages:**
- **Cost-efficient** — pay for active parameters only (~37B of 660B); 5-10x cheaper than equivalently-capable dense models
- **Massive total capacity** — 600B+ total knowledge distributed across experts; broad domain coverage
- **Specialized experts** — different experts handle different domains (code, math, language, reasoning); the right expert activates for each token
- **Lower VRAM for capability** — a 141B MoE (39B active) fits in less VRAM than a 141B dense model while outperforming it

**MoE models — disadvantages:**
- **Inconsistent quality** — if the router sends a token to the wrong expert, output quality drops; can produce "expert collision" artifacts
- **Weaker at narrow depth** — when a task requires sustained focus on one domain, only a fraction of the model is ever engaged
- **Routing overhead** — adds latency from the gating mechanism; slower at low batch sizes on local hardware
- **Harder to run locally** — expert sharding across GPUs is complex; many inference engines have limited MoE support
- **Prompt sensitivity** — MoE models can be more brittle with unusual prompts that don't clearly map to any expert's training distribution

**Guideline:** Use **MoE** when you need broad capability at low cost (general OS automation, diverse tasks, API usage). Use **dense** when you need consistent, deep focus on one domain (complex debugging sessions, long coding chains, creative problem-solving) or when running locally with limited tooling.

**Cost-saving strategy — hybrid MoE + dense workflow:**
1. Use a cheap **MoE** model (DeepSeek-V3, Mixtral 8x7B) as your primary driver for most tasks
2. If the MoE model hits a problem it can't fix after 1-2 attempts, switch to a dense model (Claude Sonnet, GPT-4o) for that specific fix
3. When calling the dense model, **minimize context length** — send only the relevant error, the failing code/command, and a short instruction. Avoid sending full conversation history
4. Once fixed, switch back to the MoE model for the next steps

This approach keeps the dense model's context window small (reducing per-call cost significantly) while still getting its superior focused reasoning when it's actually needed. You might spend 80% of tokens on cheap MoE and only 20% on dense fixes — cutting total API costs by 3-5x vs. using a dense model for everything.

### All Cloud Models

Models are grouped by knowledge freshness. For OS automation, prefer models with **2025 knowledge** — stale cutoffs produce hallucinated commands, wrong package names, and deprecated APIs.

#### Current Knowledge (2025+) — Recommended

| Model | Provider | Size | Knowledge Cutoff | Notes |
|---|---|---|---|---|
| **Claude Sonnet 4** | Anthropic (via OpenRouter) | Unknown | Early 2025 | Best all-around — excellent at shell, reasoning, tool use |
| **Claude Opus 4** | Anthropic (via OpenRouter) | Unknown | Early 2025 | Top-tier reasoning, best for complex debugging |
| **DeepSeek-V4 Pro** | DeepSeek (via API / OpenRouter) | Unknown (MoE) | 2025 | Latest DeepSeek flagship — strong coding + reasoning |
| **DeepSeek-R1-0528** | DeepSeek (via API / OpenRouter) | ~660B MoE | 2025 | Updated R1 with improved reasoning, current knowledge |
| **Gemini 2.5 Pro** | Google (via OpenRouter) | Unknown | 2025 | Strong reasoning, 1M context, very current knowledge |
| **Gemini 2.5 Flash** | Google (via OpenRouter) | Unknown | 2025 | Fast, cheap, current knowledge, good context handling |
| **Gemini 2.5 Flash Thinking** | Google (via OpenRouter) | Unknown | 2025 | Flash with chain-of-thought — fast + reasoning |
| **GPT-4.1** | OpenAI | Unknown | 2025 | Updated GPT-4 with recent knowledge, better coding |
| **Grok 3** | xAI (via OpenRouter) | Unknown | 2025 | Strong reasoning, very current, large context |
| **DeepSeek-V3** | DeepSeek | ~660B MoE | 2025 | Very large MoE, competitive with top closed models, cheap |
| **Qwen3-Coder-480B** | Alibaba (via OpenRouter) | 480B | 2025 | Largest open coding model — excellent output quality |
| **Qwen3-235B** | Alibaba (via OpenRouter) | 235B | 2025 | Strong general-purpose, good reasoning |
| **Qwen3-MoE-30B** | Alibaba (via OpenRouter) | 30B MoE | 2025 | Ultra-cheap MoE, recent knowledge, good for simple tasks |
| **Llama 4 Maverick** | Meta (via OpenRouter) | Unknown (MoE) | Mid 2025 | Meta's MoE — strong reasoning, very current |
| **Llama 4 Scout** | Meta (via OpenRouter) | Unknown (MoE) | Mid 2025 | Smaller MoE, 10M context, good for long sessions |
| **Claude 3.5 Sonnet** | Anthropic (via OpenRouter) | Unknown (MoE) | Early 2025 | Strong coding, very reliable |
| **Claude 3.5 Haiku** | Anthropic (via OpenRouter) | Unknown | Early 2025 | Fast, cheap, good for simple tasks |
| **Mistral Small 3.1** | Mistral (via OpenRouter) | 24B | 2025 | Efficient, recent knowledge, good for simple automation |
| **Codestral** | Mistral (via OpenRouter) | 22B | 2025 | Code-specialized, very current, good at shell |
| **Phi-4** | Microsoft (via OpenRouter) | 14B | 2025 | Small but strong reasoning, good for constrained budgets |
| **Command R+** | Cohere (via OpenRouter) | 104B | 2025 | Good tool use, strong at structured output |

#### Dated Knowledge (2024 and earlier) — Use with Caution

| Model | Provider | Size | Knowledge Cutoff | Notes |
|---|---|---|---|---|
| **Mistral Large 2** | Mistral (via OpenRouter) | 123B | 2024 | Strong model but dated — verify commands against docs |
| **DeepSeek-R1** | DeepSeek | ~660B MoE | 2024 | Good reasoning, but knowledge is aging |
| **Mixtral 8x22B** | Mistral (via OpenRouter) | 141B MoE | 2024 | Excellent cost/quality, but verify current packages |
| **DBRX 132B** | Databricks (via OpenRouter) | 132B MoE | 2024 | Strong open MoE, but older knowledge |
| **GPT-4o** | OpenAI | Unknown | Late 2023 | Strong generalist, but frequently wrong about current APIs/libs |
| **GPT-4o-mini** | OpenAI | Unknown | Late 2023 | Cheap but dated — avoid for any task involving modern tooling |
| **Llama 3.3 70B** | Meta (via OpenRouter) | 70B | Late 2023 | Strong open model, but badly outdated for current work |

### Knowledge Cutoff — Why It Matters for OS Automation

OS automation relies on current information: package versions, API endpoints, CLI flags, library features, and platform quirks. A model with a stale knowledge cutoff will:

- Hallucinate deprecated flags and removed commands
- Recommend outdated packages or broken install methods
- Be unaware of new language features, framework APIs, or security practices
- Fail silently because it doesn't know what it doesn't know

**Current knowledge models (2025+) — use these for automation:**
Claude Sonnet 4, Claude Opus 4, DeepSeek-V4 Pro, DeepSeek-R1-0528, Gemini 2.5 Pro, Gemini 2.5 Flash, GPT-4.1, Grok 3, DeepSeek-V3, Qwen3-Coder-480B, Qwen3-235B, Llama 4 Maverick, Claude 3.5 Sonnet, Codestral, Phi-4, Command R+

**Dated models — avoid for any task involving modern tooling:**
GPT-4o (late 2023), GPT-4o-mini (late 2023), Llama 3.3 70B (late 2023), DeepSeek-R1 (2024), Mixtral 8x22B (2024), Mistral Large 2 (2024), DBRX 132B (2024) — these will frequently suggest outdated commands, wrong package names, and deprecated APIs. Only use them for pure logic/debugging where current information doesn't matter.

**Rule of thumb:** If you're installing packages, using APIs, or working with frameworks released in the last 18 months, use a 2025+ model. For pure logic/debugging tasks where external knowledge is irrelevant, older models are fine.

**API key sources:**
- [OpenRouter](https://openrouter.ai) — unified access to 200+ models, pay-as-you-go
- [OpenAI](https://platform.openai.com) — GPT-4o, GPT-4o-mini
- [DeepSeek](https://platform.deepseek.com) — DeepSeek-V3, DeepSeek-R1
- [HuggingFace](https://huggingface.co) — Serverless Inference API
- [Google AI](https://aistudio.google.com) — Gemini models

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
