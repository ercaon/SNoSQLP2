import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["spiele"]
collection = db["pcgames"]

help_text = """
    Games-Datenbank CLI - Befehlsübersicht:
    [] beschreibt Zusätzliche informationen die nur für den nutzer sind und nicht für das Programm
    Vorhandene Felder:
        title
        erscheinungsjahr
        downloads
        fsk
        genere
        rating
    
    Test Connection -   test_connection
    Insert          -   insert "Titel","Erscheinungsjahr"...
    Search          -   search "[Titel zum identifizieren]"
    Update          -   update "[Titel zum identifizieren]","[Feld zum updaten]","[neuer Wert]"
    Remove          -   remove "[Titel zum identifizieren]"
    Exit            -   exit
    
    !!! Wichtiger Hinweis: Der Title wird zum identifizieren verwendet, falls er mehrfach vorkommt, 
        werden alle identifizierten Beiträge bearbeitet.!!!
    """

schluessel: list[str] = ["title", "erscheinungsjahr", "downloads", "fsk", "genre", "rating"]


print(help_text)

while True:
    command = input("Bitte Befehl eingeben: ").lower()

    if command.lower() == "exit": exit()

    command, attributes = command.split(" ")
    attributes = attributes.split(",")

    for i in range(len(attributes)):
        attributes[i] = attributes[i].strip('"')


    if command == "test_connection":
        info = client.server_info()
        print(info)

    elif command == "insert":
        document = dict(zip(schluessel, attributes))
        if len(document) != 6:
            print("Nicht die richtige Menge an Argumenten gegeben.")
            continue
        ergebnis = collection.insert_one(document)
        print("Erfolgreich" if ergebnis.acknowledged == True else "Nicht erfolgreich")

    elif command == "search":
        kriterium = {"title": attributes[0]}
        ergebnis = list(collection.find(kriterium))
        if ergebnis:
            for element in ergebnis:
                print(f"""
                    ID: {element["_id"]}
                    Title: {element["title"]}
                    Erscheinungsjahr: {element["erscheinungsjahr"]}
                    Altersfreigabe: {element["fsk"]}
                    Gruppe: {element["genre"]}
                    Rating: {element["rating"]}
                """)
        else:
            print("Nicht gefunden.")

    elif command == "update":
        kriterium = {"title": attributes[0]}
        update = {"$set":{attributes[1]: attributes[2]}}
        ergebnis = collection.update_many(kriterium, update)
        print("Erfolgreich" if ergebnis.acknowledged == True else "Nicht erfolgreich")

    elif command == "remove":
        kriterium = {"title": attributes[0]}
        ergebnis = collection.delete_many(kriterium)
        print("Erfolgreich" if ergebnis.acknowledged == True else "Nicht erfolgreich")

    else:
        print(f"Ungültiger Befehl. Bitte versuche es erneut. {command} - {attributes}")