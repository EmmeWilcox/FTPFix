##FTP ANALYSIS by Grayson Wilcox
##Wilcox.g8@gmail.com
##Written 8-16-16
import hashlib
import smtplib
import sys
from glob import glob
from email.mime.text import MIMEText
import email.utils

##This method grabs a file from the ftp server. It should be the same file.
def checkHash(baseFile, outFile):
    trueBaseFile = open((baseFile),"rb")
    trueOutFile = open(outFile,"rb")
    baseHash = hashlib.md5((trueBaseFile.read())).hexdigest()
    outHash = hashlib.md5((trueOutFile.read())).hexdigest()
    return (baseHash == outHash)

##Probably outdated but is for finding the file name.
def pathToName(pathObj):
    retBuf = ''
    for i in range(0,len(pathObj)):
        if not pathObj[i] == '\\':
            retBuf = retBuf + pathObj[i]
        else:
            retBuf = ''
    return retBuf        


####This method sends the email.
def sendEmail(myResult, fileName):
    if(myResult):
        ##Sets the text
        msg = MIMEText("Hello,\nThis is a notification that the file " + fileName +
                       " has been uploaded successfully")
        msg['To'] = email.utils.formataddr(("Recipient","xxxxxxxxxxxxxxxxxx"))
        msg['From'] = email.utils.formataddr(("Autoconfirm","xxxxxxxxxxxxxxxxxx"))
        msg['Subject'] = "File successfully uploaded"
        server = smtplib.SMTP("xxxxxxxxxxxxxxxxxxxxxxxxxxx")

        ##Gets the email addresses
        try:
            text_file = open('FTP_Email.txt')
            lines = text_file.read().split('\n')
        except:
            print "Missing email doc"
            sys.exit()

        ##Literally sends it. Expect breakage
        try:
            server.starttls()
            server.ehlo()
            server.login('xxxxxxxxxxxxxxxx','xxxxxxxxxxxxxx')
            server.sendmail('xxxxxxxxxxxxxxxxxxxxxxxx',
                            lines,msg.as_string())
            print "Email sent"
        except:
            print "ERROR OCCURS"
            sys.exit()
        finally:
            server.quit()
    else:
        print "Something went wrong"

####main
baseFiles = []
outFiles = []
outFileNames = []
hashes = []
result = True

##For use with multiple files
for filename in glob(sys.argv[1]):
    baseFiles.append(filename)
for filename in glob(sys.argv[2]):
    outFiles.append(filename)
    outFileNames.append(pathToName(filename))

##Quick length check
if not len(baseFiles) == len(outFiles):
    print "Process failed"
    sys.exit()

##Hash check
for i in range(0,len(baseFiles)):
    hashes.append(checkHash(baseFiles[i],outFiles[i]))
##Ensures a working determination
for truth in hashes:
    result = result and truth
##Sends final result
sendEmail(result, sys.argv[1])


