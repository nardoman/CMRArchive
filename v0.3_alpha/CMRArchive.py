
   ###############################################
   ####### Versione 0.3 alpha di CMRArchive ######
   #######   by Giulio Nardini (@cgiulina)  ######
   ###############################################
   ###############################################
   #######         Librerie richieste:      ######
   #######             pytesseract          ######       
   #######               Image              ######
   #######                csv               ######
   ###############################################
   ###############################################

import pytesseract as pt
import os
import csv
import shutil
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from PIL import Image

################ FUNZIONI PER IL PROGRAMMA ################### 

##############################################################
#    FUNZIONE CHE VERIFICA SE (py)TESSERACT è INSTALLATO     #
##############################################################

def IsTess():

    User = os.getcwd()[9:] #TROVO IL PERCORSO DEL FILE
    
    User = User[:User.find("\\")] #TROVO IL NOME UTENTE
    
    TessPath = r'C:\Users\XXXXXX\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' #SCRIVO IL PERCORSO DI DEFAULT DI TESSERACT

    TessPath = TessPath.replace("XXXXXX", User) #SOSTITUISCO IL NOME UTENTE PER OTTENERE IL PERCORSO PERSONALE
    
    try:
        
        pt.pytesseract.tesseract_cmd = TessPath #percorso di default di Tesseract, in futuro devo dare l'opzione per impostare il percorso

        return True
    
    except:

        input ("Installa TESSERACT prima di procedere! Leggi il file README prima di riprovare")
        
        return False
    
        
##############################################################
#       FUNZIONE CHE VERIFICA SE IL VRID ESISTE IN FMC       #
##############################################################

def verifica(VRID, dizVRID):

    token = False   
    
    if VRID in dizVRID:                                              
 
        print (f"\nVRID {VRID} presente in FMC, rinomino il file!")

        token = True
              
    else:

        print (f"\nVRID {VRID} non presente in FMC, possibile errore di OCR. File spostato nella cartella \"Da verificare\"")
    return token

##############################################################
#FUNZIONE CHE GENERA IL DIZIONARIO DEI VRID A PARTIRE DA FMC #
##############################################################

def creaDizVRID(csvFMC): 
    
    dizVRID = dict()
    
    with open(csvFMC, newline='') as csvfile:

        csvFMC = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
        
        for row in csvFMC[1:]: #per escludere la prima riga con le intestazioni
            VRID = row[2]
            mm = row[17][:2]
            dd = row[17][3:5]
            yyyy = row[17][6:10]

            dizVRID[VRID] = (str(yyyy), str(mm), str(dd))

    return dizVRID

##############################################################
#FUNZIONE DI OCR CHE LEGGE L'IMMAGINE E LA TRASFORMA IN TESTO#
##############################################################

def ocr(folder): 

    totalSize = 0                       #Peso totale dei file elaborati
    totalCMR = 0                        #Numero totale di file trattati
    totalFile = len(os.listdir(folder)) #numero totale di file presenti in cartella

    print (f"\nTrovati {totalFile} file(s), inizio la scansione OCR...")

    index = 1
    
    for el in os.listdir(folder):                              #per ogni file in cartella
        
        if not os.path.isdir(f"{folder}/{el}") :               #se è un file

            im = Image.open(f"{folder}/{el}")                  #aprilo come immagine
              
            VRID = pt.image_to_string(im)                      #uso pytesseract per estrarre il testo
            print (VRID)
            if not VRID.find("Dock/Trailer")+1:  #necessario perchè spesso è la prima lettera, quindi restituisce 0
                
                VRID = VRID[VRID.find("VRID"):VRID.find("VRID")+18]    #Trovo il VRID ed estraggo una sottostringa
                VRID = VRID[VRID.find("1"):VRID.find("1")+8]           #Incontro il primo 1 e da li estraggo il VRID

                totalSize += os.path.getsize(f"{folder}\{el}")     #Aggiungo il peso in bytes al totale
                totalCMR += 1                                      #Aggiungo 1 al numero di file elaborati


                if VRID == "":
                   VRID = str(index + 1)

                os.rename(f"{folder}\{el}", f"{folder}\{VRID}.png") #rinomino il file con il VRID
                                    
                if verifica (VRID, dizVRID):
                    if os.path.exists(f"{folder}\{dizVRID[VRID][0]}\{dizVRID[VRID][1]}\{dizVRID[VRID][2]}"):
                       pass
                    else:
                       os.makedirs(f"{folder}\{dizVRID[VRID][0]}\{dizVRID[VRID][1]}\{dizVRID[VRID][2]}")
                       
                    shutil.move(f"{folder}\{VRID}.png", f"{folder}\{dizVRID[VRID][0]}\{dizVRID[VRID][1]}\{dizVRID[VRID][2]}")

                else:
                    if os.path.exists(f"{folder}\DA VERIFICARE"):
                       pass
                    else:
                       os.makedirs(f"{folder}\DA VERIFICARE")
                    
                    shutil.move(f"{folder}\{VRID}.png", f"{folder}\DA VERIFICARE\{VRID}.png")
            
            else:
                if os.path.exists(f"{folder}\PROBABILI TDR CARTACEE"):
                       pass
                else:
                    os.makedirs(f"{folder}\PROBABILI TDR CARTACEE")
                shutil.move(f"{folder}/{el}", f"{folder}\PROBABILI TDR CARTACEE\{el}")
         
    print (f"\n\nSono stati elaborati {totalCMR} file(s) su un totale di {totalFile}, per {totalSize/1000000} Mb")

