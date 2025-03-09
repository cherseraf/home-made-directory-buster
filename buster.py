import argparse
import time
import requests
import re
import threading

import threading
import requests
import re

def search_directories(cookie, recursive, extension, headers, cookies, base_url, file, timeInSeconds):
    try:
        if base_url == "" or file == "":
            print("Invalid URL or file values.")
            exit()
        else:
            threads = []  # List to store all threads

            with open(file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if(extension):
                        line = line + "." + extension
                    
                    current_url = base_url + line
                    response = requests.get(url=current_url, headers=headers, cookies=cookies)

                    if(response.status_code >= 200 and response.status_code < 300):
                        print("Directory found: " + current_url)
                        if(recursive):
                            current_url = current_url + "/"
                            thread = threading.Thread(target=search_directories, args=(cookie, recursive, extension, headers, cookies, current_url, file, timeInSeconds))
                            threads.append(thread)  # Add the thread to the list
                            thread.start()

            for thread in threads:
                thread.join()
    
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")




def main():

    parser = argparse.ArgumentParser(description="A small directory busting tool.")

    parser.add_argument("url", type=str, help="The target webserver.")
    parser.add_argument("file", type=str, help="File to brute force the website with.")

    parser.add_argument("-a", type=str, default="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)", help="Change your USER_AGENT.")
    parser.add_argument("-c", type=str, help="Set your cookie.")
    parser.add_argument("-r", action='store_true', help="Search recursively.")
    parser.add_argument("-x", type=str, help="Search with specific extension. (e.g. php, aspx)")
    parser.add_argument("-t", type=float, default=0.001, help="Specify the waiting timeInSeconds in seconds. (Default is 0.1 seconds.)")

    args = parser.parse_args()

    url = args.url
    file = args.file

    if(url == ""):
        print("Please specify a URL")
        exit()
    if(file == ""):
        print("Please specify a file")
        exit()

    cookie = args.c
    recursive = args.r
    extension = args.x
    timeInSeconds = args.t

    if(url[-1] != "/"):
        url = url + "/"

    if(args.a):
        headers = {
            'User-Agent': args.a
        }
    
    if(args.c):
        cookies = {cookie.split(':')[0]: cookie.split(':')[1] for cookie in args.c.split(';')}
    else:
        cookies = {}

    search_directories(cookie, recursive, extension, headers, cookies, url, file, timeInSeconds)
    

if(__name__ == "__main__"):
    main()
