import requests
import random
import string
import time
from colorama import Fore

while True:
    time.sleep(2.5)
    try:
        response = requests.get('https://www.instagram.com/accounts/emailsignup/')
        csrf_token = response.cookies.get("csrftoken")

        headers = {
            'x-csrftoken': csrf_token,
        }

        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)) 
        data = {'username': username}

        response = requests.post('https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/',
            headers=headers,
            data=data
        )

        response_json = response.json()
        errors = response_json.get('errors', {})
        if '{"message":"","spam":true,"status":"fail"}' in response.text:
            print(f"{Fore.RED}Ratelimited{Fore.RESET}")
        elif 'username' in errors:
            if any(error['code'] == 'username_is_taken' for error in errors['username']):
                print(f"{Fore.MAGENTA}@{Fore.RESET}{Fore.CYAN}{username}{Fore.RED} taken.{Fore.RESET}")
        elif 'CSRF' in response.text:
            print(f"{Fore.RED}CSRF invalid{Fore.RESET}")
        else:
            print(f"{Fore.MAGENTA}@{Fore.RESET}{Fore.CYAN}{username}{Fore.GREEN} available!{Fore.RESET}")
            with open('available.txt', 'a') as file:
                    file.write(f"{username}\n")
    except:
        pass
