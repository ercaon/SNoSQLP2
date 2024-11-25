import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["spiele"]
collection = db["pcgames"]

help_text = """
    Games-Datenbank CLI - Befehlsübersicht:
    [] beschreibt Zusätzliche informationen die nur für den nutzer sind und nicht für das Programm
    Insert          -   insert "Titel","Erscheinungsjahr","Downloads","FSK","Genre","Bewertung[x/10]"
    Info            -   info "[Title to id]"
    Read            -   read "[Title to id]"
    Search          -   search "[Title to id]"
    Test Connection -   test_connection
    Update          -   update "[Title to id]","[field to change]","[new Value]"
    Remove          -   remove "[Title to id]"
    Exit            -   exit
    """

#CRUD
def create(game_data):
    result = collection.insert_one(game_data)
    return result

def read(title):
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
    command = input("Bitte Befehl eingeben: ").lower()
    command, attributes = command.split(" ")
    attributes = attributes.split(",")
    for i in range(len(attributes)):
        attributes[i] = attributes[i].strip('"')

    if command == "test_connection":
        info = client.server_info()
        print(info)

    elif command == "insert":
        pass


    elif command[0] == "read":
        # Beispiel: read "Halo"
        title = command[len("read "):].strip('"')
        print(read(title))

    elif command[0] == "update":
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

    elif command[0] == "remove":
        # Beispiel: remove "Halo"
        title = command[len("remove "):].strip('"')
        print(delete(title))

    elif command[0].lower() == "exit":
        print("Programm wird beendet.")
        break

    else:
        print("Ungültiger Befehl. Bitte versuche es erneut.")