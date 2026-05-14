# linux_ai_assistant.py - Part 1
import os
import sys
import json
import requests
import socket
import subprocess
import re
from datetime import datetime
from duckduckgo_search import DDGS

def check_internet():
    """Return True if internet is reachable (Google DNS)."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def main():
    print("=== Local OS AI Assistant (Linux) ===")

    # Sudo mode selection
    sudo_choice = input("Run commands with sudo? (y/n): ").lower().strip()
    use_sudo = sudo_choice == 'y'
    if use_sudo:
        print("Sudo mode enabled - commands will be prefixed with sudo where needed")
    else:
        print("Normal user mode selected")

    # Provider selection
    print("\nSelect AI Provider:")
    print("1. Ollama (local)")
    print("2. LM Studio (local)")
    print("3. API Keys (OpenAI, Anthropic, custom)")
    provider_choice = input("Enter 1, 2, or 3: ").strip()

    # ---------- Part 2 ----------
    # Helper functions to get model lists
    def get_ollama_models():
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=5)
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                return [m["name"] for m in models]
            else:
                print("Failed to connect to Ollama. Is it running?")
                return []
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            return []

    def get_lmstudio_models():
        try:
            resp = requests.get("http://localhost:1234/v1/models", timeout=5)
            if resp.status_code == 200:
                models = resp.json().get("data", [])
                return [m["id"] for m in models]
            else:
                print("Failed to connect to LM Studio. Is it running?")
                return []
        except Exception as e:
            print(f"Error connecting to LM Studio: {e}")
            return []

    def get_api_models(base_url, api_key):
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            resp = requests.get(f"{base_url}/v1/models", headers=headers, timeout=10)
            if resp.status_code == 200:
                models = resp.json().get("data", [])
                return [m["id"] for m in models]
            else:
                print(f"Failed to get models: {resp.text}")
                return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    # Provider-specific logic
    if provider_choice == "1":
        print("\nConnecting to Ollama...")
        models = get_ollama_models()
        if not models:
            print("No Ollama models found. Please ensure Ollama is running and has models installed.")
            sys.exit(1)
        print("Available models:")
        for idx, m in enumerate(models):
            print(f"{idx+1}. {m}")
        model_idx = int(input("Select model number: ")) - 1
        selected_model = models[model_idx]
        provider_type = "ollama"
        api_key = None
        base_url = None

    elif provider_choice == "2":
        print("\nConnecting to LM Studio...")
        models = get_lmstudio_models()
        if not models:
            print("No LM Studio models found. Please ensure LM Studio server is running (default port 1234).")
            sys.exit(1)
        print("Available models:")
        for idx, m in enumerate(models):
            print(f"{idx+1}. {m}")
        model_idx = int(input("Select model number: ")) - 1
        selected_model = models[model_idx]
        provider_type = "lmstudio"
        api_key = None
        base_url = "http://localhost:1234"

    elif provider_choice == "3":
        print("\nAPI Key Provider Setup")
        provider_name = input("Provider name (e.g., OpenAI, Anthropic, custom): ").strip()
        api_key = input("Enter API key: ").strip()
        base_url = input("Enter base URL (e.g., https://api.openai.com or http://localhost:1234): ").strip()
        if not base_url.startswith("http"):
            base_url = "https://" + base_url
        base_url = base_url.rstrip("/")
        print(f"Fetching models from {base_url}...")
        models = get_api_models(base_url, api_key)
        if not models:
            print("No models found or failed to fetch. You may still proceed with a manual model name.")
            manual_model = input("Enter model name manually (or press Enter to exit): ").strip()
            if not manual_model:
                sys.exit(1)
            selected_model = manual_model
        else:
            print("Available models:")
            for idx, m in enumerate(models):
                print(f"{idx+1}. {m}")
            model_idx = int(input("Select model number: ")) - 1
            selected_model = models[model_idx]
        provider_type = "api"
    else:
        print("Invalid choice")
        sys.exit(1)

    print(f"\nSelected model: {selected_model}")

    # Store configuration for the chat loop
    config = {
        "provider_type": provider_type,
        "model": selected_model,
        "api_key": api_key,
        "base_url": base_url,
        "use_sudo": use_sudo
    }

    # ---------- Part 3 ----------
    def execute_bash(command, use_sudo=False, cwd=None):
        """Execute a bash command and return result object."""
        try:
            # Prefix with sudo if enabled and not already present
            if use_sudo and not command.strip().startswith("sudo"):
                command = f"sudo {command}"
            result = subprocess.run(
                ["bash", "-c", command],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=cwd
            )
            return result
        except subprocess.TimeoutExpired:
            class MockResult:
                def __init__(self):
                    self.returncode = 1
                    self.stdout = ""
                    self.stderr = "Command timed out after 30 seconds."
            return MockResult()
        except Exception as e:
            class MockResult:
                def __init__(self):
                    self.returncode = 1
                    self.stdout = ""
                    self.stderr = f"Error: {e}"
            return MockResult()

    def run_os_command(command, use_sudo=False, cwd=None):
        """
        Execute a bash command.
        Returns (output, success_flag)
        """
        result = execute_bash(command, use_sudo, cwd)
        success = result.returncode == 0
        output = result.stdout + result.stderr
        log_command(command, output, success)
        return output, success

    def confirm_action(command):
        """Ask user for confirmation before executing a command."""
        print(f"\n[!] Command to execute (bash):")
        print(f"    {command}")
        confirm = input("Execute? (y/n): ").strip().lower()
        return confirm == 'y'

    def log_command(command, output, success):
        """Log command execution details to file."""
        log_path = os.path.expanduser("~/command_log.txt")
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Success: {success}\n")
                f.write(f"Command: {command}\n")
                f.write(f"Output :\n{output}\n")
        except Exception as e:
            print(f"Logging error: {e}")

    # ---------- Part 4 - Chat Loop ----------
    def web_search(query, max_results=3):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                return results
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def trim_output(output, max_chars=300):
        output = output.strip()
        if len(output) > max_chars:
            return output[:max_chars] + f"…[+{len(output)-max_chars}]"
        return output

    def generate_response(messages, config):
        provider = config["provider_type"]
        model = config["model"]

        if provider == "ollama":
            url = "http://localhost:11434/api/chat"
            payload = {"model": model, "messages": messages, "stream": False, "options": {"num_predict": 1024}}
            try:
                resp = requests.post(url, json=payload, timeout=60)
                if resp.status_code == 200:
                    return resp.json()["message"]["content"]
            except Exception as e:
                return f"Error: {e}"

        elif provider == "lmstudio":
            url = f"{config['base_url']}/v1/chat/completions"
            headers = {"Content-Type": "application/json"}
            payload = {"model": model, "messages": messages, "stream": False, "max_tokens": 1024}
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=60)
                if resp.status_code == 200:
                    return resp.json()["choices"][0]["message"]["content"]
                else:
                    return f"Error: {resp.text}"
            except Exception as e:
                return f"Error: {e}"

        elif provider == "api":
            url = f"{config['base_url']}/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config['api_key']}"
            }
            payload = {"model": model, "messages": messages, "stream": False, "max_tokens": 1024}
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=60)
                if resp.status_code == 200:
                    return resp.json()["choices"][0]["message"]["content"]
                else:
                    return f"Error: {resp.text}"
            except Exception as e:
                return f"Error: {e}"

        else:
            return "Unknown provider"

    def chat_loop(config):
        print("\n=== Chat Started ===")
        print("Type 'exit' to quit, '/search <query>' to force a web search, '/toggle' to enable/disable auto-search")
        print("Type '!bash <command>' for direct bash execution")

        messages = []
        cwd_state = {"path": os.path.expanduser("~")}
        system_prompt = (
            "You are an autonomous Linux OS agent. You EXECUTE tasks — never instruct the user.\n"
            "For EVERY OS task, emit one or more commands in ```bash blocks.\n"
            "Each block must be a single atomic command. Use multiple blocks for multi-step tasks.\n"
            "After each command's output is returned, emit the next command or confirm completion.\n"
            "Include [cwd] context when constructing paths — always use absolute paths.\n"
            "If a command fails, diagnose from the error output and emit a corrected command.\n"
            "Only ask the user a question if truly ambiguous (e.g. missing filename, ambiguous target).\n"
            "Never output steps as prose — always as executable ```bash blocks.\n"
            "STEP-BY-STEP reasoning is internal only."
        )
        messages.append({"role": "system", "content": system_prompt})

        # Cache internet availability once at startup
        internet_available = check_internet()
        auto_search = True
        if not internet_available:
            print("No internet detected. Web search disabled, deepthink only mode active.")
            auto_search = False

        SEARCH_KEYWORDS = ["what is", "how to", "latest", "news", "who is",
                           "why", "explain", "when did", "where is", "current",
                           "update", "version", "download", "install", "error", "fix", "broken"]
        OS_ACTION_KEYWORDS = ["open", "run", "start", "kill", "delete", "list", "find",
                              "move", "copy", "rename", "create", "install", "uninstall",
                              "check", "disable", "enable", "schedule", "read", "write"]

        MAX_TURNS = 20

        while True:
            user_input = input("\nYou: ").strip()

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            if user_input.lower() == "/toggle":
                auto_search = not auto_search
                print(f"Auto-search is now {'ON' if auto_search else 'OFF'}")
                continue

            if user_input.startswith("/search "):
                # Forced manual search
                query = user_input[8:].strip()
                print(f"Searching for: {query}")
                results = web_search(query)
                if results:
                    search_context = "\n".join([f"- {r['body'][:120]} ({r['href']})" for r in results[:2]])
                    user_input = f"Search:'{query}':\n{search_context}\nAnswer concisely."
                else:
                    user_input = f"I tried to search for '{query}' but got no results. Please answer as best you can."

            elif user_input.startswith("!bash "):
                # Direct bash execution
                cmd = user_input[6:].strip()
                if confirm_action(cmd):
                    output, success = run_os_command(cmd, config.get("use_sudo", False))
                    print(f"\nBash Output:\n{output}")
                    messages.append({"role": "user", "content": f"[bash:{cmd[:40]}]\n{trim_output(output)}"})
                    response = generate_response(messages, config)
                    print(f"\nAssistant: {response}")
                    messages.append({"role": "assistant", "content": response})
                else:
                    print("Command execution cancelled.")
                continue

            else:
                # Auto-search if enabled, internet available, and query matches keywords
                if auto_search and internet_available:
                    is_os_action = any(kw in user_input.lower() for kw in OS_ACTION_KEYWORDS)
                    should_search = not is_os_action and any(kw in user_input.lower() for kw in SEARCH_KEYWORDS)
                    if should_search:
                        print("(Searching web for context...)")
                        results = web_search(user_input)
                        if results:
                            search_context = "\n".join([f"- {r['body'][:100]}" for r in results[:2]])
                            user_input = f"[Search]\n{search_context}\nQ:{user_input}"
                        else:
                            print("No search results found.")

            enriched_input = f"[cwd: {cwd_state['path']}]\n{user_input}"
            messages.append({"role": "user", "content": enriched_input})

            # Periodic system prompt reminder
            if len(messages) % 8 == 0 and len(messages) > 1:
                messages.append({"role": "user", "content": "[Sys] Be autonomous. Always use ```bash blocks. Never instruct user to run commands."})

            # Trim context before generating response
            if len(messages) > 1 + (MAX_TURNS * 2):
                dropped = messages[1:-(MAX_TURNS * 2)]
                summary_content = "[System] Context trimmed. Prior actions: " + "; ".join(
                    m["content"][:80].replace("\n", " ") for m in dropped if m["role"] == "assistant"
                )
                messages = [messages[0], {"role": "user", "content": summary_content}] + messages[-(MAX_TURNS * 2):]

            print("Assistant is thinking...")
            response = generate_response(messages, config)
            print(f"\nAssistant: {response}")
            messages.append({"role": "assistant", "content": response})

            if len(messages) > 10:
                for i in range(1, len(messages) - 6):
                    if messages[i]["role"] == "assistant" and len(messages[i]["content"]) > 60:
                        messages[i]["content"] = messages[i]["content"][:60] + "…"

            def extract_and_run_commands(response, messages, config, depth=0, max_depth=5):
                if depth >= max_depth:
                    return messages
                bash_blocks = re.findall(r'```bash\n(.*?)\n```', response, re.DOTALL | re.IGNORECASE)
                sh_blocks = re.findall(r'```sh\n(.*?)\n```', response, re.DOTALL | re.IGNORECASE)
                all_commands = [c.strip() for c in bash_blocks + sh_blocks]
                if not all_commands:
                    return messages
                for cmd in all_commands:
                    print(f"\nAssistant proposes (bash):\n{cmd}")
                    if confirm_action(cmd):
                        output, success = run_os_command(cmd, config.get("use_sudo", False), cwd=cwd_state["path"])
                        print(f"\n[bash output]\n{output}")
                        cd_match = re.match(r'^cd\s+"?(.+?)"?\s*$', cmd)
                        if cd_match and success:
                            new_path = cd_match.group(1).strip()
                            if os.path.isabs(new_path):
                                cwd_state["path"] = new_path
                            else:
                                cwd_state["path"] = os.path.normpath(os.path.join(cwd_state["path"], new_path))
                        messages.append({"role": "user", "content": f"[out:{success}]\n{trim_output(output)}"})
                        if not success:
                            messages.append({"role": "user", "content": "[System] Last command FAILED. Diagnose and emit a corrected bash command."})
                        follow_up = generate_response(messages, config)
                        print(f"\nAssistant: {follow_up}")
                        messages.append({"role": "assistant", "content": follow_up})
                        messages = extract_and_run_commands(follow_up, messages, config, depth + 1, max_depth)
                    else:
                        messages.append({"role": "user", "content": f"[System] User declined: {cmd[:60]}"})
                return messages

            messages = extract_and_run_commands(response, messages, config)

    # Start the chat
    chat_loop(config)

if __name__ == "__main__":
    main()
