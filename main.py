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
    
    Insert          -   insert "Titel","Erscheinungsjahr"...
    Search          -   search "[Feld zum identifizieren]"
    Test Connection -   test_connection
    Update          -   update "[Feld zum identifizieren]","[Feld zum updaten]","[neuer Wert]"
    Remove          -   remove "[Feld zum identifizieren]"
    Exit            -   exit
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
        print(kriterium)
        ergebnis = collection.find(kriterium)
        if ergebnis:
            print(ergebnis)
        else:
            print("Nicht gefunden.")

    elif command[0] == "update":
        pass

    elif command[0] == "remove":
        pass

    else:
        print(f"Ungültiger Befehl. Bitte versuche es erneut. {command} - {attributes}")