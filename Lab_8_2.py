import sys
 
import matplotlib.pyplot as plt
import pandas as pd
 
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)
 
FILENAME = "comptage_velo_2013.csv"   
YEAR = 2013
MONTHS = ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер",
          "Лип", "Сер", "Вер", "Жов", "Лис", "Гру"]

df = None
for enc in ("utf-8", "latin1"):
    try:
        df = pd.read_csv(FILENAME, sep=None, engine="python", encoding=enc,
                         parse_dates=["Date"], dayfirst=True, index_col="Date")
        break
    except FileNotFoundError:
        print(f"Помилка: файл {FILENAME} не знайдено")
        sys.exit()
    except UnicodeDecodeError:
        continue
if df is None:
    print("Не вдалося прочитати файл")
    sys.exit()
 
df.index = pd.to_datetime(df.index, errors="coerce")
df = df[df.index.notna()]
df.index.name = "Date"
 
print(df.head())
print(df.info())
print(df.describe())

tracks = df.select_dtypes("number")
df = df[df.index.year == YEAR]
tracks = tracks.loc[df.index]

per_track = tracks.sum().sort_values(ascending=False)
print(f"\nКількість велосипедистів по кожній велодоріжці за {YEAR} рік:")
print(per_track)
print(f"\nЗагальна кількість велосипедистів за {YEAR} рік: {int(per_track.sum())}")

chosen_three = list(per_track.index[:3])
monthly = tracks.groupby(tracks.index.month).sum()
print("\nНайпопулярніший місяць для обраних велодоріжок:")
for name in chosen_three:
    best = monthly[name].idxmax()
    print(f"{name}: {MONTHS[best - 1]} ({int(monthly[name].max())} велосипедистів)")
 
track = chosen_three[0]
track_monthly = monthly[track]
print(f"\nДинаміка використання велодоріжки {track} за місяцями:")
print(track_monthly)
print("Мінімум:", MONTHS[track_monthly.idxmin() - 1], int(track_monthly.min()))
print("Максимум:", MONTHS[track_monthly.idxmax() - 1], int(track_monthly.max()))
 
fig, ax = plt.subplots()
ax.plot(track_monthly.index, track_monthly.values, marker="o", linewidth=2)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(MONTHS)
ax.set_title(f"Кількість велосипедистів на велодоріжці {track} за {YEAR} рік")
ax.set_xlabel("Місяць")
ax.set_ylabel("Кількість велосипедистів")
plt.tight_layout()
plt.savefig("bike_2013_monthly.png", dpi=150)
plt.show()