import pandas as pd
from typing import List
from pathlib import Path


def map_excel_to_string_list(file_path: str) -> str:
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    try:
        # Читаем Excel файл
        impact_df = pd.read_excel(file_path)

        # Проверяем, что DataFrame не пустой
        if impact_df.empty:
            raise ValueError(f"Файл {file_path} не содержит данных")

        # Удаляем пустые строки и столбцы
        impact_df = impact_df.dropna(how='all').dropna(axis=1, how='all')

        # Проверяем, что после удаления пустых строк/столбцов остались данные
        if impact_df.empty:
            raise ValueError(f"После удаления пустых строк/столбцов файл {file_path} не содержит данных")

        # Приведение колонок к единому виду
        impact_df.columns = [col.strip().lower() for col in impact_df.columns]

        # Форматируем данные
        result: List[str] = []
        for _, row in impact_df.iterrows():
            row_items: List[str] = []
            for col_name, value in row.items():
                # Обрабатываем NaN значения
                if pd.isna(value):
                    value = "0"
                # Форматируем числовые значения
                elif isinstance(value, (int, float)):
                    value = str(value)
                row_items.append(f"{col_name.capitalize()}: {value}")
            result.append(", ".join(row_items))

        return "\n".join(result)

    except pd.errors.EmptyDataError:
        raise ValueError(f"Файл {file_path} пуст")
    except Exception as e:
        raise Exception(f"Ошибка при чтении Excel файла {file_path}: {str(e)}")
