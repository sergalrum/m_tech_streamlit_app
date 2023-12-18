# Загрузка библиотек
import pandas as pd

import streamlit as st
import re
from io import StringIO
from scipy import stats as scst



# Установка формата
st.set_page_config(layout="wide")

# Загрузка файла
uploaded_file = st.sidebar.file_uploader("Choose an csv file", ["csv"]) #csv uploader
st.sidebar.write('Or')
use_default_df = st.sidebar.checkbox('Use default DF')

if use_default_df or uploaded_file is None:
    with open('М.Тех_Данные_к_ТЗ_DS.csv') as f:
        text = re.sub(r'"*([\r\n])+"*|(?:^"*|"*$)|""', '\\1', f.read())
    fixed_text = StringIO(text)
    df = pd.read_csv(fixed_text)

elif uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("cp1251"))
    text = re.sub(r'"*([\r\n])+"*|(?:^"*|"*$)|""', '\\1', stringio.read())
    fixed_text = StringIO(text)
    df = pd.read_csv(fixed_text)

# Уточнение изменяемых значений
work_days = st.sidebar.number_input("work_days", step=1, min_value=0, max_value=df['Количество больничных дней'].max(), value=2)
age = st.sidebar.slider("age", step=1, min_value=df['Возраст'].min(), max_value=df['Возраст'].max(), value=35)
df_hip = df.loc[df['Количество больничных дней'] >= work_days]

st.title("Проверка гипотез :red[М.Тех]")





############################################################################################################################################################################
# Гипотеза 1
# Предисловие
st.markdown("## Гипотеза 1")
st.markdown(f"Мужчины пропускают в течение года более {work_days} рабочих дней  по болезни значимо чаще женщин.")
st.markdown(f'- нулевая гипотеза - Мужчины пропускают в течение года более {work_days} рабочих дней по болезни столько же, сколько женщины')
st.markdown(f'- альтернативная гипотеза - Мужчины пропускают в течение года более {work_days} рабочих дней по болезни значимо чаще женщин.')
st.markdown(f'Используем метод `scipy.stats.ttest_ind()`, поскольку необходимо сравнить 2 набора данных, которые не зависят друг от друга.')

# Подготовка датафреймов
df_chart_m = df_hip.loc[df_hip['Пол']=='М'].groupby('Количество больничных дней')['Возраст'].count().reset_index()
df_chart_m.columns = ['Количество больничных дней', 'Количество сотрудников']
df_chart_w = df_hip.loc[df_hip['Пол']=='Ж'].groupby('Количество больничных дней')['Возраст'].count().reset_index()
df_chart_w.columns = ['Количество больничных дней', 'Количество сотрудников']

# Оформление графиков
container = st.container()
chart1, chart2 = container.columns(2)

with chart1:
    st.header("График распределения :blue[мужчин] по количеству больничных дней", divider='blue')
    st.bar_chart(data=df_chart_m, x='Количество больничных дней', y='Количество сотрудников', height=500)

with chart2:
    st.header("График распределения :red[женщин] по количеству больничных дней", divider='red')
    st.bar_chart(data=df_chart_w, x='Количество больничных дней', y='Количество сотрудников', height=500, color="#FF0000")

# Расчет pvalue
alpha_hip_1 = 0.05 # уровень статистической значимости
test_m = df_hip.loc[df_hip['Пол']=='М']['Количество больничных дней']
test_w = df_hip.loc[df_hip['Пол']=='Ж']['Количество больничных дней']
results_hip_1 = scst.ttest_ind(test_m, test_w, alternative='greater', equal_var=False)

# Вывод результатов расчета
st.markdown(f'Установленный уровень статистической значимости для первой гипотезы: {alpha_hip_1}')
st.markdown(f'Значение p-value для наблюдаемого на выборке значения: {results_hip_1.pvalue}')
if results_hip_1.pvalue < alpha_hip_1:
    st.markdown('##### Отвергаем нулевую гипотезу.')
else:
    st.markdown('##### Нет оснований отвергнуть нулевую гипотезу, вероятно, значения отличаются не значительно.')





############################################################################################################################################################################
# Гипотеза 2
# Предисловие
st.markdown("## Гипотеза 2")
st.markdown(f"Работники старше {age} лет пропускают в течение года более {work_days} рабочих дней по болезни значимо чаще своих более молодых коллег.")
st.markdown(f'- нулевая гипотеза - Работники старше {age} лет пропускают в течение года более {work_days} рабочих дней по болезни столько же, сколько их молодые коллеги.')
st.markdown(f'- альтернативная гипотеза - Работники старше {age} лет пропускают в течение года более {work_days} рабочих дней по болезни значимо чаще своих более молодых коллег.')
st.markdown(f'Используем метод `scipy.stats.ttest_ind()`, поскольку необходимо сравнить 2 набора данных, которые не зависят друг от друга.')

# Подготовка датафреймов
df_chart_old = df_hip.loc[df_hip['Возраст']>=age].groupby('Количество больничных дней')['Пол'].count().reset_index()
df_chart_old.columns = ['Количество больничных дней', 'Количество сотрудников']
df_chart_yng = df_hip.loc[df_hip['Возраст']<age].groupby('Количество больничных дней')['Пол'].count().reset_index()
df_chart_yng.columns = ['Количество больничных дней', 'Количество сотрудников']

# Оформление графиков
container = st.container()
chart1, chart2 = container.columns(2)

with chart1:
    st.header(f"График распределения сотруднико по количеству больничных дней :blue[старше {age}]", divider='blue')
    st.bar_chart(data=df_chart_old, x='Количество больничных дней', y='Количество сотрудников', height=500)

with chart2:
    st.header(f"График распределения сотруднико по количеству больничных дней :red[моложе {age}]", divider='red')
    st.bar_chart(data=df_chart_yng, x='Количество больничных дней', y='Количество сотрудников', height=500, color="#FF0000")

# Расчет pvalue
alpha_hip_2 = 0.05 # уровень статистической значимости
test_old = df_hip.loc[df_hip['Возраст']>=age]['Количество больничных дней']
test_yng = df_hip.loc[df_hip['Возраст']<age]['Количество больничных дней']
results_hip_2 = scst.ttest_ind(test_old, test_yng, alternative='greater', equal_var=False)

# Вывод результатов расчета
st.markdown(f'Установленный уровень статистической значимости для первой гипотезы: {alpha_hip_2}')
st.markdown(f'Значение p-value для наблюдаемого на выборке значения: {results_hip_2.pvalue}')
if results_hip_2.pvalue < alpha_hip_2:
    st.markdown('##### Отвергаем нулевую гипотезу.')
else:
    st.markdown('##### Нет оснований отвергнуть нулевую гипотезу, вероятно, значения отличаются не значительно.')
