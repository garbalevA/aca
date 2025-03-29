from typing import Optional, Any
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts_old import ERROR_MESSAGES
import json

# Load environment variables
load_dotenv()


class FinancierAgent:
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
        self.margin_data: Optional[str] = None
        self.impact_data: Optional[str] = None

    def set_margin_data(self, margin_data: str) -> None:
        """Устанавливает данные о маржинальности."""
        self.margin_data = margin_data

    def set_impact_data(self, impact_data: str) -> None:
        """Устанавливает данные о влиянии остановов на производство."""
        self.impact_data = impact_data

    def ask_question(self, question: str, output: Optional[Any] = None, stream_output: Optional[Any] = None) -> str:
        if not self.margin_data and not self.impact_data:
            raise ValueError(
                "Финансовые данные не загружены. Используйте set_margin_data() и set_impact_data() для загрузки данных.")

        # Формируем контекст из доступных данных
        context = ""

        if self.impact_data:
            context += f"Вот данные о влиянии остановов на производство (оборудование и их связь с продуктами):\n{self.impact_data}\n"
        if self.margin_data:
            context += f"Вот данные о маржинальности продуктов:\n{self.margin_data}\n\n"

        print("Financier Context: ", context)

        # Формируем промпт
        # prompt = f"""
        #     Проанализируй влияние остановов оборудования на производство и финансовые потери.

        #     Строго придерживайся предоставленных данных. Не добавляй никакой информации, которой нет в списке. Если данные для какого-то оборудования отсутствуют, напиши "Нет данных".

        #     Выведи ответ в точном формате (без отклонений):
        #     - Оборудование: {{название оборудования}}
        #     - Влияет на продукт: {{название продукта}}
        #     - Процент влияния: {{X%}}
        #     - Потери при остановке: {{руб./час}}

        #     🔹 **Пример правильного вывода:**
        #     - Оборудование: Насос-1
        #     - Влияет на продукт: Бензин АИ-92
        #     - Процент влияния: 30%
        #     - Потери при остановке: 100 000 руб./час

        #     - Оборудование: Компрессор-2
        #     - Влияет на продукт: Водород
        #     - Процент влияния: 50%
        #     - Потери при остановке: 150 000 руб./час

        #     Если данных для расчета нет, выведи:
        #     "Нет данных для оборудования {{название оборудования}}
        # """

        newPrompt = f"""
            ИСХОДНЫЕ ДАННЫЕ (обязательно учти):
            1. Влияние остановов:
            {self.impact_data}
            2. Маржинальность продуктов:
            {self.margin_data}

            {question}
        """

    #   Задачи:
    #         1. Рассчитай потери в рублях/час
    #         2. Учитывай наличие резервов
    #         3. Выдели критичное оборудование

    #         Формат ответа (строго JSON):
    #         {{
    #         "hourly_loss_rub": {{"оборудование1": число}},
    #         "most_critical": ["оборудование1"]
    #         }}

        expander = output.expander(
            "Промпт финансиста", expanded=False)
        expander.text(newPrompt)

        
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
        # return 'bybyby'

    # Проанализируй финансовые показатели производства. Определи критически важное оборудование с точки зрения финансовых потерь. Оцени влияние отказов на экономические показатели.
