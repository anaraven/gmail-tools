# gmail-tools
Tools to help on analyzing the answers of the students of "Computing in Molecular Biology"

For the "Computing in Molecular Biology" courses we evaluate what students have learned using exams in digital forms. To do this in a fair and transparent way I use an automatic process.

## Presenting the exam to the student
The questions of the exams are delivered on paper at the begin of the examination. In the text there is a link to a webpage, from where the students have to download a *template* for the answers. The answers have to be written in a *Markdown* file, an open and accessible standard. The students write their answers in the space given to them, respecting the *structure* of the template.

Once they have finished, they send their answer file attached in an email to my account at Istanbul University. The destination address includes the tag `+cmb`, that allows an automatic rule in the server to classify them in the folder of the course. They are also automatically copied to my Google Mail account. This way the answers are backed up in two systems, where the delivery date get registered in a way that cannot be modified by third parties.

## Electronic signature of answers
Immediately after the last answer has been delivered I download all the attached files in messages having the `CMB` tag that were received on the day of the exam. This is done automatically and exhaustively with the program `attach_downloader.py` that uses the official Google Mail Application Programming Interface to access my account. This program saves each attachment using a filename that is the electronic signature (MD5) of the student's answer.

Once the files have been saved (and backed up in at least two different servers), I send the registry of which electronic signatures correspond to each student to the online forum of the course. This way there is a public record (which cannot be modified) of what I received in the exam date.
Each student gets the same email at the same time, so even if the forum is not accessible, there are many copies of the registry.

In the email to the students they are encouraged to verify that the file I got is the same file they sent. This can be easily done on the website <http://onlinemd5.com/> without uploading the file. If any error is found, the students can request to correct it before the questions are graded.
