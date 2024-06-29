import requests
from bs4 import BeautifulSoup
import os
import re

def print_banner():
    banner = """
\033[91m
                                                                                                                                                                                                
                                                                                                                                                                                                
YYYYYYY       YYYYYYYRRRRRRRRRRRRRRRRR                           WWWWWWWW                           WWWWWWWW     OOOOOOOOO     RRRRRRRRRRRRRRRRR   LLLLLLLLLLL             DDDDDDDDDDDDD        
Y:::::Y       Y:::::YR::::::::::::::::R                          W::::::W                           W::::::W   OO:::::::::OO   R::::::::::::::::R  L:::::::::L             D::::::::::::DDD     
Y:::::Y       Y:::::YR::::::RRRRRR:::::R                         W::::::W                           W::::::W OO:::::::::::::OO R::::::RRRRRR:::::R L:::::::::L             D:::::::::::::::DD   
Y::::::Y     Y::::::YRR:::::R     R:::::R                        W::::::W                           W::::::WO:::::::OOO:::::::ORR:::::R     R:::::RLL:::::::LL             DDD:::::DDDDD:::::D  
YYY:::::Y   Y:::::YYY  R::::R     R:::::R                         W:::::W           WWWWW           W:::::W O::::::O   O::::::O  R::::R     R:::::R  L:::::L                 D:::::D    D:::::D 
   Y:::::Y Y:::::Y     R::::R     R:::::R                          W:::::W         W:::::W         W:::::W  O:::::O     O:::::O  R::::R     R:::::R  L:::::L                 D:::::D     D:::::D
    Y:::::Y:::::Y      R::::RRRRRR:::::R                            W:::::W       W:::::::W       W:::::W   O:::::O     O:::::O  R::::RRRRRR:::::R   L:::::L                 D:::::D     D:::::D
     Y:::::::::Y       R:::::::::::::RR                              W:::::W     W:::::::::W     W:::::W    O:::::O     O:::::O  R:::::::::::::RR    L:::::L                 D:::::D     D:::::D
      Y:::::::Y        R::::RRRRRR:::::R                              W:::::W   W:::::W:::::W   W:::::W     O:::::O     O:::::O  R::::RRRRRR:::::R   L:::::L                 D:::::D     D:::::D
       Y:::::Y         R::::R     R:::::R                              W:::::W W:::::W W:::::W W:::::W      O:::::O     O:::::O  R::::R     R:::::R  L:::::L                 D:::::D     D:::::D
       Y:::::Y         R::::R     R:::::R                               W:::::W:::::W   W:::::W:::::W       O:::::O     O:::::O  R::::R     R:::::R  L:::::L                 D:::::D     D:::::D
       Y:::::Y         R::::R     R:::::R                                W:::::::::W     W:::::::::W        O::::::O   O::::::O  R::::R     R:::::R  L:::::L         LLLLLL  D:::::D    D:::::D 
       Y:::::Y       RR:::::R     R:::::R                                 W:::::::W       W:::::::W         O:::::::OOO:::::::ORR:::::R     R:::::RLL:::::::LLLLLLLLL:::::LDDD:::::DDDDD:::::D  
    YYYY:::::YYYY    R::::::R     R:::::R                                  W:::::W         W:::::W           OO:::::::::::::OO R::::::R     R:::::RL::::::::::::::::::::::LD:::::::::::::::DD   
    Y:::::::::::Y    R::::::R     R:::::R                                   W:::W           W:::W              OO:::::::::OO   R::::::R     R:::::RL::::::::::::::::::::::LD::::::::::::DDD     
    YYYYYYYYYYYYY    RRRRRRRR     RRRRRRR                                    WWW             WWW                 OOOOOOOOO     RRRRRRRR     RRRRRRRLLLLLLLLLLLLLLLLLLLLLLLLDDDDDDDDDDDDD        
                                         ________________________                                                                                                                               
                                         _::::::::::::::::::::::_                                                                                                                               
                                         ________________________                                                                                                                               
                                                                                                                                                                                                   
\033[0m                                                   
    """
    print(banner)

def extract_data(content):
    # Regular expressions for extracting names, Gmail addresses, and messages
    name_regex = re.compile(r'\bName: ([A-Za-z ]+)\b')
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@gmail\.com\b')
    message_regex = re.compile(r'\bMessage: ([\s\S]+?)(?=Name: |\Z)', re.MULTILINE)

    names = name_regex.findall(content)
    emails = email_regex.findall(content)
    messages = message_regex.findall(content)

    return names, emails, messages

def extract_data_from_url():
    url = input("Paste Your URL: ").strip()

    if not url.startswith(('http://', 'https://')):
        print("Invalid URL. Please make sure the URL starts with http:// or https://")
        return None
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        content = response.text

        # If the URL returns HTML content, parse it using BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text(separator='\n')  # Get all text content, separated by newlines
        return extract_data(text_content)
    except requests.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None

def extract_data_from_txt():
    file_path = input("Paste Your Text File Path: ").strip()

    # Remove potential extra characters from file path input
    if file_path.startswith('& '):
        file_path = file_path[2:].strip()

    if not os.path.isfile(file_path):
        print(f"The file path '{file_path}' is invalid or the file does not exist.")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return extract_data(content)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def main():
    while True:
        print_banner()

        print("\nSelect an option:")
        print("01. URL")
        print("02. File")
        print("00. Exit")

        option = input("Enter option: ")

        if option == "01":
            print("Extracting data from URL...")
            data = extract_data_from_url()
            if data:
                names, emails, messages = data
                print("Names extracted from URL:", names)
                print("Gmail addresses extracted from URL:", emails)
                print("Messages extracted from URL:", messages)
                print("\n")
        elif option == "02":
            print("Extracting data from text file...")
            data = extract_data_from_txt()
            if data:
                names, emails, messages = data
                print("Names extracted from text file:", names)
                print("Gmail addresses extracted from text file:", emails)
                print("Messages extracted from text file:", messages)
                print("\n")
        elif option == "00":
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()