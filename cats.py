import porter

cat_words = [
    "Feline",
    "Kitten",
    "Kitty",
    "Pussycat",
    "Mouser",
    "Tabby",
    "Tomcat",
    "Meow",
    "Purr",
    "Hiss",
    "Claw",
    "Paw",
    "Whiskers",
    "Litter",
    "Catnip",
    "Breed",
    "Fur",
    "Pounce",
    "Grooming",
    "Nuzzle",
    "Scratch",
    "Yowl",
    "Tail",
    "Paw",
    "Mew",
    "Felid",
    "Calico",
    "Tortoiseshell",
    "Tuxedo"
    "Siamese",
    "Persian",
    "Ragdoll",
    "Bengal",
    "Sphynx",
    "Abyssinian",
    "Shorthair",
    "Rex",
    "Burmese",
    "Siberian",
    "Himalayan",
    "Ragamuffin",
    "Manx",
    "Tonkinese",
    "Mau",
    "Ocicat",
    "Chartreux"
]

cleanCatList = []

def cleanCats():
    for word in cat_words:
        word = word.lower()
        word = porter.create_stem(word)
        cleanCatList += [word]
    return cleanCatList


