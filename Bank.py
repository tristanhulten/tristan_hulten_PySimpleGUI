#import av moduler
import PySimpleGUI as sg

#variabel, lista och dictionary
saldo = 1000
total = []
info = {}

#läs in inloggningsdata och lägg in i dictionary
def öppna_kontofil(filnamn):
    global info
    with open (filnamn) as login_file:
        for x in login_file:
            #split-funktionen delar upp strängar i .txt filen till en lista
            splitline = x.split("___-___")
            info[splitline[0]] = splitline[1]
    login_file.close

#färgtemat för gui
sg.theme("topanga")

#layout för appen och hur den är uppbyggd
def bankapp():
    global saldo, total
    layout =  [
            [sg.Text("Internetbanken")],
                        #key som motsvarar värdet av inputen
            [sg.Input("",key=("*INPUT1*"))],
            [sg.Button("Sätt in pengar" ,key=("*IN*"))],
                        #key som motsvarar värdet av inputen
            [sg.Input("",key=("*INPUT2*"))],
                        #keys som motsvarar knapptryck eller vissa händelser
            [sg.Button("Ta ut pengar",key=("*UT*"))],
            [sg.Button("Aktuellt saldo",key=("*SALDO*"))],
            [sg.Text("Output:",key=("*OUTPUT*"))],
            [sg.Button("Avsluta")]
            ]

    #bestämmer hur stor gui rutan skall vara och vilken layout den ska använda
    window = sg.Window("Bankapp",layout, margins=(100,75))

    #eventloop som gör olika baserat på vad användaren väljer
    while True:
        event, values = window.read()

        #avslutar programmet om användaren stänger fönstret eller trycker på "avsluta" knappen
        if event == "Avsluta" or event == sg.WIN_CLOSED:
            break
      
        #insättningar
        try:
            if event == "*IN*":
                värdemängd = int(values["*INPUT1*"])
                #felmeddelande om insättningen är mindre än 0
                if int(values["*INPUT1*"]) <= 0:
                    window["*OUTPUT*"].update("Felaktig insättning, insättning måste vara större än 0.")
                else:
                    #räknar ut saldot med pengarna som satts in
                    total.append(värdemängd)
                    output=värdemängd
                    saldo=saldo+output
                    window["*OUTPUT*"].update(f"Du har satt in {output} kr. Du har {saldo} kr på ditt konto")
        #en except på ValueError som kommer upp om man skriver bokstäver eller andra tecken i input rutan
        except ValueError: window["*OUTPUT*"].update("Ogiltig insättning, inte en siffra.")

        #visar saldot på ditt konto
        if event == "*SALDO*":
            window["*OUTPUT*"].update(f"Du har {saldo} kr på ditt konto")
        
        #uttag
        try:
            if event == "*UT*":
                uttag=int(values["*INPUT2*"])
                #om uttaget är negativt eller större än saldot får man felmeddelande
                if int(values["*INPUT2*"]) > saldo:
                    window["*OUTPUT*"].update("Felaktigt uttag, uttag kan inte vara större än saldot.")
                elif int(values["*INPUT2*"]) <= 0:
                    window["*OUTPUT*"].update("Felaktigt uttag, uttaget måste vara större än 0.")
                else:
                    #räknar ut saldot med pengarna som tagits ut
                    total.append(uttag)
                    saldo=saldo-uttag
                    window["*OUTPUT*"].update(f"Du har tagit ut {uttag} kr. Du har {saldo} kr på ditt konto")
        #en except på ValueError som kommer upp om man skriver bokstäver eller andra tecken i input rutan
        except ValueError: window["*OUTPUT*"].update("Ogiltigt uttag, inte en siffra.")
    #stänger fönstret om while loopen slutar gälla
    window.close()

#första menyn man ser som frågar om man vill logga in eller skapa konto
def meny1():
    #layout för gui rutan
    layout = [
        [sg.Text("Logga in eller registrera")],
        [sg.Button("Logga in"),sg.Button("Registrera konto")],
        [sg.Button("Avsluta")]
    ]
    #bestämmer hur stor gui rutan skall vara och vilken layout den ska använda
    layout = sg.Window("Logga in eller Registrera",layout,margins=(100,75))

    while True:
        event,values = layout.read()
        #avslutar programmet om användaren stänger fönstret eller trycker på "avsluta" knappen
        if event == sg.WIN_CLOSED:
            break
        if event == "Avsluta":
            break
        #trycker användaren på inloggning går programmet vidare till funktionen för inloggningar
        if event == "Logga in":
            inloggning()
        #trycker användaren på registrera går programmet vidare till funktionen för att registrera ett konto
        if event == "Registrera konto":
            meny2()
        #stänger rutan när användaren gjort sitt val
        layout.close()

