import pandas as pd


def get_fault_list(file_path: str) -> str:
    try:
        df = pd.read_excel(file_path)

        # Создаем заголовки
        text_data = "Данные об отказах оборудования:\n"
        text_data += " | ".join(df.columns) + "\n"
        text_data += "-" * 50 + "\n"

        # Добавляем строки данных
        for _, row in df.iterrows():
            text_data += " | ".join(str(value) for value in row) + "\n"

        return text_data
    except Exception as e:
        raise Exception(f"Ошибка при чтении Excel файла: {str(e)}")
