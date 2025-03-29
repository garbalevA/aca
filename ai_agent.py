from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts_old import (
    create_context,
    create_prompt,
    ERROR_MESSAGES
)
import json

# Load environment variables
load_dotenv()

class DocxAIAgent:
    def __init__(self, api_key: Optional[str] = None, temperature: float = 0.3):
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DeepSeek API key is required. Set it in .env file or pass to constructor.")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        self.temperature = temperature
        self.equipment_list: Optional[List[str]] = None
        self.doc_text: Optional[str] = None

    def set_equipment_list(self, equipment_list: List[str]) -> None:
        self.equipment_list = equipment_list

    def set_doc_summary(self, doc_text: str) -> None:
        self.doc_text = doc_text

    def ask_question(self, query: str, output: Optional[Any] = None, stream_output: Optional[Any] = None) -> str:
        try:
            if not self.doc_text:
                raise ValueError(ERROR_MESSAGES['doc_not_loaded'])

            context = create_context(self.doc_text, self.equipment_list)
            prompt = create_prompt(context, query)

        

            newPrompt = f"""
                ИСХОДНЫЕ ДАННЫЕ (обязательно учти):
                1. Список оборудования:
                {self.equipment_list}
                2. Технологический регламент:
                {self.doc_text}

               {query}
            """


            expander = output.expander("Промпт технолога", expanded=False)
            expander.text(newPrompt)
            

            if stream_output:
                full_response = ""
                # Stream the response
                stream = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": newPrompt}],
                    temperature=self.temperature,
                    response_format={"type": "json_object"},
                    stream=True,
                )

                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        
                        try:
                            # Пробуем парсить накопленный JSON
                            parsed = json.loads(full_response)
                            stream_output.json(parsed)  # Обновляем отображение
                        except json.JSONDecodeError:
                            # Если JSON еще не полный, выводим как текст
                            stream_output.code(full_response)

                # print('response', response)
                final_result = json.loads(full_response)
                print('Final response:', final_result)
                return final_result
                # return json.loads(response.choices[0].message.content)
                # return "testеееееее"

                # for chunk in stream:
                #     if chunk.choices[0].delta.content:
                #         response += chunk.choices[0].delta.content
                #         output.write(response)
            else:
                # Regular response
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature
                ).choices[0].message.content

            return response
        except Exception as e:
            error_msg = ERROR_MESSAGES['general_error'].format(error=str(e))
            if output:
                output.error(error_msg)
            else:
                print(error_msg)
            raise
