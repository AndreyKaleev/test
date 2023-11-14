import pandas as pd
import ssl
import matplotlib.pyplot as plt

# подключаю SSL т.к. без него при открытии ссылки на MacOS возникает ошибка
ssl._create_default_https_context = ssl._create_unverified_context

# Создаю DataFrame загружая в него данные из GoogleSheets в формате CSV
sheets_id = "1S5WVifuEWZzlKz2Z9qUOQpa04M4avj_WkFKohK5ZNiw"
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheets_id}/export?format=csv")

# Чтобы суммировать продажи за день, обращаюсь к полю lastchangedate
# и преобразовываю его из формата "дата+время" в формат "дата"
df['lastchangedate'] = pd.to_datetime(df['lastchangedate']).dt.date

# создаю новый DaraFrame res(result) в котором будут сохранены
# промежуточные итоги продаж по дням
res = df.groupby('lastchangedate', as_index=False)['totalprice'].sum()

# для последующей фильтрации нужно преобразовать данные колонки
# "lastchangedate" из строкового формата в формат DateTime
res['lastchangedate'] = pd.to_datetime(res['lastchangedate'])

# для создания выборки продаж за март 2023г из DataFrame res
# создаю маску с нужными датами
mask = (res['lastchangedate'] > '2023-03-01') & (res['lastchangedate'] <= '2023-03-31')

# применяю функцию loc с указанием маски и сохраняю результат в
# DataFrame res
res = res.loc[mask]

# на основе DataFrame res создаю график
# вертикальная ось - сумма продажи
# горизонтальная ось - временной диапазон (даты с 1 по 31 марта 2023)
res.plot(x='lastchangedate', y='totalprice')

# вывод графика на экран
plt.show()
