import threading
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from transcribe.stt import run_stt, NEW_TEXT_EVENT
from transcribe.tts import run_tts
from mistral_ai.llm import run_mistral_llm
from execute.actions import ActionExecutor, parse_actions
TRANS_FILE = "src/transcribe/transcription.txt"
VLM_FILE = "src/mistral_ai/scripts/vlm_script.txt"
VLM_JSON_FILE = "src/mistral_ai/scripts/vlm_script.json"
LLM_FILE = "src/mistral_ai/scripts/llm_script.txt"
LLM_JSON_FILE = "src/mistral_ai/scripts/llm_script.json"
import json

def stt_thread():
    # Running in background, press ESC to exit
    run_stt()

if __name__ == "__main__":
    # Clear transcription.txt content
    with open(TRANS_FILE, "w", encoding="utf-8") as f:
        f.write("")
    with open(VLM_FILE, "w", encoding="utf-8") as f:
        f.write("")
    with open(VLM_JSON_FILE , "w", encoding="utf-8") as f:
        f.write("")
    with open(LLM_FILE, "w", encoding="utf-8") as f:
        f.write("")
    with open(LLM_JSON_FILE, "w", encoding="utf-8") as f:
        f.write("")

    # 1. Start STT thread
    threading.Thread(target=stt_thread, daemon=True).start()

    last_text = ""
    print("🟢 STT thread started. Waiting for new speech...")

    while True:
        # 2. Wait for new recording to complete
        NEW_TEXT_EVENT.wait()
        NEW_TEXT_EVENT.clear()
        # 3. Read latest text
        try:
            with open(TRANS_FILE, "r", encoding="utf-8") as f:
                text = f.read().strip()
        except FileNotFoundError:
            continue
        # 4. If text hasn't changed, ignore
        if text == last_text:
            continue
        last_text = text
        run_mistral_llm()
        run_tts(LLM_FILE)

        # 5. Read JSON action list and execute
        try:
            with open(LLM_JSON_FILE, "r", encoding="utf-8") as f:
                llm_data = json.load(f)
                action_dicts = llm_data.get("actions", [])
                actions = parse_actions(action_dicts)
                if actions:
                    print(f"🦾 Executing {len(actions)} actions...")
                    with ActionExecutor() as action_exec:
                        action_exec.execute_sequence(actions)
                else:
                    print("ℹ️ No actions to execute.")
        except Exception as e:
            print(f"❌ Failed to load or execute actions: {e}")
