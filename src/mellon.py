from kodeerimine import dekodeeri_seifidest, kodeeri_seifidesse
import PySimpleGUI as sg
import sys

def main():
    esimesed_valikud = [
        [
            sg.Button("Kodeeri", key="-TEGEVUS KODEERI-"),
            sg.Button("Dekodeeri", key="-TEGEVUS DEKODEERI-"),
        ],
        [
            sg.Button("Lõpeta", key="-LÕPETA-")
        ]
    ]

    aken = sg.Window("Mellon", layout=esimesed_valikud)

    while True:
        sündmus, _ = aken.read()

        if sündmus == "-LÕPETA-" or sündmus == sg.WIN_CLOSED:
            aken.close()
            break
        elif sündmus == "-TEGEVUS KODEERI-":
            kodeeri()

        elif sündmus == "-TEGEVUS DEKODEERI-":
            dekodeeri()


def kodeeri():
    failide_nupud = [
        [
            sg.Input(key="SALADUSED", visible=True),
            sg.FilesBrowse("Vali Saladused"),
        ],
        [
            sg.Input(key="SEIFID", visible=True),
            sg.FilesBrowse("Vali Seifid"),
        ],
        [
            sg.Input(key="SEIFIDE_UUS_KAUST", visible=True),
            sg.FolderBrowse("Vali seifide salvestamise kaust")
        ],
        [
            sg.Button("Kodeeri"),
        ]
    ]

    väljund = [
        [
            sg.Text("Programmi väljund:")
        ],
        [
            sg.Output(size=(80, 25)),
        ],
        [
            sg.Cancel("Tagasi"),
        ],
    ]

    nuppude_paigutus = [
        [
            sg.Column(failide_nupud),
            sg.VSeperator(),
            sg.Column(väljund),
        ]
    ]

    aken = sg.Window("Mellon kodeerija", layout=nuppude_paigutus)
    while True:
        sündmus, väärtused = aken.read()
        if sündmus == sg.WIN_CLOSED:
            aken.close()
            sys.exit(0)
        if sündmus == "Tagasi":
            break
        elif sündmus == "Kodeeri":
            saladused = list(väärtused["SALADUSED"].split(';'))
            seifid = list(väärtused["SEIFID"].split(';'))
            seifide_uus_kaust = väärtused["SEIFIDE_UUS_KAUST"]

            print(f"{saladused}\n{seifid}\n{seifide_uus_kaust}")

            try:
                kodeeri_seifidesse(seifid, saladused, seifide_uus_kaust)
            except Exception as e:
                print(f"VIGA: {str(e)} PROOVI UUESTI")

    aken.close()
    return

def dekodeeri():
    failide_nupud = [
        [
            sg.Input(key="SEIFID", visible=True),
            sg.FilesBrowse("Vali Seifid"),
        ],
        [
            sg.Input(key="SALADUSE_UUS_NIMI", visible=True),
            sg.FileSaveAs("Vali saladuse uus nimi")
        ],
        [
            sg.Button("Dekodeeri"),
        ]
    ]

    väljund = [
        [
            sg.Text("Programmi väljund:")
        ],
        [
            sg.Output(size=(80, 25)),
        ],
        [
            sg.Cancel("Tagasi")
        ]
    ]

    nuppude_paigutus = [
        [
            sg.Column(failide_nupud),
            sg.VSeperator(),
            sg.Column(väljund),
        ]
    ]

    aken = sg.Window("Mellon dekodeerija", layout=nuppude_paigutus)
    while True:
        sündmus, väärtused = aken.read()
        if sündmus == sg.WIN_CLOSED:
            aken.close()
            sys.exit(0)
        if sündmus == "Tagasi":
            break
        elif sündmus == "Dekodeeri":
            seifid = list(väärtused["SEIFID"].split(';'))
            saladuse_uus_nimi = väärtused["SALADUSE_UUS_NIMI"]

            print(f"seifid: {seifid}\nsaladuse_uus_nimi: {saladuse_uus_nimi}")

            try:
                dekodeeri_seifidest(seifid, saladuse_uus_nimi)
            except Exception as e:
                print(f"VIGA: {str(e)} PROOVI UUESTI")

    aken.close()
    return

if __name__ == "__main__":
    main()
