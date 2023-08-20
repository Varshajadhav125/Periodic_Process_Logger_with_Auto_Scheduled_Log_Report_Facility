#process log with periodic mail sending facility.
import os
import psutil
import time
import csv
import pandas as pd
import numpy as np
#import urllib2
from datetime import datetime
import xlsxwriter
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
def is_connected():
    try:
        urllib2.urlopen('https://mail.google.com/mail/',timeout=3)
        return True
    except urllib2.URLError as err:
        return False

def MailSender(filename,time):
    try:
        fromaddr = "vcjadhav125@gmail.com"
        toaddr = "vjadhavc1@gmail.com"

        msg =MIMEMultipart()

        msg['From'] = fromaddr

        msg['To'] = toaddr

        body = """
        Hello %s,0
        Welcome to Marvellous Infosystems.
        Please find attached document which contain log of running process.
        Log file is created at : %s
        
        This is auto generated mail.
        
        Thanks & Regards,
        Varsha Chandrakant Jadhav
        Marvellous Infosystems
         """%(toaddr,time)


        Subject = """
        
        Marvellous Infosystems Process log generated at : %s
        """%(time)

        msg['Subject'] = Subject

        msg.attach(MIMEText(body,'plain'))

        attachment = open(filename,"rb")

        p = MIMEBase('application','octal-stream')

        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Content-Disposition',"attachment; filename= %s" % filename)

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com',587)

        s.starttls()

        s.login(fromaddr,"hyhmvpequthvbabe")

        text = msg.as_string()

        s.sendmail(fromaddr,toaddr,text)

        s.quit()

        print("Log file successfully send through Mail")

    except Exception as E:
        print("Unable6 to send mail.",E)


def ProcessLog(log_dir = "Marvellous"):
    print("START PROCESS")
    listprocess = []

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
    log_path = os.path.join(log_dir + f"/MarvellousLog_{current_date}.csv")
    # log_path = os.path.join(log_dir, "MarvellousLog%s.log")

    with open(log_path,'w',newline='') as file:
        writer = csv.writer(file) 
    #f.write(separator + "\n")
    #f.write("Marvellous Infosystems Process Logger:"+"\n")
        writer.writerow(["Marvellous Infosystems Process Logger:" + current_date + ".log"+"\n"])
        header = ['pid','name','username','vms'] 
        writer.writerow(header)
        #writer.writerow(separator + "\n")
    #worksheet = workbook.add_worksheet()
        val=None
        for proc in psutil.process_iter():
            try:
                pinfo = (proc.as_dict(attrs=['pid','name','username']))
                vms = proc.memory_info().vms / (1024 * 1024)
                pinfo['vms'] = vms
                listprocess.append(pinfo)
                data=[pinfo['pid'],pinfo['name'],pinfo['username'],vms]
                writer.writerow(data)
            except(psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
                pass
        
    
    print("Log file is successfully generated at location %s"%(log_path))

    connected = is_connected()

    if connected:
        startTime = time.time()
        MailSender(log_path,current_date)
        endTime = time.time()

        print('Took %s Seconds to send mail'%(endTime - startTime))
    else:
        print("There is no internet connection")

def main():
    print("Marvellous infosystem by Varsha Jadhav-----")

    print("Application name: "+argv[0])

    if(len(argv)!= 2):
        print("Error : Invalid number of arguments")
        exit()

    if(argv[1] == "-h") or (argv[1] == "-H"):
        print(" This Script is used log record of running processes")
        exit()

    if(argv[1] == 'u') or (argv[1] == 'U'):
        print("usage: ApplicationName AbsolutePath_of_Directory")
        exit()

    try:
        schedule.every(int(argv[1])).minutes.do(ProcessLog)
        # schedule.every(int('5')).minutes.do(ProcessLog)
        while True:
            # print("shedule loop")
            schedule.run_pending()
            time.sleep(1)
    except ValueError as E:
        print(E)
        traceback.print_exc()
        print("Error : Invalid datatype of input")

    except Exception as E:
        traceback.print_exc()
        print("Error : Invalid input",E)

if __name__ == "__main__":
    main()