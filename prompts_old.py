"""Промпты и текстовые константы для AI агента."""

from typing import List, Optional

# Роли и контекст
SYSTEM_ROLE = """
Проанализируй технологический регламент и список оборудования.
1. Определи, какое оборудование критично для производственного процесса.
2. Укажи, какие единицы оборудования имеют резервные аналоги.
3. Выяви возможные последствия остановки оборудования (нарушение процесса, риски безопасности, экологические последствия).

Выведи ответ в следующем формате:
- Оборудование: {{название оборудования}}
- Критично для процесса: {{Да/Нет}}
- Есть резерв: {{Да/Нет}}
- Возможные последствия остановки: {{краткое описание}}

Пример вывода:
- Оборудование: Насос-1
- Критично для процесса: Да
- Есть резерв: Нет
- Возможные последствия остановки: Остановка насосов приведёт к прекращению подачи сырья.
"""
# Опиши основные характеристики и роль каждого оборудования в технологическом процессе. Выдели критически важные элементы и их взаимосвязи.

FAULT_SYSTEM_ROLE = """
Проанализируй историю отказов оборудования.
1. Для каждого оборудования определи частоту отказов.
2. Вычисли среднюю продолжительность простоя.
3. Оцени стоимость восстановления.

Выведи ответ в следующем формате:
- Оборудование: {{название оборудования}}
- Частота отказов: {{раз в X месяцев/лет}}
- Средняя продолжительность простоя: {{количество часов}}
- Средняя стоимость восстановления: {{сумма}}

Пример вывода:
- Оборудование: Насос-1
- Частота отказов: 1 раз в 6 месяцев
- Средняя продолжительность простоя: 5 часов
- Средняя стоимость восстановления: 50 000 руб.
"""
# Проанализируй историю отказов оборудования. Выдели основные причины отказов, их частоту и влияние на производство.

# Инструкции для ответов
# ANSWER_INSTRUCTIONS = """Ответ должен быть строго в следующем формате:
#     - Этап: {название или описание этапа}
#     - Оборудование: {название или описание оборудования}
#     - Потенциальные риски: {описание рисков}
#     - Рекомендации: {предложения по улучшению процесса}"""

# FAULT_ANALYSIS_INSTRUCTIONS = """Инструкции по анализу отказов:
# 1. Предоставьте структурированный анализ с четкими разделами
# 2. Используйте статистические данные, если они доступны
# 3. Выделите основные проблемы и их причины
# 4. Предложите конкретные рекомендации по улучшению
# 5. Оцените критичность проблем и их влияние на производство
# 6. Придерживайтесь профессионального инженерно-технического стиля"""

# Шаблоны промптов
DOCUMENT_CONTEXT_TEMPLATE = """Технологический регламент:
{text}"""

EQUIPMENT_CONTEXT_TEMPLATE = """
Список оборудования на производстве: {equipment_list}"""

FAULT_CONTEXT_TEMPLATE = """
История отказов оборудования:
{fault_list}

Список оборудования на производстве:
{equipment_list}"""

QUESTION_PROMPT_TEMPLATE = """
{context}
{system_role}
"""

FAULT_ANALYSIS_PROMPT_TEMPLATE = """
{context}
{system_role}
"""

# Сообщения об ошибках
ERROR_MESSAGES = {
    'file_not_found': "Файл не найден: {path}",
    'invalid_format': "Файл должен быть в формате .docx: {path}",
    'doc_read_error': "Ошибка при чтении документа: {error}",
    'general_error': "Ошибка: {error}",
    'doc_not_loaded': "Документ не загружен"
}


def create_context(doc_text: str, equipment_list: Optional[List[str]] = None) -> str:
    context = DOCUMENT_CONTEXT_TEMPLATE.format(text=doc_text)
    if equipment_list:
        context += EQUIPMENT_CONTEXT_TEMPLATE.format(
            equipment_list=", ".join(equipment_list))
    return context


def create_fault_context(fault_list: str, equipment_list: Optional[List[str]] = None) -> str:
    equipment_str = ", ".join(
        equipment_list) if equipment_list else "не указано"
    return FAULT_CONTEXT_TEMPLATE.format(
        fault_list=fault_list,
        equipment_list=equipment_str
    )


def create_prompt(context: str, query: str) -> str:
    return QUESTION_PROMPT_TEMPLATE.format(
        system_role=SYSTEM_ROLE,
        context=context,
    )


def create_fault_prompt(context: str, question: str) -> str:
    return FAULT_ANALYSIS_PROMPT_TEMPLATE.format(
        system_role=FAULT_SYSTEM_ROLE,
        context=context
    )


analysis_results = {
                "doc_analysis": None,
                "fault_analysis": None,
                "financial_analysis": None
            }