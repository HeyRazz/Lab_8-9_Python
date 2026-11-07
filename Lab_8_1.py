import os
import sys
 
import pandas as pd
import requests
 
SOURCE_CSV = "ukraine_life_expectancy_1991_2019.csv"  
EXTENDED_CSV = "ukraine_extended_1991_2019.csv"        
LIFE = "Life expectancy at birth, total (years)"
EXTRA_INDICATORS = {
    "Population, total": "SP.POP.TOTL",
    "GDP per capita (current US$)": "NY.GDP.PCAP.CD",
}
 
 
def fetch_indicator(code, country="ua", date_range="1991:2019"):
    url = (f"https://api.worldbank.org/v2/country/{country}/indicator/{code}"
           f"?date={date_range}&format=json&per_page=500")
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list) or len(data) < 2 or not data[1]:
        raise ValueError(f"API не повернув даних для {code}")
    return {int(item["date"]): item["value"] for item in data[1]}
 
 
def build_extended_csv():
    base = pd.read_csv(SOURCE_CSV)
    for column, code in EXTRA_INDICATORS.items():
        values = fetch_indicator(code)
        base[column] = base["Year"].map(values)
        print(f"Додано стовпець '{column}'")
    base.to_csv(EXTENDED_CSV, index=False, encoding="utf-8")
    print(f"Розширений набір даних збережено: {EXTENDED_CSV}")
 

if not os.path.exists(EXTENDED_CSV):
    try:
        build_extended_csv()
    except (requests.exceptions.RequestException, ValueError, KeyError) as err:
        print(f"Не вдалося отримати додаткові показники: {err}")
        sys.exit()
 
try:
    df = pd.read_csv(EXTENDED_CSV)
    print("Файл успішно завантажено")
except FileNotFoundError:
    print("Помилка: файл не знайдено")
    sys.exit()

print("\nПочаткові дані:")
print(df)
 
print("\nПерші 3 рядки DataFrame:")
print(df.head(3))
 
print("\nТипи даних:")
print(df.dtypes)
 
print("\nРозмір DataFrame (рядки, стовпці):")
print(df.shape)
 
print("\nОписова статистика:")
print(df.describe())

df["Year"] = df["Year"].astype(int)
df["Population, total"] = df["Population, total"].astype("int64")

df = df.sort_values("Year").reset_index(drop=True)

df["Population_mln"] = (df["Population, total"] / 1_000_000).round(2)
df["Life_exp_change"] = df[LIFE].diff().round(3)       
df["Life_per_1000USD_GDP"] = (df[LIFE] / df["GDP per capita (current US$)"] * 1000).round(3)
df["Decade"] = (df["Year"] // 10 * 10).astype(str) + "-ті"  
 
print("\nDataFrame з новими стовпцями:")
print(df)

filtered_df = df[df[LIFE] > 70]
print("\nРезультат фільтрації (тривалість життя > 70 років):")
print(filtered_df)

sorted_df = df.sort_values(by=LIFE, ascending=False)
print("\nРезультат сортування за тривалістю життя:")
print(sorted_df)

grouped_df = df.groupby("Decade").agg(
    Years_count=("Year", "count"),
    Life_mean=(LIFE, "mean"),
    Life_max=(LIFE, "max"),
    Life_min=(LIFE, "min"),
    GDP_mean=("GDP per capita (current US$)", "mean"),
    Population_mln_mean=("Population_mln", "mean"),
).round(2).reset_index()
print("\nРезультат групування за десятиліттями:")
print(grouped_df)
 
print("\nКількість унікальних значень:")
print("Країн:", df["Country Name"].nunique())
print("Років:", df["Year"].nunique())
print("Десятиліть:", df["Decade"].nunique())

df.to_csv("results_full.csv", index=False, sep=";", encoding="utf-8-sig")
filtered_df.to_csv("results_filtered.csv", index=False, sep=";", encoding="utf-8-sig")
sorted_df.to_csv("results_sorted.csv", index=False, sep=";", encoding="utf-8-sig")
grouped_df.to_csv("results_grouped.csv", index=False, sep=";", encoding="utf-8-sig")
print("\nРезультати збережено у файли results../.csv")
 