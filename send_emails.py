import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication
from optparse import OptionParser
import os



def MIMESETUP(flags,receiver,subject,base_email,attachment):
    '''Mime config'''

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = flags.sender
    message['To'] = receiver
    message['Subject'] = subject
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(base_email, 'plain'))
    
    with open(attachment, 'rb') as f: # Open the file as binary mode
        attach = MIMEApplication(f.read(),_subtype="pdf")
        
    attach.add_header('Content-Decomposition', 'attachment', filename=attachment)
    message.attach(attach)
    return message

def CreateSession(flags,message):    
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.uzh.ch', 587) #use gmail with port
    session.starttls() #enable security
    session.login(flags.sender, flags.pwd) #login with mail_id and password
    text = message.as_string()
    session.sendmail(flags.sender, message['To'], text)
    session.quit()
    print('Mail Sent to {}\n\n'.format(message['To']))

def GetStudentInfo(HW,names='students.txt'):
    ''' Find the name, email and respective homework attachment for each student.
    Returns a dictionary containing the student's name, email and corresponding pdf file
    '''
    students={}
    with open(names,'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            name = line.split('\t')[1]
            surname = line.split('\t')[0]

            def GetFile(name,surname,HW):
                homeworks = os.listdir("HW{}".format(HW))
                if name.split(" ")[-1] != name:
                    name = name.split(" ")[-1]
                if surname.split(" ")[-1] != surname:
                    surname = surname.split(" ")[-1]
                for homework in homeworks:
                    if name.lower() in homework.lower() and surname.lower() in homework.lower():
                        return os.path.join("HW{}".format(HW),homework)
                    
                print("Student '{} {}' didn't hand the homework".format(name, surname))
                return None
            
            if GetFile(name,surname,HW) != None:
                students["{} {}".format(name,surname)] = {'email':line.split('\t')[-1],'file':GetFile(name,surname,HW)}
    return students

    

def SendEmails(flags):
    ''' Send emails with attachments '''
    names  = GetStudentInfo(flags.HW)

    subject = 'HW{} results'.format(flags.HW)
    for name in names:
        base_email = '''Hello {},
In attachment is your corrected homework. Let me know in case you have questions or if the corrections do not display properly.
Cheers,
Vinicius
        '''.format(name)
        #print(base_email)

        print("Student: {} \nFile: {}: \nEmail: {} \n".format(name,names[name]['file'],names[name]['email']))
        if flags.send:
            msg = MIMESETUP(flags,names[name]['email'],subject,base_email,names[name]['file'])
            CreateSession(flags,msg)

    


if __name__=='__main__':
    parser = OptionParser(usage="%prog [opt]  inputFiles")
    parser.add_option("--HW", type=int, default=7, help="Specify the homework number")
    parser.add_option("--sender", type="string", default="your_email@uzh.ch", help="Specify the sender's email")
    parser.add_option("--pwd", type="string", default="", help="Specify the sender's password")
    parser.add_option("--send", action="store_true", default=False, help="Send the emails.")
    (flags, args) = parser.parse_args()
    SendEmails(flags)
