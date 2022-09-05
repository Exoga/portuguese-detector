import sys, ebooklib
from ebooklib import epub

ESTAR_CONJUGATIONS = {
    "estar",
    "estou", "estás", "está", "estamos", "estais", "estão",
    "estive", "estiveste", "esteve", "estivemos", "estivestes", "estiveram",
    "estava", "estavas", "estava", "estávamos", "estáveis", "estavam",
    "estarei", "estarás", "estará", "estaremos", "estareis", "estarão",
    "esteja", "estejas", "estejamos", "estejais", "estejam",
    "estivesse", "estivesses", "estivéssemos", "estivésseis", "estivessem",
    "estiver", "estiveres", "estivermos", "estiverdes", "estiverem",
    "estaria", "estarias", "estaríamos", "estaríeis", "estariam"
}

# The % useage of infinitive gerund in the text (a text above this is classified PT-PT, below is classified PT-BR)
PORTUGAL_BRAZIL_THRESHOLD = 0.08

path = sys.argv[1]

book = epub.read_epub(path)

title = book.get_metadata('DC', 'title')

if len(title) == 0:
    raise Exception("Potentially unsupported format!")

title = title[0][0]

print(f"Found ebook: {title}")
print("Attempting to parse...")

documents = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)

def findInfinitive(text):
    instances = []
    nonInstances = []
    listOfWords = text.split()
    wordCount = len(listOfWords)
    for i in range(wordCount):
        word = listOfWords[i]
        if word not in ESTAR_CONJUGATIONS:
            continue
        if wordCount <= i+2:
            continue
        if listOfWords[i+1] == "a":
            instances.append(f"{word} a {listOfWords[i+2]}")
        else:
            nonInstances.append(f"{word} {listOfWords[i+1]}")
    return {
        "ig": instances,
        "other": nonInstances
    }

infinitives = []
nonInfinitives = []

for document in documents:
    ig = findInfinitive(document.get_body_content().decode())
    infinitives.extend(ig["ig"])
    nonInfinitives.extend(ig["other"])

print("Infinitive Gerund:")
print(infinitives)
print("Other uses of estar:")
print(nonInfinitives)

print(f"Found {len(infinitives)} instances of estar with infinitive gerund and {len(nonInfinitives)} other uses of 'estar'.")
portugalyness = len(infinitives) / len(nonInfinitives)
classification = ""
if portugalyness >= PORTUGAL_BRAZIL_THRESHOLD:
    classification = "European"
else:
    classification = "Brazilian"
print(f"This e-book is most likely {classification} Portuguese.")