##############################################################
#####   FUNZIONE DI ORGANIZZAZIONE DEI FILE GIà NOMINATI #####
##############################################################

def org(folder): 

    index = 1
    
    for el in os.listdir(folder):                #per ogni file in cartella
        
        if not os.path.isdir(f"{folder}/{el}") : #se è un file
  
            VRID = el[:-4]                       #trovo il VRID eliminando l'estensione
            print (VRID)

            if verifica (VRID, dizVRID):
                if os.path.exists(f"{folder}\{dizVRID[VRID][0]}\{dizVRID[VRID][1]}\{dizVRID[VRID][2]}"):
                   pass
                else:
                   os.makedirs(f"{folder}\{dizVRID[VRID][0]}\{dizVRID[VRID][1]}\{dizVRID[VRID][2]}")
                   
                shutil.move(f"{folder}\{VRID}.png", f"{folder}\{dizVRID[VRID][0]}\{dizVRID[VRID][1]}\{dizVRID[VRID][2]}")

            else:
                if os.path.exists(f"{folder}\DA VERIFICARE"):
                   pass
                else:
                   os.makedirs(f"{folder}\DA VERIFICARE")
                
                shutil.move(f"{folder}\{VRID}.png", f"{folder}\DA VERIFICARE\{VRID}.png")

         
    input (f"\n\nSono stati elaborati tutti i file!")

##############################################################

###################### INIZIO CODICE  ########################
    
print ("----- BENVENUTO IN CMRArchive v1.0 alpha ----- \n\n") #header del programma

Mod = input ("""Il software presenta 2 modalità:\n
1. SCANSIONE E ARCHIVIAZIONE DI CMR (da utilizzare per rinominare e archiviare i CMR automaticamente)\n
2. ARCHIVIAZIONE DI CMR (già rinominati e in cartella pronti per essere archiviati

Seleziona la modalità di utilizzo del software per procedere:\n""")

if Mod == "1":

    Tvalue = IsTess()

    if Tvalue == True:   #Se Tesseract è installato True, altrimenti in futuro lancio il download in automatico
    
        folder = path = askdirectory(title='\nSeleziona la cartella delle scansioni dei CMR: \n') #inserimento del percorso in cui ci sono le scansioni
            
        csvFMC = filedialog.askopenfilename(title="Seleziona il csv ottenuto da FMC", filetypes=(("Comma separated Values","*.csv"), ("all files","*.*")))                                                   #inserimento del percorso in cui è presente il csv ottenuto da FMC 
       
        dizVRID = creaDizVRID (csvFMC)    #genera un dizionario sulla base del documento scaricato da FMC
        
        ocr(folder)                       #lancia la funzione principale del programma

        input("Chiudi il programma premendo qualsiasi tasto. Grazie per aver utilizzato CMRArchive! ")
        
    else:
       
        "Scarica Tesseract dal sito ------------"
 
elif Mod == "2":

    folder = path = askdirectory(title='\nSeleziona la cartella delle scansioni dei CMR: \n') #inserimento del percorso in cui ci sono le scansioni

    csvFMC = filedialog.askopenfilename(title="Seleziona il csv ottenuto da FMC", filetypes=(("Comma separated Values","*.csv"), ("all files","*.*")))                                                   #inserimento del percorso in cui è presente il csv ottenuto da FMC 

    dizVRID = creaDizVRID (csvFMC)   #genera un dizionario sulla base del documento scaricato da FMC
    
    org(folder)
    
else:
    input ("MODALITA' NON RICONOSCIUTA! RIAVVIA CMRArchive PER RICOMINCIARE")
    

