#from connexionboitemail import readEmails
#from connexionboitemailparts import readEmailsPart
from returnmails import returnEmails
from savemailstojson import save_email_to_file
#readEmails()
#readEmailsPart()

emails = returnEmails()

if emails:
    save_email_to_file(emails, "codes/mails.json")