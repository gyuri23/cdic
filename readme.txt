--------------------
Időzétés és példák |
--------------------------------------------------------------------------------------------------

Mentés script itt van:  /var/lib/backup/duplicity-backup.sh
Időzítés megnézése:     crontab -l
Időzítés szerkesztése:  crontab -e

Mentések állapota:      duplicity collection-status rsync://username:password@192.168.x.x::/backup/folder

Keresés a mentésben:    duplicity list-current-files rsync://username:password@192.168.x.x::/backup/folder | egrep 'Jan  4 10.*username.*cur'

Visszaállítás:          duplicity --no-encryption -t 1D --file-to-restore var/vmail/foldername/user.name/Maildir/.user/cur/1451900101.M380766P46633.zentyal,S=521444,W=528340:2,Sabc username:password@192.168.x.x::/backup/folder /home/foldername/test.txt

Viszaállított levél:    head -50 /var/vmail/foldername/username/Maildir/.Sent/cur/1451900079.M690485P26762.zentyal\,S\=14302283\,W\=14498365\:2\,S


--------
Mentés |
-------------------------------------------------------------------------------------------------

Alap titkosítás nélkül:         duplicity --no-encryption /home/user/Teszt/Work file:///home/user/Teszt/Backup
Megadodd időnként full mentés:  duplicity --full-if-older-than 1M /home/me sftp://uid@other.host/some_dir


----------------------------------
Keresés fájlra a mentések között |
-------------------------------------------------------------------------------------------------

1. duplicity collection-status
2. duplicity list-current-files -t [idő] | grep fájlnév

pl. duplicity collection-status rsync://username:password@192.168.x.x::/backup/folder

Egy fájl keresése, az utolsó mentésre:  duplicity list-current-files file:///home/username/Backup | grep cript.txt
Fájl keresés megadott időpontra (-t):   duplicity list-current-files -t 1D file:///home/username/Teszt/Backup

Reguláris keresés:  duplicity list-current-files rsync://username:password@192.168.x.x::/backup/folder | egrep 'Jan  4 10.*robert.*cur'
# A dátumnál ha 1 karakter a nap akkor 2 szóköz kell

Elérhető mentések:  duplicity collection-status file:///home/username/Teszt/Backup
                    duplicity collection-status rsync://username:password@192.168.x.x::/backup/folder


---------------
Visszaállítás |
-------------------------------------------------------------------------------------------------

Komplett mappa vissza:          duplicity --no-encryption file:///home/username/Teszt/Backup /home/username/Teszt/Work
Egy file megadott időpontban:   duplicity --no-encryption -t 1D --file-to-restore fájl.txt file:///home/username/Teszt/Backup /home/username/Teszt/fájl.txt
                                duplicity --no-encryption -t 1D --file-to-restore var/vmail/foldername/username/Maildir/.user/cur/1451900101.M380766P46633.zentyal,S=521444,W=528340:2,Sabc rsync://username:password@192.168.x.x::/backup/folder /home/admin/Letöltések/test.txt

--------------------------------------------------
Levélbe nézés (visszállítás után, vagy a helyén) |
--------------------------------------------------------------------------------------------------

Levél megnézés:     head -50 /var/vmail/foldername/username/Maildir/.Sent/cur/1451900079.M690485P26762.zentyal\,S\=14302283\,W\=14498365\:2\,S
