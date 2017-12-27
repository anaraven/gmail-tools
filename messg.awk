#!/usr/bin/awk -f
BEGIN {FS="\t" }
/^#/{next}
{
gsub(/"/,"");
print "sendemail -f \"CMB1 <andres.aravena+cmb@istanbul.edu.tr>\"", \
"-t \""$4"\" -s \"smtp.gmail.com:587\" -o tls=yes", \
"-xu \"andres.aravena@istanbul.edu.tr\" -xp \"ANJTN8R9\"", \
"-u \"Your file \\\""$5"\\\" was received\"", \
"-m \"The fingerprint is",$1". Please keep this file for your records\""
}
