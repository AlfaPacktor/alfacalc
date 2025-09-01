import streamlit as st
import streamlit.components.v1 as components

# ИСПРАВЛЕННАЯ Страница Входа
def login_page():
    st.header("Добро пожаловать!")
    # Поле для ввода имени (логина). Оно теперь единственное.
    username = st.text_input("Введите ваше имя (Например, Иван Петров)")

    # Добавляем кнопку "Войти"
    if st.button("Войти"):
        # Новая проверка: просто смотрим, ввел ли пользователь имя.
        if username: # Если поле username не пустое
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            # st.rerun() перезагрузит страницу и покажет калькулятор.
            # Ваша функция get_user_state() сама создаст "личный блокнот", если нужно.
            st.rerun()
        else:
            # Если пользователь ничего не ввел, вежливо просим его это сделать.
            st.warning("Пожалуйста, введите имя, чтобы продолжить.")

# --- Данные о продуктах ---
PRODUCTS_DK = [
    "ДК", "Акт", "Трз", "Комбо/Кросс КК Одобрено", "Комбо/Кросс КК Выдано", "Трз.", "ЦП", "Гос.Уведомления", "Смарт", "Кешбек", "ЖКУ", "БС",
    "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет",
    "Вклад", "Детская Кросс", "Сим-Карта", "Перевод Пенсии",
    "Селфи ДК", "Селфи КК"
]

PRODUCTS_KK = [
    "КК", "Акт", "Трз", "Кросс ДК", "ЦП", "Гос.Уведомления", "Смарт", "Кешбек", "ЖКУ", "БС",
    "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет",
    "Вклад", "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Перевод Пенсии",
    "Селфи ДК"
]

PRODUCTS_MP = [
    "МП", "ЦП", "Гос.Уведомления", "Смарт", "Кешбек", "ЖКУ", "БС", "Инвесткопилка",
    "БС со Стратегией", "Токенизация", "Накопительный Счет", "Вклад",
    "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Перевод Пенсии", "Кросс ДК",
    "Селфи ДК", "Селфи КК"
]

PRODUCT_LISTS = {
    "ДК": PRODUCTS_DK,
    "КК": PRODUCTS_KK,
    "МП": PRODUCTS_MP
}

