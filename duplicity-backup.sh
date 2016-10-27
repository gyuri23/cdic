/usr/bin/mysqldump -u root -pxxxxxx --single-transaction --opt -R dbname -r /var/tmp/backup.sql

duplicity -v0\
 --no-print-statistics\
 --no-encryption\
 --archive-dir /var/cache/duplicity\
 --volsize 500\
 --asynchronous-upload\
 --full-if-older-than 30D\
 /var/www/html rsync://user:password@192.168.x.x::/backup/bdweb1/www

duplicity -v0\
 --no-print-statistics\
 --no-encryption\
 --archive-dir /var/cache/duplicity\
 --volsize 500\
 --asynchronous-upload\
 --full-if-older-than 30D\
 /var/tmp/ rsync://user:password@192.168.x.x::/backup/bdweb1/mysql

rm /var/tmp/bandur.sql

duplicity remove-all-but-n-full 2\
 --archive-dir /var/cache/duplicity\
 --force\
 rsync://user:password@192.168.x.x::/backup/bdweb1/www

duplicity remove-all-but-n-full 2\
 --archive-dir /var/cache/duplicity\
 --force\
 rsync://user:password@192.168.x.x::/backup/bdweb1/mysql

duplicity collection-status rsync://user:password@192.168.x.x::/backup/bdweb1/www > /var/lib/backup/result.txt
duplicity collection-status rsync://user:password@192.168.x.x::/backup/bdweb1/mysql >> /var/lib/backup/result.txt
python /var/lib/backup/backupriport.py
