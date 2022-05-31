#import av moduler
import PySimpleGUI as sg


saldo = 1000
total = []

#färgtemat för gui
sg.theme('topanga')

#layout för appen och hur den är uppbyggd
layout =  [
        [sg.Text("Internetbanken")],
        [sg.Button("1. Insättningar" ,key=("*IN*"))],
        [sg.Input("",key=("*INPUT1*"))],
        [sg.Button("2. Uttag",key=("*UT*"))],
        [sg.Input("",key=("*INPUT2*"))],
        [sg.Button("3. Saldo",key=("*SALDO*"))],
        [sg.Text("Output:",key=("*OUTPUT*"))],
        [sg.Button("Avsluta")]
        ]


window = sg.Window('bankapp',layout, margins=(100,75))

#eventloop som gör olika baserat på vad användaren väljer
while True:
    event, values = window.read()

    #avslutar programmet om användaren stänger fönstret eller trycker på "avsluta" knappen
    if event == 'Avsluta' or event == sg.WIN_CLOSED:
        break
    
    #insättningar
    if event == "*IN*":
        värdemängd = int(values["*INPUT1*"])
        total.append(värdemängd)
        output=värdemängd
        saldo=saldo+output
        window["*OUTPUT*"].update(f"Du har satt in {output} kr. Du har {saldo} kr på ditt konto")

    #visa saldo
    if event == "*SALDO*":
        window["*OUTPUT*"].update(f"Du har {saldo} kr på ditt konto")

    #uttag
    if event == "*UT*":
        uttag=int(values["*INPUT2*"])
        total.append(uttag)
        saldo=saldo-uttag
        window["*OUTPUT*"].update(f"Du har tagit ut {uttag} kr. Du har {saldo} kr på ditt konto")
#stänger fönstret om while loopen slutar gälla
window.close()


