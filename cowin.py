import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import time

class Slot(object):
    def __inti__(self):
        self.date=""
        self.hospitalName = ""
        self.city=""
        self.address=""
        self.pincode=""
        self.vaccineName = ""
        self.availableDose1 = 0
        self.availableDose2 = 0
        self.minAge=""
        self.free=0

    def __str__(self):
        str = "{0}, {1:>50}, {2:>7}, {3:>14}, {4:>14}, {5:>11}, {6:>7}, {7}, {8}".format(
            self.date,
            self.hospitalName,
            self.city,
            #self.address,
            self.pincode,
            self.vaccineName,
            self.availableDose1,
            self.availableDose2,
            self.minAge,
            self.free
        )
        return str
    def getHtmlHeader(self):
        str = "<tr> \
                    <th>{0}</th> \
                    <th>{1}</th> \
                    <th>{2}</th> \
                    <th>{3}</th> \
                    <th>{4}</th> \
                    <th>{5}</th> \
                    <th>{6}</th> \
                    <th>{7}</th> \
                    <th>{8}</th> \
                  </tr> ".format(
            "Date",
            "Hospital Name",
            "City",
            #self.address,
            "Pincode",
            "Vaccine Name",
            "Available Dose1",
            "Available Dose2",
            "Min Age",
            "Fee"
        )
        return str

    def getHtml(self):
        htmlStr = "<tr> \
                    <td>{0}</td> \
                    <td>{1}</td> \
                    <td>{2}</td> \
                    <td>{3}</td> \
                    <td>{4}</td> \
                    <td>{5}</td> \
                    <td>{6}</td> \
                    <td>{7}</td> \
                    <td>{8}</td> \
                  </tr> ".format(
                    self.date,
                    self.hospitalName,
                    self.city,
                    #self.address,
                    self.pincode,
                    self.vaccineName,
                    self.availableDose1,
                    self.availableDose2,
                    self.minAge,
                    self.free
                )  
        return htmlStr
    

class Cowin(object):
    def __init__(self):
        self._URL = "https://cdn-api.co-vin.in/"
        self._headers = {
            "host": "cdn-api.co-vin.in",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "accept": "application/json",
            "Accept-Language": "hi_IN"
        }
        self._target = ""
        self._params= {}
        self._response = {}
        self._availableFlag=False
        self._emailBody=""
        self._slots = []
    def flushEmailBody(self):
        self._emailBody=""
        self._availableFlag = False
    def getAvailabilityDistrict(self, district_id, date):
        self._target="api/v2/appointment/sessions/public/findByDistrict"
        self._params = {
            "district_id": district_id,
            "date": date
        }
        self.getReq()
        for r in self._response:
            if int(r['min_age_limit']) == 18:
                myslot = Slot()
                myslot.date = date
                myslot.hospitalName = r['name']
                myslot.city=r['block_name']
                myslot.address=r['address']
                myslot.pincode=r['pincode']
                myslot.vaccineName= r['vaccine']
                myslot.availableDose1=r['available_capacity_dose1']
                myslot.availableDose2=r['available_capacity_dose2']
                myslot.minAge=r['min_age_limit']
                myslot.free=r['fee']

                print(myslot)
                self._slots.append(myslot)

                if int(r['available_capacity_dose1']) > 0:
                    self._availableFlag=True

    def getReq(self):
        r = requests.get(self._URL + self._target, params=self._params, headers=self._headers, verify=True)
        if r.status_code == 200 :
            self._response = r.json()['sessions']
        else:
            print("NOK reposne: ", r.status_code)

    def getHtmlEmailBody(self):
        htmlEmailBody = "<table>"
        htmlEmailBody+=self._slots[0].getHtmlHeader()
        for s in self._slots:
            htmlEmailBody+= s.getHtml()
        htmlEmailBody += "</table>"
        return htmlEmailBody

    def sendEmail(self):
        try:
            if self._availableFlag!=True:
                print("No Available Slot, Not sending email")
                return 

            # creates SMTP session 
            email = smtplib.SMTP('smtp-relay.gmail.com', 587) 
            
            # TLS for security 
            email.starttls() 
            
            # authentication
            # compiler gives an error for wrong credential. 
            email.login("", "") 
            
            # MIMEMultipart 
            msg = MIMEMultipart() 

            # senders email address 
            msg['From'] = '' 

            # receivers email address 
            msg['To'] = '' 

            # the subject of mail
            msg['Subject'] = "Vaccine Available"

            # the body of the mail 
            body = self.getHtmlEmailBody() #"Vaccine Available"

            # attaching the body with the msg 
            msg.attach(MIMEText(body, 'html'))

            # Converts the Multipart msg into a string ß
            message = msg.as_string() 
            
            # sending the mail 
            email.sendmail('', '', message) 
            print("Email Sent....")
            # terminating the session 
            email.quit()
        except smtplib.SMTPException as e:
            print("Exception: {0}".format(e))
           
def main():
    mycowin = Cowin()
    a=0
    while a<10:
        for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]:
            #print(i)
            d =datetime.today() + timedelta(days=i)
            dt = d.strftime('%d-%m-%Y')
            #print("                                      Date:",dt)
            mycowin.getAvailabilityDistrict(363, dt)
            #print(mycowin.getHtmlEmailBody())
        # Send Email if Vaccine is Available for 18+
        mycowin.sendEmail()

        print("Sleeping for 20 sec")
        time.sleep(20)

        mycowin.flushEmailBody()

if __name__ == "__main__":
    main()