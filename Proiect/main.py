import math
import sys
from easygui import *

#############################################################################################################################
#Am ales pentru acest proiect sa criptez textul clar cu cifrul Bifid, dupa care sa criptez rezultatul cu cifrul Nihilist.
#Decriptarea este in mod simteric, mai intai voi descifra cu Nihilist dupa care cu Bifid.
#
# Programu ia din 'Input' textul si aplica actiunea ceruta din GUI si scrie in 'Output' rezultatu.
# Am facut si fisiere in plus in care sa se vada cifrarile separat
#######################################################################################################################


def patrat_polybius(cheie):#primeste cheia secreta ca un sir de caractere mici
    patrat=[]
    for i in range(0,len(cheie)):
        if cheie[i] not in patrat :#daca nu este dea un element din cheie il pune
            patrat.append(cheie[i])
    for i in range(0,len(alfabet)):
        if alfabet[i] not in patrat :#completeaza patratu cu restul alfabetului
            patrat.append(alfabet[i])
    return patrat

def literaToCoordonata(litera):
    coordonate=[]#O sa am intr-o lista coordonatele [i,j]
    if litera=='j' : litera='i'#in caz ca primeste ca litera 'j' o va considera drept 'i' si va continua prelucrarea
    for i in range(0,len(patratPolybius)):
        if litera==patratPolybius[i]:#ca sa gasesc pozitia din patratul polybius a literei pe care vreau sa o transform
            break
    coordonate.append(math.floor(i/5)+1)#fomrula ca sa transforma din coordonata in pozitia linii
    coordonate.append(i%5+1)#fomrula ca sa transforma din coordonata in pozitia coloanei
    return coordonate

def textToCoordonate(text):#transforma din text in lista de grupuri a cate doua coordonate [i,j]
    nou_text=[]
    for i in range(0,len(text)):
        nou_text.append(literaToCoordonata(text[i]))
    return nou_text

def cifreToCoordonate(text):#primeste ca data de intrare un string cu textul cifrat fara spatii intre perechi
    coor = []
    for i in range(0,len(text)):
        if len(text[i])>2:#daca am un sir mai mare de 2 inseamna ca trebuie sa despart cele doua cifre in functie de pozitia zeroului
            if(text[i][1]=='0'):#daca in mijloc se afla 0 inseamna ca prima coordonata este formata din doua cifre
                coor.append([int(text[i][0])*10+int(text[i][1]), int(text[i][2])])
            else:#daca in mijloc nu se afla 0 inseamna ca a doua coordonata este cea formata din doua cifre
                coor.append([int(text[i][0]),int(text[i][1]) * 10 + int(text[i][2])])
        else:#daca nu am un sir mai mare de 2 atunci pot sa despart usor cele doua cifre
            coor.append([int(text[i][0]),int(text[i][1])])
    return coor#returnez o lista de liste in care voi avea [[i0,j0],[i1,j1],[i2,j2],...]

def cifrareNihilist(key,textClar):
    tClar=textToCoordonate(textClar)#transform textul clar in coordonate
    cheie=textToCoordonate(key)#transform cheia in coordonate
    for i in range(len(key),len(tClar)):#conpletez cheia pana ajunge sa fie la fel de mare ca textul clar
        cheie.append(cheie[i%(len(key))])
    textCriptat=[]
    for i in range(0,len(tClar)):
        suma=[]
        suma.append(tClar[i][0]+cheie[i][0])
        suma.append(tClar[i][1] + cheie[i][1])
        textCriptat.append(suma)#contruiesc textul criptat prin suma coordonatelor celor doua texte
    return textCriptat
def descifrareNihilist(key,textCifrat):#primeste cheia si o lista de cifre
    tCif=cifreToCoordonate(textCifrat)#transform textul cifrat in lista de coordonate
    cheie=textToCoordonate(key)#transform cheia in coordonate
    for i in range(len(key),len(tCif)):#conpletez cheia pana ajunge sa fie la fel de mare ca textul clar
        cheie.append(cheie[i%(len(key))])
    textDecriptat=''#incep sa construiesc textul decriptat
    for i in range(0,len(tCif)):
        scadere=[]
        scadere.append(tCif[i][0]-cheie[i][0])
        scadere.append(tCif[i][1]-cheie[i][1])
        textDecriptat+=coordonataToLitera(scadere)#contruiesc textul decriptat prin scaderea coordonatelor celor doua texte
    return textDecriptat


def coordonataToLitera(coordonata):
    adresa=(coordonata[0]-1)*5+(coordonata[1]-1)
    a=patratPolybius[adresa]
    return a

def textToCoordonateVector(text):#sa imi intoarca un vector cu coordonate nu o lista de liste, pentru usurinta
    nou_text=[]
    for i in range(0,len(text)):
        nou_text.append(literaToCoordonata(text[i])[0])
        nou_text.append(literaToCoordonata(text[i])[1])
    return nou_text

def cifrareBifid(textClar):#primeste textul clar
    tClar=textToCoordonate(textClar)#transforma textul clar in coordonate din patratu polybius
    textCodat=[]#ca sa retin pozitile in el
    textCriptat=''#ca sa construiesc textul criptat
    for i in range(0,len(tClar)):
        textCodat.append(tClar[i][0])
    for i in range(0,len(tClar)):
        textCodat.append(tClar[i][1])
    for i in range(0, len(textCodat),2):#in punctu asta textCodat este un vector cu toate cordonatele
        textCriptat+=coordonataToLitera([textCodat[i],textCodat[i+1]])
    return textCriptat
