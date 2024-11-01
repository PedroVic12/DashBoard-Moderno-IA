import json
import os
from litellm import completion
from crewai import LLM


class MyLLLMJarvis:
    def __init__(self, api_key):
        self.gemini = LLM(model="gemini1.5-pro", api_key=api_key)

    def get_response(self, messages, response_schema):
        response = completion(
            model="gemini/gemini-1.5-pro",
            messages=messages,
            response_format={
                "type": "json_object",
                "response_schema": response_schema,
            },
        )
        return json.loads(response.choices[0].message.content)


class Marketeer:
    def __init__(self, llm_jarvis):
        self.llm_jarvis = llm_jarvis

    def create_marketing_strategy(self, product_name):
        messages = [
            {
                "role": "user",
                "content": f"Create a marketing strategy for {product_name}.",
            }
        ]
        response_schema = {
            "type": "object",
            "properties": {
                "strategy": {"type": "string"},
            },
            "required": ["strategy"],
        }
        response = self.llm_jarvis.get_response(messages, response_schema)
        return response["strategy"]


class Cook:
    def __init__(self, llm_jarvis):
        self.llm_jarvis = llm_jarvis

    def get_cookie_recipes(self):
        messages = [{"role": "user", "content": "List 5 popular cookie recipes."}]
        response_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                },
                "required": ["recipe_name"],
            },
        }
        response = self.llm_jarvis.get_response(messages, response_schema)
        return [recipe["recipe_name"] for recipe in response]


# Configuração do ambiente

# Execução do chatbot
if __name__ == "__main__":
    api_key = "AIzaSyDAPQnsTQxOL5HJ0zpjdYZKxbQ - ekmi3S0"
    llm_jarvis = MyLLLMJarvis(api_key)

    # Instanciando os módulos
    marketeer = Marketeer(llm_jarvis)
    cook = Cook(llm_jarvis)

    # Exemplo de uso
    print("Estratégia de Marketing:")
    strategy = marketeer.create_marketing_strategy("Cookies Gourmet")
    print(strategy)

    print("\nReceitas de Cookies:")
    recipes = cook.get_cookie_recipes()
    for recipe in recipes:
        print(recipe)
