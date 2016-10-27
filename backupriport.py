#!/usr/bin/python

import smtplib

f = open('/var/lib/backup/result.txt', 'r')
backup_result = f.read()
f.close()

message = """From: servername <servername@company.hu>
To: Riport <riport@domain.hu>
Subject: duplicity backup -- comopany -- server
""" + backup_result

mail = smtplib.SMTP('192.168.x.x',587)
mail.ehlo()
mail.starttls()
mail.login('riport@company.hu','password')
mail.sendmail('riport@company.hu','riport@domain.hu',message)
mail.close()
