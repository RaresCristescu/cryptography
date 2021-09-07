import sys
import random
from easygui import *

# ####################################################################################################
# #   Am implementat Blum Blum Shub
# #   Programu primeste in GUI ca input dimensiunea dorita ( in MB ) pentru generarea numarului,si scrie in fisierul output.txt forma sa in baza 2.
# #   Pentru valoarea introdusa 2 dureaza jumatate de minut sa genereze numarul,posibil sa dureze mai mult
# ###################################################################################################

def primM(n):#incerc sa gasesc un prim mare de n biti
    incercare = random.getrandbits(int(n)) | 1  # construiesc un numar cu n biti random. de care ma asigur ca e impar prin | 1 (cresc sansele sa fie prim)
    prob = 0
    while True:
        prob = testPrim(incercare)#verific cat de probabil este ca "incercare" sa fie prime
        if prob > 0:#daca probabilitate e mai mare de 0 returnez canditatu
            return incercare
        incercare += 2#daca nu este il cresc cu 2 pana gasesc un numar impar probabil prim


def testPrim(n): #testez probabilitatea ca n sa fie prim folosind Miller-Rabin

    if n <= 1:#daca e mai mic ca 1 sigur nu e prim
        return 0

    bases = [random.randrange(2, n) for x in range(100)]#umple bases cu 100 de numere random mai mici ca n
    for b in bases:
        if n % b == 0:#daca n se imparte la un element din bases atunci n nu e prim
            return 0

    s = 0
    m = n - 1#consider forma lui n find n=1+(2^s)*m
    #incep sa construiesc elementele pentru forma lui n
    while not m & 1:  # cat timp m este par il impart la 2
        m >>= 1#round(m/2)
        s += 1#numarul de impartiri la 2

    for b in bases:#pentru fiecare element din bases
        pPrim = algP(m, s, b, n)#verific daca n este prim folosind elementul din bases
        if pPrim==0:#daca gasesc macar un exemplu pt care nu este prim returnez 0
            return 0

    if pPrim:#daca este prim returnez 1
        return 1
    return 0


def algP(m, s, x, n):# Algorithm P din Art of Computer Programming vol. 2 pag. 395

    y = pow(x, m, n)#(b^m)%n

    for j in range(s):
        if (y == 1 and j == 0) or (y == n - 1):#daca y=1 si j=0 sau y=n-1 atunci n este probabil prim
            return 1
        y = pow(y, 2, n)#(y^2)%n
    return 0


def getPrime(biti):#generez un numar prim mare cu conditia p%4=3
    while True:
        p =primM(biti)
        if p % 4 == 3:
            return p

def genereazaN(biti):#genereaza N=p*q, unde p si q sunt prime mari

    p = getPrime(biti / 2)
    while True:
        q = getPrime(biti / 2)
        if p != q:
            return p * q



def BlumBulmShub(numBiti):#primeste ca data de intrare numarul de biti dorit pentru generarea numarului si returneaza numarul generat sub forma de biti

    n = genereazaN(32)#generez un N mare de 32 de biti
    seed = random.getrandbits(31)#construiesc un seed cu 31 de biti random
    x= seed % n#ca sa fie coprim sigur
    bits=''
    for i in range(numBiti):
        x = (x*x) % n
        bits+=str(x%2)
    return bits




fisier = open("output.txt", "wb")#pentru scrierea in fisier binar a numarului
while True:
    title = "Proiect 2"
    msg ="Introduceti dimensiunea in MB\n(Dupa ce termina de calculat programu va deschide o fereastra sa confirme generarea)"
    val=enterbox(msg,title)
    if val is None:#daca s-a inchis fereastra se iese din program
        sys.exit(0)
    val=float(val)
    val=val*8000000#programu are nevoie de biti,transform  1 MB = 8 Mb = 8*1000000 biti
    a = BlumBulmShub(int(val))
    text=a.encode()#transfrom din stirng in binar
    fisier.write(text)#scrierea in fisier
    fisier.close()
    numar=int(a,base=2)#forma in baza 10 a numarului
    msg = "Numarul a fost generat si scris in 'output.txt' cu succes!\n"
    msgbox(msg,title)
    sys.exit(0)