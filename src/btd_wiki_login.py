#!/usr/bin/env python

import requests
import os
import sys
import ssl
from getpass import getpass

class BTDWikiLogin:
    def __init__(self):
        self.api_url = "https://btd.miraheze.org/w/api.php"
        #context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        #context.minimum_version = ssl.TLSVersion.TLSv1_3
        self.session = requests.Session()
        #self.session.ssl_context = context
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0'
        }

    def login(self, username, password):
        """Basic login to BTD Wiki"""
        try:
            # Step 1: Get login token
            token_params = {
                "action": "query",
                "meta": "tokens",
                "type": "login",
                "format": "json"
            }
            
            r = self.session.get(self.api_url, params=token_params)
            login_token = r.json()["query"]["tokens"]["logintoken"]
            
            # Step 2: Perform login
            login_data = {
                "action": "login",
                "lgname": username,
                "lgpassword": password,
                "lgtoken": login_token,
                "format": "json"
            }
            
            r = self.session.post(self.api_url, data=login_data)
            return "Success" in str(r.json())
            
        except Exception as e:
            print(f"Error: {str(e)} using: {username} // {password}")
            return False

    def upsert_page(self, title, content):
        """Create or update a wiki page"""
        try:
            # Get CSRF token
            r = self.session.get(self.api_url, params={
                "action": "query",
                "meta": "tokens",
                "format": "json"
            })
            csrf_token = r.json()["query"]["tokens"]["csrftoken"]
            
            # Edit the page
            r = self.session.post(self.api_url, data={
                "action": "edit",
                "title": title,
                "text": content,
                "token": csrf_token,
                "format": "json"
            })
            
            result = r.json()
            if "error" in result:
                print(f"Error editing page: {result['error']['info']}")
                return False
            elif "edit" in result and result["edit"]["result"] == "Success":
                print(f"Successfully edited page: {title}")
                return True
            else:
                print(f"Unknown error: {result}")
                return False
                
        except Exception as e:
            print(f"Error editing page: {str(e)}")
            return False

def list_files_recursive(folder_path):
    """
    Recursively lists all files in a directory and its subdirectories.

    Args:
        folder_path (str): The path to the directory.

    Returns:
        list: A list of file paths.
    """
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_paths.append(file_path)
    return file_paths

def main():
    from btd_wiki_creds import btd_creds
    #print(f"username: {btd_creds['username']} password: {btd_creds['password']}")
    #print(f"openssl version {ssl.OPENSSL_VERSION}")

    wiki = BTDWikiLogin()
    if wiki.login(btd_creds["username"], btd_creds["password"]):
        print("Login successful")
    else:
        print("Login failed")
        sys.exit()

    basedir = "../docs"
    wikifiles = list_files_recursive(basedir)
    #wikifiles = ["../docs/Items/Unique/Ravaging_T1"]
    for wikifile in wikifiles:
        wikipath = wikifile.lstrip(basedir)
        print(f"{wikifile} {wikipath}")
        with open(wikifile, "r") as file:
            contents = file.read()
            print("==================")
            print(contents)
            print("\n\n\n\n")
            wiki.upsert_page(wikipath, contents)

    

if __name__ == "__main__":
    main() 