def descifrareBifid(textCifrat):#primeste textul cifrat
    tCif=textToCoordonateVector(textCifrat)#am folosit o functie care imi returneaza un vector de coordonate nu o lista de liste. Este mai usor de folosit.
    textCodat=[]
    textDecriptat=''
    for i in range(0,len(textCifrat)):
        textCodat.append([tCif[i],tCif[i+len(textCifrat)]])#construiesc lista de liste in care retin coordonatele
    for i in range(0,len(textCodat)):
        textDecriptat+=coordonataToLitera(textCodat[i])#transform din coordonate in litere si returnez textul decriptat
    return textDecriptat

def Cripteaza(cheiepatratBif,cheiepatratNih,cheieSecreta):#primeste ca arugmente cele 3 chei
    global patratPolybius
    f = open("Input.txt", "r")
    text_clar = f.read().lower()#citeste textul clar
    f.close()
    text_clar = text_clar.translate({ord(i): None for i in ' .,?!;:'})  # scap de semne de punctuatie
    text_clar = text_clar.replace('\n', '')  # elimin si '\n'
    patratPolybius = patrat_polybius(cheiepatratBif)#construiesc patratul polybius pentru Bifid
    criptatBifid = cifrareBifid(text_clar)#cifrez cu Bifid
    f = open("CriptatBifid.txt", "w")
    f.write(criptatBifid)#Scriu intr-un fisier textul cifrat cu Bifid
    f.close()

    patratPolybius = patrat_polybius(cheiepatratNih)#inlocuiesc patratul cu cel construit cu cheia pentru Nihilist
    criptatNihilist = cifrareNihilist(cheieSecreta, criptatBifid)  # criptarea sub forma de lista de liste
    f = open("CriptatFinal.txt", "w")
    text = ''  # construiesc un text ca sa scriu intr-un fisier textul criptat cu nihilist
    for i in range(0, len(criptatNihilist)):
        text += str(criptatNihilist[i][0])
        text += str(criptatNihilist[i][1])
        text += ' '
    f.write(text)#Scriu textul intr-un fisier
    f.close()
    f = open("Output.txt", "w")
    f.write(text)  # Scriu textul infisieru de output
    f.close()
    return text

def Decripteaza(cheiepatratBif,cheiepatratNih,cheieSecreta):
    global patratPolybius
    f = open("Input.txt", "r")#citeste din fisierul in care am pus textul dupa criptare
    inputNih = f.read()
    f.close()
    inputNih = inputNih.split(" ")#scap de spatiile dintre coordonate
    inputNih.pop()#splitul salva un element in plus '' pe care l-am eliminat cu pop
    patratPolybius = patrat_polybius(cheiepatratNih)#construiesc patratul polybius cu cheia pentru Nihilist
    descifrare = descifrareNihilist(cheieSecreta, inputNih)#Descifrez cu Nihilist
    f = open("DecriptatNihilist.txt", "w")
    f.write(descifrare)#Scriu textul decriptat doar cu Nihilist
    f.close()
    patratPolybius = patrat_polybius(cheiepatratBif)#construiesc patratul cu cheia pentru Bifid
    descifrare1 = descifrareBifid(descifrare)#descifrez cu Bifid
    f = open("DecriptatFinal.txt", "w")
    f.write(descifrare1)#Scriu intr-un fisier textul final descifrat
    f.close()
    f = open("Output.txt", "w")
    f.write(descifrare1)  # Scriu textul infisieru de output
    f.close()
    return descifrare1


alfabet="ABCDEFGHIKLMNOPQRSTUVWXYZ"
alfabet=alfabet.lower()



while 1:
    msg ="Alegeti acitunea pe care doriti sa o faceti.\nNu uitati sa puneti in Input.txt textul corespunzator alegerii."
    title = "Proiect"
    choices = ["Cripteaza", "Decripteaza"]#cele 2 variante
    choice = choicebox(msg, title, choices)#choice are salvat in el ce a ales useru
    if choice is None:#in caz ca s-a inchis fereastra sa se inchida si programu
        sys.exit(0)

    msg = "Introduceti cheile necesare"
    fields = ["Cheie pentru algortimul Bifid", "Cheie pentru algoritmul Nihilist", "Cheie pentru cifrare"]
    chei = []#voi retine cheile introduse in interfata in aceasta variabila
    chei = multenterbox(msg, title, fields)
    while 1:#daca este o casuta lasata goala va da un mesaj
        if chei == None:
            sys.exit(0)#in caz ca s-a inchis fereastra se inchide programu
        errmsg = ""
        for i in range(len(fields)):
            if chei[i].strip() == "":#daca este o casuta goala se va aduga in mesaju de eroare
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fields[i])
        if errmsg == "": break  # daca mesaju de eroare este gol inseamna ca toate casutele au fost completate si se paote iesi din while
        chei = multenterbox(errmsg, title, fields, chei)#daca s-a gasit un mesaj de eroare se va redeschide fereastra initiala in care pastrez parametrii deja introdusi si afisez mesaju de eroare

    chei[0]= chei[0].translate({ord(i): None for i in ' .,?!;:1234567890-=+_`'})#eliminm caracterele speciale din cheile introduse in caz ca au fost introduse
    chei[1] = chei[1].translate({ord(i): None for i in ' .,?!;:1234567890-=+_`'})
    chei[2] = chei[2].translate({ord(i): None for i in ' .,?!;:1234567890-=+_`'})

    if(choice=="Cripteaza"):
        msg=Cripteaza(chei[0].lower(), chei[1].lower(), chei[2].lower())
    else:
        msg=Decripteaza(chei[0].lower(), chei[1].lower(), chei[2].lower())
    verif=msgbox(msg,title)#afisez rezultatul criptarii sau decriptarii
    if verif is None:#daca s-a inchis fereastra se iese din program
        sys.exit(0)