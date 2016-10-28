#!/usr/bin/env python

# cdic.py
# 1.0 - 2016.10.18
#
# Description

import argparse
import codecs
import sys
import re
import time

start_time = time.time()
record_number = 0

# =================== Parancssori argumentumok definiálása ====================

parser = argparse.ArgumentParser(description='''Generate dictionary for a
                                 dictionary attack.''')
parser.add_argument('i', metavar='first-filename-input', type=str,
                    help='Input source file')
parser.add_argument('o', metavar='second-filename-output', type=str,
                    help="Output destination file")
parser.add_argument('-d', metavar='number',
                    help="Number of chars depth. Default = 2")
parser.add_argument('-s', metavar='filename',
                    help="Special chars source file")

args = parser.parse_args()


# ========================= Függvények definiálása ============================

# ----------------------------- Progress Bar ----------------------------------

# Print iterations progress
def print_progress(iteration, total, prefix='', suffix='', decimals=1,
                   bar_length=100):
    # Call in a loop to create terminal progress bar
    # @params:
    #     iteration   - Required  : current iteration (Int)
    #     total       - Required  : total iterations (Int)
    #     prefix      - Optional  : prefix string (Str)
    #     suffix      - Optional  : suffix string (Str)
    #     decimals    - Optional  : positive number of decimals in percent
    #                               complete (Int)
    #     barLength   - Optional  : character length of bar (Int)
    format_str = "{0:." + str(decimals) + "f}"
    percents = format_str.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(
        '\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


# ---------------------- Fájl létezését ellenőrző függvény --------------------

def existe(file_name):
    try:
        f = open(file_name, 'r')
        f.close()
        return file_name
    except IOError:
        sys.exit("Input file: " + file_name + " missing.")


# ---------------------- Elemek kiírására rekurzív függvény -------------------

def extend_word(record, repeat):
    # A szavak végéhez fűzött extended_chars.
    global extended_chars
    # Outputnak megadott fájl.
    global file_destination
    # Kiírt rekordok számolásához változó.
    global record_number
    # Ciklus ami végigpörgeti a hozzáírni kívánt karaktektereket
    for index in range(len(extended_chars)):
        # Elkészíti a kiíráshoz az aktuális elemet (szót) úgy hogy a szó
        # végéhez írja azt a karaktert aminél jár a ciklus.
        write_record = record + extended_chars[index]
        # Beleírja az out fájlba az elkészített szót és lezárja soremeléssel.
        file_destination.write(write_record + "\r\n")
        # Növeljük a kíírt rekodok számát a statisztikához.
        record_number += 1
        # Teszteléshez kiírja a végeredményt. Alapból ki van kapcsolva.
        # print(write_record)
        # Ha nem csak 1 karaktert akarunk a szavakhoz fűzni akkor újra
        # meghívjuk magát a extend_word függvényt. Ettől rekurzív :)
        if repeat > 1:
            # Átadjuk a write_record függvénynek az aktuális szót és
            # csökkentjük egyel az ismétlés számot.
            extend_word(write_record, repeat - 1)


# ================================= Előkészítés ===============================

# Input fájl megnyitása, ezt használjuk a szótár elkészítéshez
file_source = open(existe(args.i), 'r')
# Megnyitjuk az output fájlt UTF-8 kódolással, ide fogjuk írni az eredményt.
file_destination = codecs.open(args.o, 'w', 'utf-8')

# ----------------------------- Ha -d mélység paraméter -----------------------

# Ha van -d paraméter beállítjuk az értékét
if args.d:
    depth = int(args.d)
# Ha nincs beállítjuk a default 2 értéket
else:
    depth = 2

# ------------ Ha van -s külön speiális karakter fájl, feldolgozzuk -----------

# Ha van -s paraméter megnyitjuk a speciális karakterket tartalmazó fájlt és
# kiolvassuk belőle a számokhoz adandó karakterket.
if args.s:
    # Speciális karakterket tartalmazó fájl megnyitása, ezt használjuk a
    # szavak bővítéséhez
    file_special_chars = open(existe(args.s), 'r')
    # Ha van BOM kihagyjuk, úgy hogy nem pozícionálunk vissza a fájl elejére
    if b'\xef\xbb\xbf' not in file_special_chars.read(1).encode('utf-8'):
        file_special_chars.seek(0)
    # Csak az első sort használjuk, a többi nem kell.
    special_chars_input = list(file_special_chars.readline())
    # Segédváltozó a gyűjtéshez.
    special_chars = list("")
    # Feldolgozza a beolvasott sor minden egyes karakterét.
    for position, char in enumerate(special_chars_input):
        # Ha van benne sima betű, szám, vagy szóköz azt nem vesszük figyelembe.
        if not re.match(r'[0-9\n\ a-zA-Z]', char):
            # Ha megfelelő a karakter, hozzáadjuk a többihez.
            special_chars += char
    # Az extended_chars változóan lesz az "igazi" karakterek listája. Ezek
    # a számok és nem betűk.  
    extended_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                      '9'] + special_chars
    # Speciáls karakter fájl bezárása
    file_special_chars.close()
else:
    # Alapértelmezett hozzáfűzendő extended_chars a számok, ha nincs
    # külön fájl. 
    extended_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# ================================ Feldolgozás ================================

# Progress Bar számláló nullázása
progress_counter = 0
# Progress Bar ősszes sor beállítás a % számításhoz
total_line = sum(1 for line in file_source)
# Fájl lejére ugrás a számolás után
file_source.seek(0)

# Megnyitja a forrásfájlt, amit bővítni akarunk
# Ha van BOM kihagyjuk, úgy hogy nem pozícionálunk vissza a fájl elejére
if b'\xef\xbb\xbf' not in file_source.read(1).encode('utf-8'):
    file_source.seek(0)

# Initial call to print 0% progress
print_progress(progress_counter, total_line, prefix='Progress:',
               suffix='Complete', bar_length=50)
# Forrás input fájl végigolvasása soronként. A soremelesét levágjuk a végéről.
for line in file_source:
    # Aktuális sor (szó) átadása a kiíráshoz. A meghívott függvény fogja
    # rekurzívan hozzáírni a beállított karakterket.
    extend_word(line.rstrip("\n"), depth)
    # Progress Bar számláló növelése.
    progress_counter += 1
    # Progress Bar frissítése a feldolgozás alatt.
    print_progress(progress_counter, total_line, prefix='Progress:',
                   suffix='Complete', bar_length=50)

# Nyitott fájlok bezárása
file_source.close()
file_destination.close()

# =============================== Statisztikák  ===============================

print("Record number: {0:,d}".format(record_number))
seconds = time.time() - start_time
print("Running time (H:M:S): " + str(int(seconds / 3600)) + ":" +
      str(int(seconds / 60)) + ":" + str(int(seconds)))
