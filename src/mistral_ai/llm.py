from src.mistral_ai.mistral import Mistralmodel
from mistral_ai.prompts.plan_prompt import system_prompt, example, assistant_prompt
from src.utils import get_last_text_line ,get_full_text, safe_extract_json_and_response_for_llm
import json
from pathlib import Path
from typing import Union, Any
import re


def run_mistral_llm():
    client = Mistralmodel()
    transcribed_text = get_full_text("./src/transcribe/transcription.txt")

    subtasks = client.chat_with_text(
        transcribed_text,
        system_prompt=system_prompt,
        example=example,
        assistant_prompt=assistant_prompt
    )

    # safely extract JSON and response
    response, json_blocks = safe_extract_json_and_response_for_llm(str(subtasks))

    # Save response text
    Path("./src/mistral_ai/scripts/llm_script.txt").write_text(response, encoding="utf-8")

    print("🤖 LLM Response:")
    print(">>> Subtask list:\n", response)
    print(">>> JSON:\n", json.dumps(json_blocks[0], indent=2, ensure_ascii=False) if json_blocks else "None")

    # Save JSON action structure
    if json_blocks:
        with open("./src/mistral_ai/scripts/llm_script.json", "w", encoding="utf-8") as jf:
            json.dump(json_blocks[0], jf, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    run_mistral_llm()