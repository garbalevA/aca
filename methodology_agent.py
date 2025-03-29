from typing import Optional, Any
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts_old import ERROR_MESSAGES
import json

# Load environment variables
load_dotenv()


class MethodologyAgent:
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
        self.methodology_content: Optional[str] = None

    def set_methodology_content(self, content: str) -> None:
        """Устанавливает содержимое методологии."""
        self.methodology_content = content

    def analyze_methodology(self, question: str, analysis_results: dict, output: Optional[Any] = None, stream_output: Optional[Any] = None) -> str:
        print("Starting analyze_methodology...")
        print(f"Output object type: {type(output)}")

        if not self.methodology_content:
            print("Error: methodology_content is None")
            raise ValueError(
                "Методология не загружена. Используйте set_methodology_content() для загрузки данных.")

        # Формируем контекст из методологии
        context = f"Вот методология оценки критичности оборудования::\n{self.methodology_content}\n"
        print("Context formed successfully")

        # Формируем промпт
        # prompt = f"""
        # {outerDocs}

        # {context}

        # Используя методологию, рассчитай уровень критичности оборудования на основе предоставленных выше данных.

        # Выведи результат в следующем формате:
        # - Оборудование: {{название оборудования}}
        # - Итоговый уровень критичности: {{Высокая/Средняя/Низкая}}
        # - Основание для критичности: {{ключевые факторы}}

        # Пример вывода:
        # - Оборудование: Насос-1
        # - Итоговый уровень критичности: Высокая
        # - Основание для критичности: Частые отказы (1 раз в 6 месяцев), отсутствие резерва, высокие потери при остановке (100 000 руб./час).

        # - Оборудование: Компрессор-3
        # - Итоговый уровень критичности: Средняя
        # - Основание для критичности: Имеется резерв, но длительные простои (10 часов), умеренные финансовые потери.
        # """

        newPrompt = f"""
            ИСХОДНЫЕ ДАННЫЕ (обязательно учти):
                1. Технолог: {json.dumps(analysis_results['doc_analysis'], ensure_ascii=False)}
                2. Механик: {json.dumps(analysis_results['fault_analysis'], ensure_ascii=False)}
                3. Финансист: {json.dumps(analysis_results['financial_analysis'], ensure_ascii=False)}
                4. Методика: {self.methodology_content}

            {question}
        """

        expander = output.expander(
                "Промпт методолога", expanded=False)
        expander.text(newPrompt)

        print('newPrompt', newPrompt)

        try:
            print("Starting LLM processing...")
            if stream_output:
                # container = output.container()
                full_response = ""
                print("Using streaming output...")
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
                # return "test metodolog"
            else:
                print("Using direct output...")
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": newPrompt}],
                    temperature=self.temperature,
                    response_format={"type": "json_object"}
                )
                print("LLM processing completed")
                print(f"Final response length: {len(response)}")
                return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            error_msg = f"Ошибка при анализе методологии: {str(e)}"
            if output:
                print("Writing error to output...")
                output.error(error_msg)
            raise