#funktion för användare som vill skapa ett konto
def meny2():
    global info
    #layout för gui rutan
    skapa = [
        [sg.Text("Skapa ett nytt konto")],
        [sg.Text("Väl ditt användarnamn:"), sg.InputText('',key=("*ANVÄNDARNAMN*"))],
        [sg.Text("Välj ditt lösenord:"), sg.InputText('',key=("*LÖSENORD*"))],
        [sg.Button("Skapa Konto"),sg.Button("Avsluta")]
    ]
    #bestämmer hur stor gui rutan skall vara och vilken layout den ska använda
    skapa = sg.Window("Skapa konto",skapa,margins=(100,75))

    while True:
        event,values = skapa.read()
        #avslutar programmet om användaren stänger fönstret eller trycker på "avsluta" knappen
        if event == sg.WIN_CLOSED:
            break
        if event == "Avsluta":
            break
        #när användaren trycker på starta konto 
        if event =="Skapa Konto":
            #definerar variablerna lösenord och användarnamn enligt strängarna vi får ut i inputs ovan
            användarnamn = values["*ANVÄNDARNAMN*"]
            lösenord = values["*LÖSENORD*"]
            #felmeddelande om det nya användarnamnet redan används av någon annan
            if användarnamn in info:
                sg.popup("Användarnamn finns redan")
                continue
            #felmeddelande om det nya användarnamnet är samma som det vi använder som "splitter" (se första funktionen högst upp)
            elif användarnamn == "___-___":
                sg.popup("Ogiltigt användarnamn")
                continue
            #felmeddelande om det nya lösenordet är samma som det vi använder som "splitter" (se första funktionen högst upp)
            elif lösenord == "___-___":
                sg.popup("Ogiltigt lösenord")
                continue                  
            else:
                #skriver det nya användarnamnet och lösenordet till en textfil
                with open("login_data.txt", "a+") as login_file:
                    login_file.write(användarnamn + "___-___" + lösenord + "___-___" + "\n")
                    #tömmer dictionaryt som också innehåller inloggningsinformation
                    info.clear()
                    #stänger textfilen med inloggningsinformation
                    login_file.close
                #går tillbaka till funktionen som läser in inloggningsdatan och lägger in det i vårt dictionary
                #detta görs för att se till att ditt nya användarnamn och lösenord sparas i textfilen och dictionaryt innan du kommer till inloggningssidan
                öppna_kontofil("login_data.txt")
                #går vidare till inloggningssidan
                inloggning()

        return användarnamn, lösenord
    #stänger fönstret om while loopen slutar gälla
    skapa.close() 

#funktion för användare som vill logga in
def inloggning():
    global info
    #layout för gui rutan
    inlogg_layout = [
        [sg.Text("Användarnamn")],
        [sg.Input("",key=("*ANVÄNDARNAMN*"))],
        [sg.Text("Lösenord")],
        [sg.Input("",key=("*LÖSENORD*"))],
        [sg.Button("Logga in"),sg.Button("Avsluta")]
    ]
    #bestämmer hur stor gui rutan skall vara och vilken layout den ska använda
    inlogg_layout = sg.Window('Bankapp', inlogg_layout,margins=(100,75))

    while True:
        event,values = inlogg_layout.read()

        #definerar variablerna lösenord och användarnamn enligt strängarna vi får ut i inputs ovan
        användarnamn = values["*ANVÄNDARNAMN*"]
        lösenord = values["*LÖSENORD*"]

        #avslutar programmet om användaren stänger fönstret eller trycker på "avsluta" knappen
        if event == sg.WIN_CLOSED:
            break
        if event == "Avsluta":
            break
        #när användaren trycker logga in
        if event == "Logga in":
            #om användarnamnet finns i vårt dictionary (info) och lösenordet matchar användarnamnet
            if användarnamn in info and info[användarnamn] == lösenord:
                #går vidare till bankappen om man loggar in korrekt
                bankapp()
            else:
                #felmeddelande om användare inte finns eller om lösenordet inte matchar användaren
                sg.popup("Fel användare och/eller lösenord")
                continue
        else:
            sg.popup("Något gick fel försök igen")
            continue
        #stänger ner rutan när while loopen slutar gälla
        inlogg_layout.close()

#går först till funktionen som läser in inloggningsdatan och lägger in det i vårt dictionary
öppna_kontofil("login_data.txt")
#går sedan till första menyn
meny1()
