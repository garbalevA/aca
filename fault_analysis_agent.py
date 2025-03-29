from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts_old import (
    create_fault_context,
    create_fault_prompt,
    ERROR_MESSAGES
)
import json
# Load environment variables
load_dotenv()


class FaultAnalysisAgent:
    def __init__(self, api_key: Optional[str] = None, temperature: float = 0.3):
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError(
                "DeepSeek API key is required. Set it in .env file or pass to constructor.")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        self.temperature = temperature
        self.fault_list: Optional[str] = None
        self.equipment_list: Optional[List[str]] = None

    def set_fault_list(self, fault_list: str) -> None:
        self.fault_list = fault_list

    def set_equipment_list(self, equipment_list: List[str]) -> None:
        self.equipment_list = equipment_list

    def ask_question(self, question: str, output: Optional[Any] = None, stream_output: Optional[Any] = None) -> str:
        if not self.fault_list:
            raise ValueError(
                "Список отказов не загружен. Используйте set_fault_list() для загрузки данных.")

        context = create_fault_context(self.fault_list, self.equipment_list)
        prompt = create_fault_prompt(context, question)

        newPrompt = f"""
            ИСХОДНЫЕ ДАННЫЕ (обязательно учти):
            1. Список оборудования:
            {self.equipment_list}
            2. История отказов:
            {self.fault_list}

            {question}
       """
#  "failure_rate": {{"оборудование1": число}},
#             "mttr_hours": {{"оборудование1": число}},
#             "most_problematic": [{{"name":"оборудование1", "reason":"текст-объяснение"}}],

        expander = output.expander(
            "Промпт механика", expanded=False)
        expander.text(newPrompt)

        try:
            if stream_output:
                full_response = ""
                
                stream = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": newPrompt}],
                    temperature=self.temperature,
                    response_format={"type": "json_object"},
                    stream=True
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
                        

                # return 'fault hahaha'
            else:
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": newPrompt}],
                    temperature=self.temperature,
                    response_format={"type": "json_object"}
                ).choices[0].message.content
            return response
        except Exception as e:
            error_msg = f"Ошибка при анализе отказов: {str(e)}"
            if output:
                output.error(error_msg)
            raise
