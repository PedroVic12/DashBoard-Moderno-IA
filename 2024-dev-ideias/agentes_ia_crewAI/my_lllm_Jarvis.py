from crewai import LLM


class MyLLLMJarvis(LLM):
    # ollama run llama2
    ollama = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")
    gemini = LLM(model="gemini1.5-pro", api_key="your-api-key")

    gemini_request = LLM(
        model="custom-model-name",
        base_url="https://api.your-provider.com/v1",
        api_key="your-api-key",
    )

from litellm import completion
import json
import os

os.environ["GEMINI_API_KEY"] = ""

messages = [{"role": "user", "content": "List 5 popular cookie recipes."}]

response_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "recipe_name": {
                "type": "string",
            },
        },
        "required": ["recipe_name"],
    },
}


completion(
    model="gemini/gemini-1.5-pro",
    messages=messages,
    response_format={
        "type": "json_object",
        "response_schema": response_schema,
    },  # 👈 KEY CHANGE
)

print(json.loads(completion.choices[0].message.content))
