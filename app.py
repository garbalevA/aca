import streamlit as st
from ai_agent import DocxAIAgent
from fault_analysis_agent import FaultAnalysisAgent
from financier_agent import FinancierAgent
from methodology_agent import MethodologyAgent
from equipment_list_processor import get_equipment_list
from equipment_description_processor import analyze_document
from get_fault_list import get_fault_list
from map_excel_to_string_list import map_excel_to_string_list
import os
import uuid
from prompts_old import analysis_results
from prompts.financier_prompt import FINANCIER_PROMPT
from prompts.mechanic_prompt import MECHANIC_PROMPT
from prompts.methodologist_prompt import METHODOLOGIST_PROMPT
from prompts.technologist_prompt import TECHNOLOGIST_PROMPT


def show_agent_analysis(agent, prompt, st_container):
    col1, col2 = st_container.columns(2)
    doc_output = col1.empty()
    stream_output = col2.empty()
    result = agent.ask_question(
        prompt, output=doc_output, stream_output=stream_output)
    print('result', result)
    # col2.write(result)
    return result


def main():

    st.set_page_config(page_title="ACA AI", page_icon=None,
                       layout="wide", initial_sidebar_state="auto", menu_items=None)

    attachments_container = st.container(border=True)
    attachments_container.markdown("### Загруженные файлы")

    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {
            "doc_analysis": None,
            "fault_analysis": None,
            "financial_analysis": None
        }

    st.title("srACA AI", )
    st.text("в каждом промпте должно быть слово 'json'")
    col1, col2 = st.columns(
        2, gap="small", vertical_alignment="top", border=False)

    # doc_file = st.file_uploader("Загрузите .docx файл", type=['docx'])
    # excel_file = st.file_uploader("Загрузите Excel файл со списком оборудования (опционально)", type=['xlsx', 'xls'])
    # fault_file = st.file_uploader("Загрузите Excel файл со списком поломок (опционально)", type=['xlsx', 'xls'])
    # margin_file = st.file_uploader("Загрузите Excel файл с маржинальностью (опционально)", type=['xlsx', 'xls'])
    # impact_file = st.file_uploader("Загрузите Excel файл с влиянием остановов на производство (опционально)", type=['xlsx', 'xls'])

    # Проверяем наличие docx файла в директории files
    doc_path = "files/example1.docx"
    if os.path.exists(doc_path):
        # if doc_file:
        # Создаем временные пути для файлов с уникальными именами
        temp_dir = "temp_files"
        os.makedirs(temp_dir, exist_ok=True)

        # doc_path = os.path.join(temp_dir, f"{uuid.uuid4()}.docx")
        # excel_path = None if not excel_file else os.path.join(temp_dir, f"{uuid.uuid4()}.xlsx")
        # fault_path = None if not fault_file else os.path.join(temp_dir, f"{uuid.uuid4()}.xlsx")
        # margin_path = None if not margin_file else os.path.join(temp_dir, f"{uuid.uuid4()}.xlsx")
        # impact_path = None if not impact_file else os.path.join(temp_dir, f"{uuid.uuid4()}.xlsx")

        try:
            # Сохраняем документ
            # with open(doc_path, "wb") as f:
            #     f.write(doc_file.getvalue())

            # Сохраняем Excel если есть
            # if excel_file:
            #     with open(excel_path, "wb") as f:
            #         f.write(excel_file.getvalue())

            # Сохраняем файл с поломками если есть
            # if fault_file:
            #     with open(fault_path, "wb") as f:
            #         f.write(fault_file.getvalue())

            # Сохраняем файл с маржинальностью если есть
            # if margin_file:
            #     with open(margin_path, "wb") as f:
            #         f.write(margin_file.getvalue())

            # Сохраняем файл с влиянием остановов если есть
            # if impact_file:
            #     with open(impact_path, "wb") as f:
            #         f.write(impact_file.getvalue())

            # Инициализируем агентов
            doc_agent = DocxAIAgent()
            fault_agent = FaultAnalysisAgent()
            financier_agent = FinancierAgent()
            methodology_agent = MethodologyAgent()

            # Обрабатываем документ
            doc_text = analyze_document(doc_path)
            doc_agent.set_doc_summary(doc_text)

            # Создаем контейнер для хранения результатов анализа

            

            # Отображаем содержимое документа
            attachments_container.markdown(
                "Описание технологического процесса docx")
            # st.text(doc_text)

            # Обрабатываем Excel если есть
            equipment_file_path = "files/Список_оборудования.xlsx"
            if os.path.exists(equipment_file_path):
                equipment_list = get_equipment_list(equipment_file_path)
                doc_agent.set_equipment_list(equipment_list)
                fault_agent.set_equipment_list(equipment_list)

                attachments_container.markdown("Список оборудования xlsx")
                # st.write(", ".join(equipment_list))

            # Обрабатываем файл с поломками если есть
            fault_file_path = "files/История_отказов.xlsx"
            if os.path.exists(fault_file_path):
                fault_data = get_fault_list(fault_file_path)
                fault_agent.set_fault_list(fault_data)
                attachments_container.markdown("История отказов xlsx")
                # st.text(fault_data)

            # Отображаем данные о маржинальности из текущей директории
            margin_file_path = "files/Маржинальность_продуктов_блока_риформинга.xlsx"

            if os.path.exists(margin_file_path):
                margin_data = map_excel_to_string_list(margin_file_path)
                financier_agent.set_margin_data(margin_data)
                attachments_container.markdown("Маржинальность xlsx")
                # margin_columns[1].badge("Success", icon=":material/check:", color="green")
                # st.text(margin_data)
            else:

                st.error(
                    f"Файл {margin_file_path} не найден в текущей директории")

            # Отображаем данные о влиянии остановов из текущей директории
            impact_file_path = "files/Влияние_оставов_на_производство_продуктов.xlsx"
            if os.path.exists(impact_file_path):
                impact_data = map_excel_to_string_list(impact_file_path)
                financier_agent.set_impact_data(impact_data)
                attachments_container.markdown("Влияние остановов xlsx")
                # st.text(impact_data)
            else:
                st.error(
                    f"Файл {impact_file_path} не найден в текущей директории")

            # Секция для анализа методологии

            # Отображаем данные методологии из директории files
            methodology_file_path = "files/metodologiya.docx"
            if os.path.exists(methodology_file_path):
                methodology_content = analyze_document(methodology_file_path)
                methodology_agent.set_methodology_content(methodology_content)
                attachments_container.markdown("Методология docx")
                # st.text(methodology_content)

                # Добавляем textarea для ввода промпта
                technologist_user_prompt = col1.text_area(
                    "**Промпт для агента-технолога**", value=TECHNOLOGIST_PROMPT, height=200)

                # Кнопка и ответ для агента-технолога
                if col1.button("Задать вопрос технологу"):
                    doc_result = show_agent_analysis(
                        doc_agent, technologist_user_prompt, st)
                    st.session_state.analysis_results["doc_analysis"] = doc_result

                mechanic_user_prompt = col1.text_area(
                    "**Промпт для агента-механика**", value=MECHANIC_PROMPT, height=200)

                if col1.button("Задать вопрос механику"):
                    mechanic_result = show_agent_analysis(
                        fault_agent, mechanic_user_prompt, st)
                    st.session_state.analysis_results["fault_analysis"] = mechanic_result

                financier_user_prompt = col2.text_area(
                    "**Промпт для агента-финансиста**", value=FINANCIER_PROMPT, height=200)

                if col2.button("Задать вопрос финансисту"):
                    financier_result = show_agent_analysis(
                        financier_agent, financier_user_prompt, st)
                    st.session_state.analysis_results["financial_analysis"] = financier_result

                methodologist_user_prompt = col2.text_area(
                    "**Промпт для агента-методолога**", value=METHODOLOGIST_PROMPT, height=200)

                if col2.button("Задать вопрос методологу", disabled=not all(st.session_state.analysis_results.values())):
                    methodology_output = st.empty()
                    methodology_output2 = st.empty()
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!methodology_output', st.session_state.analysis_results)
                    methodology_result = methodology_agent.analyze_methodology(
                        methodologist_user_prompt, analysis_results=st.session_state.analysis_results, output=methodology_output, stream_output=methodology_output2)
                    # st.markdown("#### � Ответ методолога:")
                    # st.write(methodology_result)

                print(st.session_state.analysis_results["doc_analysis"])
                if st.session_state.analysis_results["doc_analysis"] is not None:
                    col1.badge("Агент-технолог",
                               icon=":material/check:", color="green")

                if st.session_state.analysis_results["fault_analysis"] is not None:
                    col1.badge("Агент-механик",
                               icon=":material/check:", color="green")

                if st.session_state.analysis_results["financial_analysis"] is not None:
                    col1.badge("Агент-финансист",
                               icon=":material/check:", color="green")

                # Кнопка для полного анализа
                if st.button("Провести полный анализ (последовательно 4 агента)"):
                    st.markdown("### 🚀 Начинаем анализ...")

                    # Запускаем анализ документации
                    st.markdown(f"#### 📄 Анализ технолога:")
                    doc_result = show_agent_analysis(
                        doc_agent, technologist_user_prompt, st)
                    st.session_state.analysis_results["doc_analysis"] = doc_result

                    # # Запускаем анализ отказов
                    st.markdown("#### ⚠️ Анализ механика:")
                    fault_result = show_agent_analysis(
                        fault_agent, mechanic_user_prompt, st)
                    st.session_state.analysis_results["fault_analysis"] = fault_result

                    # # Запускаем финансовый анализ
                    st.markdown("#### 💰 Анализ финансиста:")
                    financial_result = show_agent_analysis(
                        financier_agent, financier_user_prompt, st)
                    st.session_state.analysis_results["financial_analysis"] = financial_result

                    # # Запускаем анализ методологии с учетом всех результатов
                    st.markdown("#### 📊 Результаты анализа методологии:")

                    methodology_output = st.empty()
                    methodology_output2 = st.empty()
                    # analysis_context = ""
                    # if analysis_results["doc_analysis"]:
                    #     analysis_context += f"Вот информация о технологическом процессе и критичности оборудования:\n{analysis_results['doc_analysis']}\n\n"
                    # if analysis_results["fault_analysis"]:
                    #     analysis_context += f"Вот данные о частоте отказов и продолжительности простоев оборудования:\n{analysis_results['fault_analysis']}\n\n"
                    # if analysis_results["financial_analysis"]:
                    #     analysis_context += f"Вот данные о финансовых потерях от остановок:\n{analysis_results['financial_analysis']}\n\n"

                    # # st.markdown("### 📋 Контекст для анализа методологии:")
                    # # st.markdown(analysis_context)

                    result = methodology_agent.analyze_methodology(
                        methodologist_user_prompt, st.session_state.analysis_results, output=methodology_output, stream_output=methodology_output2)
                    # st.write(result)
                    # st.write(result)
            else:
                st.error(
                    f"Файл {methodology_file_path} не найден в директории files")

        finally:
            # Удаляем временные файлы только в конце
            # if os.path.exists(doc_path):
            #     os.remove(doc_path)
            # if excel_path and os.path.exists(excel_path):
            #     os.remove(excel_path)
            # if fault_path and os.path.exists(fault_path):
            #     os.remove(fault_path)
            # if margin_path and os.path.exists(margin_path):
            #     os.remove(margin_path)
            # if impact_path and os.path.exists(impact_path):
            #     os.remove(impact_path)
            # Удаляем временную директорию, если она пуста
            if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                os.rmdir(temp_dir)

    else:
        st.info("Пожалуйста, загрузите документ (.docx)")
        # st.error(f"Файл {doc_path} не найден в директории files")


if __name__ == "__main__":
    main()
