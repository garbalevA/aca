import pandas as pd
from typing import List


def get_equipment_list(file_path: str) -> List[str]:
    try:
        df = pd.read_excel(file_path)

        if df.empty:
            raise ValueError("Excel файл не содержит данных")

        # Получаем последнюю колонку
        last_column = df.iloc[:, -1]

        # Преобразуем значения в строки и убираем пустые значения
        equipment_list = [str(value).strip() for value in last_column if pd.notna(value) and str(value).strip()]

        if not equipment_list:
            raise ValueError("Последняя колонка не содержит данных об оборудовании")

        return equipment_list

    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel файла: {str(e)}")
