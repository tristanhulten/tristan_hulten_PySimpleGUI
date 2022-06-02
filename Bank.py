#import av moduler
import PySimpleGUI as sg

#variabel lista och dictionary
saldo = 1000
total = []
info = {}

#läs in inloggningsdata och lägg in i dictionary
def öppna_kontofil(filnamn):
    global info
    with open (filnamn) as login_file:
        for x in login_file:
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
            [sg.Input("",key=("*INPUT1*"))],
            [sg.Button("Sätt in pengar" ,key=("*IN*"))],
            [sg.Input("",key=("*INPUT2*"))],
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
                if int(values["*INPUT1*"]) <= 0:
                    window["*OUTPUT*"].update("Felaktig insättning, insättning måste vara större än 0.")
                else:
                    total.append(värdemängd)
                    output=värdemängd
                    saldo=saldo+output
                    window["*OUTPUT*"].update(f"Du har satt in {output} kr. Du har {saldo} kr på ditt konto")
        except ValueError: window["*OUTPUT*"].update("Ogiltig insättning, inte en siffra.")

        #visa saldo
        if event == "*SALDO*":
            window["*OUTPUT*"].update(f"Du har {saldo} kr på ditt konto")
        
        #uttag
        try:
            if event == "*UT*":
                uttag=int(values["*INPUT2*"])
                if int(values["*INPUT2*"]) > saldo:
                    window["*OUTPUT*"].update("Felaktigt uttag, uttag kan inte vara större än saldot.")
                elif int(values["*INPUT2*"]) <= 0:
                    window["*OUTPUT*"].update("Felaktigt uttag, uttaget måste vara större än 0.")
                else:
                    total.append(uttag)
                    saldo=saldo-uttag
                    window["*OUTPUT*"].update(f"Du har tagit ut {uttag} kr. Du har {saldo} kr på ditt konto")
        except ValueError: window["*OUTPUT*"].update("Ogiltigt uttag, inte en siffra.")
    #stänger fönstret om while loopen slutar gälla
    window.close()

def meny1():
   
    layout = [
        [sg.Text("Logga in eller registrera")],
        [sg.Button("Logga in"),sg.Button("Registrera konto")],
        [sg.Button("Avsluta")]
    ]

    layout = sg.Window("Logga in eller Registrera",layout,margins=(100,75))

    while True:
        event,values = layout.read()

        if event == sg.WIN_CLOSED:
            break
        if event == "Avsluta":
            break
        if event == "Logga in":
            inloggning()
        if event == "Registrera konto":
            meny2()
        layout.close()

def meny2():
    global info
    skapa = [
        [sg.Text("Skapa ett nytt konto")],
        [sg.Text("Väl ditt användarnamn:"), sg.InputText('',key=("*ANVÄNDARNAMN*"))],
        [sg.Text("Välj ditt lösenord:"), sg.InputText('',key=("*LÖSENORD*"))],
        [sg.Button("Skapa Konto"),sg.Button("Avsluta")]
    ]

    skapa = sg.Window("Skapa konto",skapa,margins=(100,75))

    while True:
        event,values = skapa.read()

        if event == sg.WIN_CLOSED:
            break
        if event == "Avsluta":
            break

        if event =="Skapa Konto":
            användarnamn = values["*ANVÄNDARNAMN*"]
            lösenord = values["*LÖSENORD*"]
            if användarnamn in info:
                sg.popup("Användarnamn finns redan")
                continue  
            elif användarnamn == "___-___":
                sg.popup("Ogiltigt användarnamn")
                continue
            elif lösenord == "___-___":
                sg.popup("Ogiltigt lösenord")
                continue                  
            else:
                with open("login_data.txt", "a+") as login_file:
                    login_file.write(användarnamn + "___-___" + lösenord + "___-___" + "\n")
                    info.clear()
                    login_file.close
                
                öppna_kontofil("login_data.txt")
                inloggning()

        return användarnamn, lösenord
  
    skapa.close() 

def inloggning():
    global info
    inlogg_layout = [
        [sg.Text("Användarnamn")],
        [sg.Input("",key=("*ANVÄNDARNAMN*"))],
        [sg.Text("Lösenord")],
        [sg.Input("",key=("*LÖSENORD*"))],
        [sg.Button("Logga in"),sg.Button("Avsluta")]
    ]

    inlogg_layout = sg.Window('Bankapp', inlogg_layout,margins=(100,75))

    while True:
        event,values = inlogg_layout.read()

        användarnamn = values["*ANVÄNDARNAMN*"]
        lösenord = values["*LÖSENORD*"]

        if event == sg.WIN_CLOSED:
            break
        if event == "Avsluta":
            break
        if event == "Logga in":
            if användarnamn in info and info[användarnamn] == lösenord:
                bankapp()
            else:
                sg.popup("Fel användare och/eller lösenord")
                continue
        else:
            sg.popup("Något gick fel försök igen")
            continue
        inlogg_layout.close()

öppna_kontofil("login_data.txt")
meny1()