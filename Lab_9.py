import string
 
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import gutenberg, stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer, WordNetLemmatizer

for resource in ("gutenberg", "stopwords", "wordnet", "omw-1.4", "punkt", "punkt_tab"):
    nltk.download(resource, quiet=True)
 
FILE_ID = "edgeworth-parents.txt"
plt.style.use("ggplot")
 
 
def bar_chart(top, title, filename):
    words = [w for w, _ in top]
    counts = [c for _, c in top]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(words, counts, color="steelblue")
    ax.set_title(title)
    ax.set_xlabel("Слово")
    ax.set_ylabel("Кількість уживань")
    for i, c in enumerate(counts):
        ax.text(i, c, str(c), ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()
 
print(gutenberg.fileids())
text = gutenberg.words(FILE_ID)
 
total = len(text)
unique = len(set(text))
print("\nКількість слів (токенів) у тексті:", total)
print("Кількість унікальних слів:", unique)
print(f"Унікальні слова становлять {unique / total:.1%} від усіх токенів")
print(f"Кожне унікальне слово вживається в середньому {total / unique:.1f} разів")

fdist = FreqDist(text)
top_ten = fdist.most_common(10)
print("\n10 найбільш вживаних слів:")
print(top_ten)
bar_chart(top_ten, "10 найуживаніших слів (edgeworth-parents)", "top10_raw.png")

stop_words = set(stopwords.words("english"))
without_stop_words = [w for w in text if w.lower() not in stop_words]
print("\nТекст після видалення стоп-слів:")
print(without_stop_words[:20])
 
table = str.maketrans("", "", string.punctuation)
stripped = [w.translate(table).lower() for w in without_stop_words]
stripped = [w for w in stripped if w.isalpha()] 
 
print("\nКількість слів після очищення:", len(stripped))
print("Кількість унікальних слів після очищення:", len(set(stripped)))
 
fdist_clean = FreqDist(stripped)
top_ten_clean = fdist_clean.most_common(10)
print("\n10 найбільш вживаних слів після видалення стоп-слів та пунктуації:")
print(top_ten_clean)
bar_chart(top_ten_clean, "10 найуживаніших слів без стоп-слів і пунктуації",
          "top10_clean.png")

lemmatizer = WordNetLemmatizer()

lemmas = [lemmatizer.lemmatize(lemmatizer.lemmatize(w, pos="n"), pos="v") for w in stripped]
top_ten_lemmas = FreqDist(lemmas).most_common(10)
print("\n10 найбільш вживаних слів після лематизації:")
print(top_ten_lemmas)
 
stemmer = PorterStemmer()
stems = [stemmer.stem(w) for w in stripped]
top_ten_stems = FreqDist(stems).most_common(10)
print("\n10 найбільш вживаних слів після стемінгу (Porter):")
print(top_ten_stems)