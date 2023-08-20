#Automation script which accept directory name from user and remove duplicate file from that directory.
import os
import psutil
import time
#import urllib2
from datetime import datetime
import hashlib
import urllib
import urllib.request as urllib2
import urllib.error
import urllib.parse
import smtplib
import schedule
from sys import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import traceback
#import subprocess
def is_connected():
    try:
        urllib2.urlopen('https://mail.google.com/mail/', timeout=3)
        return True
    except urllib2.URLError as err:
        return False

def MailSender(filename,time):
    try:
        fromaddr = "vcjadhav125@gmail.com"
        toaddr = "vjadhavc1@gmail.com"

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()

        msg['From'] = fromaddr

        msg['To'] = toaddr

        #make the body of the email
        body = """
        Hello %s,
        Welcome to Marvellous Infosystems.
        Please find attached document which contain log of running process.
        Log file is created at : %s

        This is auto generated mail.

        Thanks & Regards,
        Varsha Chandrakant Jadhav
        Marvellous Infosystems
         """ % (toaddr,time)

        Subject = """

        Marvellous Infosystems Process log generated at : %s
        """ % (time)

        msg['Subject'] = Subject

        #make a MIME object to define parts of the email
        msg.attach(MIMEText(body,'plain'))

        attachment = open(filename,'rb')

        p = MIMEBase('application','octet-stream')

        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # msg.attach(attachment,maintype = "application",subtype = "log",filename=filename)

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        s.login(fromaddr, "hyhmvpequthvbabe")

        text = msg.as_string()

        s.sendmail(fromaddr, toaddr, text)

        s.quit()

        print("Log file successfully send through Mail")

    except Exception as E:
        print("Unable6 to send mail.", E)

def DeleteFiles(log_dir="Marvellous"):
    listprocess = []
    arr = FindDuplicate(argv[1])
    results = list(filter(lambda x: len(x) > 1, arr.values()))

    icnt = 0

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    current_date = datetime.now()
    current_date = current_date.strftime("%Y_%m_%d_%I_%M_%S")
    print(current_date)
    separator = "-" * 80
    # variable1="hello"
    # string1=f"variable 1 : {variable1}"
    # print(string1)
    log_path = os.path.join(log_dir + f"/MarvellousLog_{current_date}.log")
    # log_path = os.path.join(log_dir, "MarvellousLog%s.log")

    f = open(log_path, 'a')
    f.write(separator + "\n")
    # f.write("Marvellous Infosystems Process Logger:"+"\n")
    f.write("Marvellous Infosystems Process Logger:" + current_date + ".log"+"\n")
    f.write(separator + "\n")
    if len(results) > 0:
        try:
            for result in results:
                for subresult in result:
                    icnt += 1
                    if icnt >= 2:   
                        os.remove(subresult)
                        f.write("The following files are removed:"+"\n")
                        listprocess.append(subresult)                
        except:
            pass
    else:
        f.write("No duplicate files found:")    

    for element in listprocess:
        f.write("%s\n"%element)
        #print(element)
    f.flush()
    f.close()

    print("Log file is successfully generated at location %s"%(log_path))

    connected = is_connected()

    if connected:
        startTime = time.time()
        MailSender(log_path,current_date)
        endTime = time.time()

        print('Took %s Seconds to send mail'%(endTime - startTime))
    else:
        print("There is no internet connection")

def hashfile(path,blocksize = 1024):
    afile = open(path,'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)

    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def FindDuplicate(path):
    
    flag = os.path.isabs(path)
    if flag == False:
        path = os.path.abspath(path)

    exists = os.path.isdir(path)
    dups = { }
    if exists:
        for dirName,subdirs,fileList in os.walk(path):
            print("Current folder is : "+dirName)
            for filen in fileList:
                path = os.path.join(dirName,filen)
                file_hash = hashfile(path)
                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]
        return dups
    else:
        print("Invalid Path")

def printresults():
    dict1=FindDuplicate(argv[1])
    results = list(filter(lambda x: len(x) > 1,dict1.values()))

    if len(results) > 0:
        print("Duplicates Found: ")
        print("The following files are duplicate")
        for result in results:
            for subresult in result:
                print('\t\t%s'%subresult)
    else:
        print("No duplicate files found.")

def main():
    print("Marvellous infosystem by Varsha Jadhav-----")

    print("Application name: "+argv[0])

    if(len(argv)!= 3):
        print("Error : Invalid number of arguments")
        exit()

    if(argv[1] == "-h") or (argv[1] == "-H"):
        print("This Script is used to traverse specific directory and delete duplicate files")
        exit()

    if(argv[1] == 'u') or (argv[1] == 'U'):
        print("usage: ApplicationName AbsolutePath_of_Directory Extension")
        exit()

    try:
        arr = { }
        startTime = time.time()
        schedule.every(int(argv[2])).minutes.do(printresults)
        schedule.every(int(argv[2])).minutes.do(DeleteFiles)
        while True:
            # print("shedule loop")
            schedule.run_pending()
            time.sleep(1)
        endTime = time.time()

        print('took %s seconds to evaluate.'%(endTime - startTime))

    except ValueError as E:
        print(E)
        traceback.print_exc()
        print("Error : Invalid datatype of input")

    except FileNotFoundError as E:
        print(E)
        traceback.print_exc()
        print("Error : Invalid datatype of input")

    except Exception as E:
        traceback.print_exc()
        print("Error : Invalid input",E)

if __name__ == "__main__":
    main()