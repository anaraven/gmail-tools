#!/usr/bin/awk -f
BEGIN {FS="\t" }
/^#/{next}
{
gsub(/"/,"");
print "sendemail -f \""LBL" <andres.aravena+" tolower(LBL) "@istanbul.edu.tr>\"", \
"-t \""$4"\" -s \"smtp.gmail.com:587\" -o tls=yes", \
"-xu \"andres.aravena@istanbul.edu.tr\" -xp \"ivynjtyyaqqrlwgs\"", \
"-u \"Your file \\\""$5"\\\" was received\"", \
"-m \"The MD5 fingerprint of your file is "toupper($1)". Please keep this number for your records and verify that your file has the same fingerprint.\""
}
