import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["deine_datenbank"]
collection = db["deine_sammlung"]

help_text = """
    Games-Datenbank CLI - Befehlsübersicht:
    Insert  -   insert "Titel","Erscheinungsjahr","Genre","Entwickler","Publisher","Plattformen","Bewertungssystem:Punkte, ..."
    Read    -   read ""
    Update  -   update "" to "",""
    Remove  -   remove ""
    Exit    -   exit
    """

#CRUD
def create(game_data):
    # Füge das Spiel in die Sammlung ein
    result = collection.insert_one(game_data)
    return result

def read(title):
    # Suche das Spiel in der Sammlung
    game = collection.find_one({"Titel": title})
    if game:
        return game  # Gibt das Spiel-Dokument zurück
    else:
        return "Spiel nicht gefunden."

def update(old_title, new_game_data):
    # Aktualisiere das Spiel in der Sammlung
    result = collection.update_one({"Titel": old_title}, {"$set": new_game_data})
    return result

def delete(title):
    # Lösche das Spiel aus der Sammlung
    result = collection.delete_one({"Titel": title})
    return result

print(help_text)

while True:
    command = input("Bitte Befehl eingeben: ").strip()

    if command.startswith("insert"):
        # Beispiel: insert "Halo","2005","IMDB:5,rottentomatos:7"
        content = command[len("insert "):].strip('"')
        title, year, ratings = content.split('","')
        ratings_dict = dict(rating.split(':') for rating in ratings.split(','))
        game_data = {
            "Titel": title,
            "Erscheinungsjahr": int(year),
            "Bewertungssystem": ratings_dict
        }
        print(create(game_data))

    elif command.startswith("read"):
        # Beispiel: read "Halo"
        title = command[len("read "):].strip('"')
        print(read(title))

    elif command.startswith("update"):
        # Beispiel: update "Halo" to "Halo 2","2007","IMDB:6,rottentomatos:8"
        content = command[len("update "):].strip('"')
        old_title, new_content = content.split(' to ')
        new_title, new_year, new_ratings = new_content.split('","')
        new_ratings_dict = dict(rating.split(':') for rating in new_ratings.split(','))
        new_game_data = {
            "Titel": new_title,
            "Erscheinungsjahr": int(new_year),
            "Bewertungssystem": new_ratings_dict
        }
        print(update(old_title, new_game_data))

    elif command.startswith("remove"):
        # Beispiel: remove "Halo"
        title = command[len("remove "):].strip('"')
        print(delete(title))

    elif command.lower() == "exit":
        print("Programm wird beendet.")
        break

    else:
        print("Ungültiger Befehl. Bitte versuche es erneut.")