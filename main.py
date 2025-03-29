import argparse
from ai_agent import DocxAIAgent

# not used now


def main():
    parser = argparse.ArgumentParser(description='Анализ технической документации с помощью AI')
    parser.add_argument('--file', type=str, required=True, help='Путь к файлу .docx')
    parser.add_argument('--query', type=str, required=True, help='Вопрос о содержании документа')
    parser.add_argument('--model', type=str, default="mistral:7b", help='Модель AI для анализа')
    parser.add_argument('--temperature', type=float, default=0.7, help='Температура для модели (0.0-1.0)')

    args = parser.parse_args()

    # Инициализация AI агента
    agent = DocxAIAgent(model_name=args.model, temperature=args.temperature)

    # Получение ответа на вопрос
    print(f"\nВопрос: {args.query}")
    print("\nОтвет:")
    agent.ask_question(args.file, args.query)


if __name__ == "__main__":
    main()
