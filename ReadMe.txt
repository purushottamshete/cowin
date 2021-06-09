Name: Cowin.py
Author: Purushottam Shete
Email: purushottamshete@gmail.com

Description: Cowin Vassine Slot Checking and email notification script
This script checks vaccine slot for a district for next 20 days
And if the vaccine slot is available for 18-45 age it will send notification on your email.

Note: This script works from indian servers of IP address for rest setu api gives autherization error.
Please refer: https://apisetu.gov.in/public/marketplace/api/cowin


How to Use:
1. Set your diistrict id
            mycowin.getAvailabilityDistrict(363, dt)

use below api to find your distict id
/v2/admin/location/districts/{state_id}
Example: https://cdn-api.co-vin.in/api/v2/admin/location/districts/21

and get state_id with below api
/v2/admin/location/districts/{state_id}
https://cdn-api.co-vin.in/api/v2/admin/location/states

2. Set email credentials:
 # authentication
            # compiler gives an error for wrong credential. 
            email.login("<email_id>", "<password>") 
            
3. Set email from and to # senders email address 
            msg['From'] = '' 

            # receivers email address 
            msg['To'] = '' 

            # sending the mail 
            email.sendmail('<to_email>', '<from_email>', message) 

Run: python cowin.py

