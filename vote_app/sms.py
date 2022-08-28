from typing import List
import requests
from django.conf import settings


class SmsApi:
    BASE_URL = "https://sms.textcus.com/api/send"
    API_KEY = settings.SMS_API_KEY

    def send(self, recipients: List[str], message: str, sender_id: str) -> bool:
        recipients = self.clean_recipients(recipients)
        recipients_string = ",".join(recipients)
        params = {
            "apikey": self.API_KEY,
            "destination": recipients_string,
            "message": message,
            "source": sender_id,
            "dlr": 0,
            "type": 0,
        }
        url = "https://sms.textcus.com/api/send"
        try:
            response = requests.get(url, params=params)
            response_data = response.json()
            
            return response_data["status"] == "0000"
        except Exception as e:
            print(e)
            print('/n/n/n/n')
            raise e

    def clean_recipients(self, recipients: List[str]) -> List[str]:
        cleaned_list: List[str] = []
        for number in recipients:
            if len(number) < 10:
                cleaned_number = "".join(["233", number])
            elif len(number) == 10:
                cleaned_number = "".join(["233", number[1:]])
            else:
                cleaned_number = number
            cleaned_list.append(cleaned_number)
        return cleaned_list




class Sms:
    """An abstraction class for integrating with an sms api"""
    sms_host: str = "https://api.mnotify.com/api/"
    api_key = settings.MNOTIFY_SMS_API_KEY
    balance_url = f"{sms_host}balance/sms?key={api_key}"
    bulk_sms_url = 'https://api.mnotify.com/api/sms/quick?key=' + api_key

    def check_balance(self):
        response = requests.get()
        return response
    
    def send_message(self, message: str, recipients: List[str], sender:str = "KSA-EC", is_scheduled=False, schedule_date="") -> requests.Response:
        # TODO This deactivates all sms sending
        """ response = requests.Response()
        return response """
        data = {
            'recipient[]': [self.parse_number(number) for number in recipients],
            'sender': sender,
            'message': message,
            'is_schedule': is_scheduled,
            'schedule_date': schedule_date,
        }
        response = requests.post(self.bulk_sms_url, data=data)
        return response
        
    
    def send_my_sms(self):
        return self.send_message("Hello from Prince", ['0243186008'])
    
    def parse_number(self, number: str):
        if len(number) > 10:
            if number.startswith("233"):
                number = number.replace('233', '0', 1)
        return number
    
    
        