# --- Стили ---
def apply_styles():
    st.markdown("""
        <style>
            .main { background-color: #FFFFFF; }
            
            .main-menu-container {
                margin-left: auto;
                margin-right: auto;
                margin-top: 20px;
                max-width: 500px; 
            }
            
            @media (max-width: 600px) {
                .main-menu-container {
                    width: 95%; 
                }
            }

            div.stButton > button {
                height: 50px;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                background-color: #FFFFFF;
                color: #000000;
                font-family: 'Calibri', sans-serif;
                font-size: 16px;
                text-align: center;
            }
            div.stButton > button:hover {
                background-color: #F0F0F0;
                border-color: #AAAAAA;
            }
            .stToggle { font-family: 'Calibri', sans-serif; color: #000000; }
            .report-text {
                font-family: 'Calibri', sans-serif;
                font-size: 16px;
                line-height: 1.8;
                border: 1px solid #DDDDDD;
                padding: 15px;
                border-radius: 8px;
                white-space: pre-wrap;
                background-color: #FAFAFA;
            }
            .copy-button {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-family: 'Calibri', sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Логика состояний (сессии) для МНОГИХ пользователей ---
def initialize_global_state():
    # Это создает "полку" для хранения блокнотов всех пользователей
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {}

def get_user_state():
    # Эта функция находит на "полке" личный блокнот текущего сотрудника
    username = st.session_state['username']
    if username not in st.session_state['user_data']:
        st.session_state['user_data'][username] = {
            'page': 'main',
            'toggles': {},
            'report_text': ""
        }
    return st.session_state['user_data'][username]

def logout():
    # Эта функция "закрывает сессию" - отправляет пользователя обратно к экрану входа
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.rerun()

# --- Функции для переключения страниц (НОВЫЕ ВЕРСИИ) ---
def go_to_page(page_name):
    # Теперь эта функция меняет страницу в ЛИЧНОМ блокноте пользователя
    user_state = get_user_state()
    user_state['toggles'] = {}
    user_state['page'] = page_name

def go_to_main():
    # То же самое для возврата на главную
    user_state = get_user_state()
    user_state['toggles'] = {}
    user_state['page'] = 'main'

def reset_all():
    # И сброс работает только для текущего пользователя
    user_state = get_user_state()
    user_state['page'] = 'main'
    user_state['toggles'] = {}
    user_state['report_text'] = ""

# --- Компонент для копирования ---
def copy_to_clipboard_component(text_to_copy):
    import random
    component_id = random.randint(1000, 9999)
    
    html_code = f"""
    <div style="margin: 10px 0;">
        <button id="copyBtn_{component_id}" onclick="copyToClipboard_{component_id}()" 
                style="background-color: #4CAF50; border: none; color: white; padding: 10px 20px; 
                       text-align: center; text-decoration: none; display: inline-block; 
                       font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 8px; 
                       font-family: 'Calibri', sans-serif;">
            Скопировать
        </button>
        <div id="copyMessage_{component_id}" style="color: green; font-weight: bold; margin-top: 10px; display: none;">
            Текст скопирован в буфер обмена!
        </div>
    </div>
    
    <script>
        function copyToClipboard_{component_id}() {{
            const text = `{text_to_copy}`;
            
            if (navigator.clipboard && window.isSecureContext) {{
                navigator.clipboard.writeText(text).then(function() {{
                    document.getElementById("copyMessage_{component_id}").style.display = "block";
                    setTimeout(function() {{
                        document.getElementById("copyMessage_{component_id}").style.display = "none";
                    }}, 2000);
                }}).catch(function(err) {{
                    fallbackCopy_{component_id}(text);
                }});
            }} else {{
                fallbackCopy_{component_id}(text);
            }}
        }}
        
        function fallbackCopy_{component_id}(text) {{
            const textArea = document.createElement("textarea");
            textArea.value = text;
            textArea.style.position = "fixed";
            textArea.style.left = "-999999px";
            textArea.style.top = "-999999px";
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {{
                document.execCommand('copy');
                document.getElementById("copyMessage_{component_id}").style.display = "block";
                setTimeout(function() {{
                    document.getElementById("copyMessage_{component_id}").style.display = "none";
                }}, 2000);
            }} catch (err) {{
                alert('Не удалось скопировать текст. Пожалуйста, скопируйте вручную.');
            }} finally {{
                document.body.removeChild(textArea);
            }}
        }}
    </script>
    """
    
    components.html(html_code, height=100)

# --- Логика генерации отчета ---
def generate_report_text(main_product, toggles):
    product_list = PRODUCT_LISTS.get(main_product.upper())
    if not product_list:
        return ""
    report_lines = [f"{product} {'+' if toggles.get(product, False) else '-'}" for product in product_list]
    return "\n".join(report_lines)

# --- Страницы приложения ---
def main_page():
    st.header("Выберите основной продукт")

    left_space, main_content, right_space = st.columns([1, 4, 1])

    with main_content:
        st.button(
            "ДК", 
            on_click=go_to_page, 
            args=('dk',), 
            use_container_width=True
        )
        
        st.button(
            "КК", 
            on_click=go_to_page, 
            args=('kk',), 
            use_container_width=True
        )
        
        st.button(
            "МП", 
            on_click=go_to_page, 
            args=('mp',), 
            use_container_width=True
        )

def product_submenu_page(product_type, product_list):
    user_state = get_user_state()
    
    st.header(f"Дополнительные продукты для «{product_type}»")
    
    for product in product_list:
        user_state['toggles'][product] = st.toggle(
            product,
            value=user_state['toggles'].get(product, False),
            key=f"{st.session_state['username']}_{product_type}_{product}"
        )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Сформировать отчет"):
            user_state['report_text'] = generate_report_text(product_type, user_state['toggles'])
            user_state['page'] = 'report'
            st.rerun()
            
    with col2:
        st.button("Вернуться", on_click=go_to_main)

def report_page():
    user_state = get_user_state()

    st.header("Сформированный отчет")
    
    report_text = user_state.get('report_text', "Отчет пуст.")
    
    st.text_area(
        label="Отчет для копирования:", 
        value=report_text, 
        height=200,
        help="Нажмите на текст, затем Ctrl+C (или Cmd+C), чтобы скопировать"
    )

    # Добавляем кнопку копирования
    copy_to_clipboard_component(report_text)

    st.button("Сбросить", on_click=reset_all)

# --- Главная функция приложения ---
def main():
    apply_styles()
    initialize_global_state()

    if not st.session_state.get('logged_in', False):
        login_page()
    else:
        st.write(f"Вы вошли как: {st.session_state['username']}")
        st.button("Выйти", on_click=logout)

        user_state = get_user_state()

        if user_state['page'] == 'main':
            main_page()
        elif user_state['page'] == 'dk':
            product_submenu_page("ДК", PRODUCTS_DK)
        elif user_state['page'] == 'kk':
            product_submenu_page("КК", PRODUCTS_KK)
        elif user_state['page'] == 'mp':
            product_submenu_page("МП", PRODUCTS_MP)
        elif user_state['page'] == 'report':
            report_page()

if __name__ == "__main__":
    main()
