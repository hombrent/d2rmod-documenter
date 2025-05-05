#!/usr/bin/env python

import requests
import os
from getpass import getpass

class BTDWikiLogin:
    def __init__(self):
        self.api_url = "https://btd.miraheze.org/w/api.php"
        self.session = requests.Session()
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
            print(f"Error: {str(e)}")
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

def main():
    username = "foo"
    password = "bar"
    
    wiki = BTDWikiLogin()
    if wiki.login(username, password):
        print("Login successful")
        # Update dev page
        wiki.upsert_page("Dev", "dev page. all under construction")
    else:
        print("Login failed")

if __name__ == "__main__":
    main() 