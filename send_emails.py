#!/usr/bin/env python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication
from optparse import OptionParser
import os
import unicodedata
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')



def MIMESETUP(flags,receiver,subject,base_email,attachment):
    '''Mime config'''

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = flags.sender
    message['To'] = receiver
    message['Cc'] = flags.sender
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
    session = smtplib.SMTP('smtp.cern.ch', 587) #use gmail with port
    session.starttls() #enable security
    session.login(flags.sender, flags.pwd) #login with mail_id and password
    text = message.as_string()
    session.sendmail(flags.sender, [message['To'], message['Cc']], text)
    session.quit()
    print('Mail sent to {}\n'.format(message['To']))


# take one line from students.csv. For each, check if a file with this XXX.YYY exists (without @zzz.AA, because some students have ethz addresses)
# if such a corresponding file exists, return the entire filename and the complete mailaddress
def get_hw_and_address_from_line(line, hwfolder, filename_must_contain_any_of=None):
    address_full = line.split(',')[3].lower()
    address_firstpart = address_full.split('@')[0]

    # look for address_firstpart in content of folder
    files_in_folder = os.listdir(hwfolder)
    correctfile = None
    for f in files_in_folder:
        if address_firstpart in f.lower():
            if filename_must_contain_any_of is not None:
                for part in filename_must_contain_any_of:
                    if part in f:
                        if correctfile is None:
                            correctfile = f
                        else:
                            raise ValueError('For address there seem to be multiple matching files, \'%s\' and \'%s\'' % (correctfile, f))
            else:
                if correctfile is None:
                    correctfile = f
                else:
                    raise ValueError('For address there seem to be multiple matching files, \'%s\' and \'%s\'' % (correctfile, f))
                break

    if correctfile is None:
        print 'Did not find a file for address %s' % (address_full)
        return (None, None)
    else:
        print 'Nice, found this file for address %s: %s' % (address_full, correctfile)
        return (address_full, os.path.join(hwfolder, correctfile))




def GetStudentInfo(HW,studentlist='students.csv'):

    # takes number of HW and filename of studentlist in csv format
    # returns tuple of: (list of tuples with addresses and corresponding files, list of all files [for bookkeeping])

    addresses_and_filenames = []
    hwfolder = 'Sheet%02i' % (HW)
    with open(studentlist, 'r') as f:
        lines = f.readlines()
        for line in lines:
            addresses_and_filenames.append(get_hw_and_address_from_line(line=line, hwfolder=hwfolder, filename_must_contain_any_of=['Sheet%02i' % (HW), 'sheet%02i' % (HW)]))

    return addresses_and_filenames, [os.path.join(hwfolder, f) for f in os.listdir(hwfolder)]


    # students={}
    # with codecs.open(names,'r', encoding="utf-8") as f:
    #     lines = f.readlines()
    #     for line in lines:
            # line = line.strip('\n')
            # name = line.split(',')[1]
            # surname = line.split(',')[2]



            # def GetFile(name,surname,HW):
            #     homeworks = os.listdir("Sheet%02i"%(HW))
            #     if name.split(" ")[-1] != name:
            #         name = name.split(" ")[-1]
            #     if surname.split(" ")[-1] != surname:
            #         surname = surname.split(" ")[-1]
            #     for homework in homeworks:
            #         if name.lower().decode('UTF-8') in homework.lower() and surname.lower().decode('UTF-8') in homework.lower(): #TODO: implement accent support
            #
            #             print("-- Nice, student '{} {}' handed in the homework".format(name, surname))
            #             return os.path.join("sheet%02i"%(HW),homework)

                # print("Student '{} {}' didn't hand the homework".format(name, surname))
                # return None

            # if GetFile(name,surname,HW) != None:
            #     students["{} {}".format(name,surname)] = {'email':line.split(',')[3],'file':GetFile(name,surname,HW)}
    # return students



def SendEmails(flags):
    ''' Send emails with attachments '''
    (addresses_and_filenames, allfiles)  = GetStudentInfo(flags.HW)

    subject = 'PHY211 sheet {} results'.format(flags.HW)
    addresses_used = []
    files_used = []
    for (address, filename) in addresses_and_filenames:
    # for name in names:
        base_email = '''Hi,

Attached you can find your marked solutions for sheet {}.

Cheers,
Kyle & Arne
        '''.format(flags.HW)
        #print(base_email)

        # print("File: {}: \nEmail: {} \n".format(names[name]['file'],names[name]['email']))
        # print names[name]['email']

        if filename is not None:
            if address in addresses_used:
                raise ValueError('Trying to send to address %s, but it already appeared before... duplicate entry in CSV?')
            addresses_used.append(address)
            files_used.append(filename)
            print 'Sending: %s --> %s' % (filename, address)
            if flags.send:

                msg = MIMESETUP(flags=flags,receiver=address,subject=subject,base_email=base_email,attachment=filename)
                CreateSession(flags,msg)
    print 'Sent %i mails' % (len(addresses_used))
    files_not_used = [f for f in allfiles if f not in files_used]
    if len(files_not_used) > 0:
        print '\n\n--> WARNING: Not all files in the folder have been sent (%i leftover), some maybe named badly? Here they are:' % (len(files_not_used))
    for f in files_not_used:
        print ' ', f

def RemoveSpecialCharacters(string):
    return "".join(e for e in string if e.isalnum())




if __name__=='__main__':
    parser = OptionParser(usage="%prog [opt]  inputFiles")
    parser.add_option("--HW", type=int, default=7, help="Specify the homework number")
    parser.add_option("--sender", type="string", default="your_email@uzh.ch", help="Specify the sender's email")
    parser.add_option("--pwd", type="string", default="", help="Specify the sender's password")
    parser.add_option("--send", action="store_true", default=False, help="Send the emails.")
    (flags, args) = parser.parse_args()
    SendEmails(flags)
