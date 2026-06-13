import json

dogs = [
    "Labrador Retriever", "German Shepherd", "Golden Retriever", "French Bulldog", "Bulldog",
    "Poodle", "Beagle", "Rottweiler", "German Shorthaired Pointer", "Dachshund",
    "Pembroke Welsh Corgi", "Australian Shepherd", "Yorkshire Terrier", "Boxer",
    "Great Dane", "Siberian Husky", "Cavalier King Charles Spaniel", "Doberman Pinscher",
    "Miniature Schnauzer", "Shih Tzu", "Boston Terrier", "Bernese Mountain Dog",
    "Pomeranian", "Havanese", "Cane Corso", "English Springer Spaniel", "Shetland Sheepdog",
    "Brittany", "Pug", "Cocker Spaniel", "Miniature American Shepherd", "Border Collie",
    "Mastiff", "Chihuahua", "Vizsla", "Basset Hound", "Belgian Malinois",
    "Maltese", "Weimaraner", "Collie", "Newfoundland", "Rhodesian Ridgeback",
    "Shiba Inu", "West Highland White Terrier", "Bichon Frise", "Bloodhound",
    "English Cocker Spaniel", "Akita", "Portuguese Water Dog", "Chesapeake Bay Retriever",
    "Dalmatian", "St. Bernard", "Papillon", "Australian Cattle Dog", "Bullmastiff",
    "Samoyed", "Scottish Terrier", "Soft Coated Wheaten Terrier", "Whippet",
    "German Wirehaired Pointer", "Chinese Shar-Pei", "Wirehaired Pointing Griffon",
    "Great Pyrenees", "Alaskan Malamute", "Cardigan Welsh Corgi", "Cairn Terrier",
    "Irish Setter", "Giant Schnauzer", "Old English Sheepdog", "Bull Terrier",
    "Chow Chow", "Italian Greyhound", "Pekingese", "Irish Wolfhound"
]

cats = [
    "Persian", "Maine Coon", "Ragdoll", "Sphynx", "British Shorthair",
    "Abyssinian", "Exotic Shorthair", "Siamese", "Scottish Fold", "Burmese",
    "Birman", "American Shorthair", "Bengal", "Russian Blue", "Norwegian Forest Cat",
    "Siberian", "Oriental Shorthair", "Devon Rex", "Cornish Rex", "Himalayan",
    "Munchkin", "Savannah", "Turkish Angora", "Balinese", "Tonkinese",
    "Somali", "Egyptian Mau", "American Curl", "Colorpoint Shorthair", "Singapura"
]

foods = [
    {"id": "apples", "name": "Apples", "category": "Fruit"},
    {"id": "chocolate", "name": "Chocolate", "category": "Sweets"},
    {"id": "grapes", "name": "Grapes", "category": "Fruit"},
    {"id": "bananas", "name": "Bananas", "category": "Fruit"},
    {"id": "blueberries", "name": "Blueberries", "category": "Fruit"},
    {"id": "onions", "name": "Onions", "category": "Vegetable"},
    {"id": "garlic", "name": "Garlic", "category": "Vegetable"},
    {"id": "watermelon", "name": "Watermelon", "category": "Fruit"},
    {"id": "tomatoes", "name": "Tomatoes", "category": "Vegetable"},
    {"id": "strawberries", "name": "Strawberries", "category": "Fruit"},
    {"id": "avocado", "name": "Avocado", "category": "Fruit"},
    {"id": "peanut-butter", "name": "Peanut Butter", "category": "Snacks"},
    {"id": "bread", "name": "Bread", "category": "Carbs"},
    {"id": "cheese", "name": "Cheese", "category": "Dairy"},
    {"id": "macadamia-nuts", "name": "Macadamia Nuts", "category": "Nuts"}
]

breeds = []

for dog in dogs:
    breeds.append({
        "id": dog.lower().replace(' ', '-'),
        "name": dog,
        "emoji": "🐶"
    })

for cat in cats:
    breeds.append({
        "id": cat.lower().replace(' ', '-'),
        "name": cat,
        "emoji": "🐱"
    })

schema = {
    "breeds": breeds,
    "foods": foods
}

with open('data/schema.json', 'w') as f:
    json.dump(schema, f, indent=2)

print(f"Added {len(dogs)} dogs and {len(cats)} cats to schema.json!")
