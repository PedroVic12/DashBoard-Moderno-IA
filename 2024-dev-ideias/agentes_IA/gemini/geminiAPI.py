import json
import os
from litellm import completion


class GeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        os.environ["GEMINI_API_KEY"] = self.api_key

    def get_completion(self, user_message):
        messages = [{"role": "user", "content": user_message}]

        response = completion(
            model="gemini/gemini-1.5-pro",
            messages=messages,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    # Uso da classe


api_key = "AIzaSyDAPQnsTQxOL5HJ0zpjdYZKxbQ - ekmi3S0"


gemini_api = GeminiAPI(api_key)

result = gemini_api.get_completion("List 5 popular cookie recipes.")
print(result)
