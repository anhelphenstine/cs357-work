import requests
import json
import traceback

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

def call_model(messages, config):
    """Send message history to the model provider and return the assistant reply string."""
    url = config["provider_url"]
    headers = {}
    if config.get("api_key"):
        # Hosted providers need a key; local Ollama does not, so api_key is null there.
        headers["Authorization"] = f"Bearer {config['api_key']}"

    if url.rstrip("/").endswith("/chat/completions"):
        # OpenAI-style providers: sampling settings sit at the top level.
        payload = {
            "model": config["model"],
            "messages": messages,
            "stream": False,
            "temperature": config["temperature"],
            "seed": config["seed"]
        }
    else:
        # Ollama (local or hosted): sampling settings sit under "options".
        payload = {
            "model": config["model"],
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": config["temperature"],
                "seed": config["seed"]
            }
        }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]   # OpenAI-style reply
        return data["message"]["content"]                     # Ollama reply
    except Exception as e:
        print(f"[lab1:call_model] {e}")
        traceback.print_exc()
        raise

import re

def parse_response(text):
    """
    Returns ("action", tool_name, argument) or ("final", None, answer_text).
    Returns ("unknown", None, text) if neither pattern is found.
    """
    final_match = re.search(r"Final Answer:\s*(.+)", text, re.IGNORECASE | re.DOTALL)
    if final_match:
        return ("final", None, final_match.group(1).strip())

    action_match = re.search(r"Action:\s*(\w+)\(([^)]*)\)", text, re.IGNORECASE)
    if action_match:
        return ("action", action_match.group(1).strip(), action_match.group(2).strip())

    return ("unknown", None, text)


def build_system_prompt(goal, tools):
    return "You are a helpful AI assistant. Always respond using the format 'Final Answer: your answer here'."


def run_agent(goal, config, tools):
    """Run the perceive -> plan -> act loop until a final answer or the step budget runs out."""
    messages = [
        {"role": "system", "content": build_system_prompt(goal, tools)},
        {"role": "user", "content": goal},
    ]
    step_budget = config["step_budget"]

    for step in range(1, step_budget + 1):
        print(f"\n[step {step}] planning...")
        reply = call_model(messages, config)
        messages.append({"role": "assistant", "content": reply})
        print(f"[step {step}] model: {reply}")

        kind, name, payload = parse_response(reply)

        if kind == "final":
            print(f"[step {step}] final answer: {payload}")
            return payload, step, "final answer"

        if kind == "action":
            print(f"[step {step}] action: {name}({payload})")
            try:
                tool = tools.get(name) if isinstance(tools, dict) else None
                if tool is None:
                    observation = f"Unknown tool: {name}"
                elif payload:
                    observation = tool(payload)
                else:
                    observation = tool()
            except Exception as e:
                observation = f"Tool {name} failed: {e}"
                traceback.print_exc()

            observation = str(observation)
            print(f"[step {step}] observation: {observation}")
            messages.append({"role": "user", "content": f"Observation: {observation}"})
            continue

        print(f"[step {step}] could not parse an action or final answer")
        messages.append({"role": "user", "content": "Observation: reply with an Action: tool(arg) or Final Answer: text"})

    print(f"\n[budget reached after {step_budget} steps]")
    return None

if __name__ == "__main__":
    config = load_config()
    tools = {}  # empty for now
    answer, steps, reason = run_agent("What is the capital of France?", config, tools)
    print(f"\nResult: {answer}")
    print(f"Steps used: {steps} | Reason: {reason}")


