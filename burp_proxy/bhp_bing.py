# Imports
from burp import IBurpExtender
from burp import IContextMenuFactory


from java.net import URL
from java.util import ArrayList
from javax.swing import JMenuItem
from thread import start_new_thread


import json
import socket
import urllib

API_KEY = ""
API_HOST = "api.cognitive.microsoft.com"


class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None

        callbacks.setExtensionName("BHP Bing")
        callbacks.registerContextMenuFactory(self)

        return

    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()

        menu_list.add(JMenuItem("Send to Bing", actionPerformed=self.bing_menu))

        return menu_list

    def bing_menu(self, event):
        http_traffic = self.context.getSelectedMessages()
        print(f"{len(http_traffic)} requests highlighted")

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
        
            print(f"User selected host: {host}")
            self.bing_search(host)

        return
    
    def bing_search(self, host):
        try:
            is_ip = bool(socket.inet_aton(host))
        except socket.error:
            is_ip = False

        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True
        
        start_new_thread(self.bing_query, (f"ip: {ip_address}"))

        if domain:
            start_new_thread(self.bing_query, (f"domain: {host}"))


    def bing_query(self, bing_query_string):
        print(f"Performing Bing Search {bing_query_string}")

        http_request = f'GET https://{API_HOST}/bing/v7.0/search?q={bing_query_string} HTTP/1.1\r\nHost: {API_HOST}\r\nConnection: close\r\nOcp-Apim-Subscription-Key: {API_KEY}\r\nUser-Agent: Black Hat Python\r\n\r\n'

        json_body = self._callbacks.makeHttpRequest(API_HOST, 443, True, http_request).tostring()
        json_body = json_body.split('\r\n\r\n', 1)[1]

        try:
            response = json.loads(json_body)
        except (TypeError, ValueError) as err:
            print(f'No result from bing: {err}')
        else:
            sites = list()
            if response.get('webPages'):
                sites = response['webPages']['value']
            if len(sites):
                for site in sites:
                    print('*' * 100)
                    print(f"Name: {site['name']}")
                    print(f"URL: {site['url']}")
                    print(f"Description: {site['snippet']}")
                    print('*' * 100)

                    java_url = URL(site['url'])

                    if not self._callbacks.isInScope(java_url):
                        print('Adding to Burp Scope')
                        self._callbacks.includeInScope(java_url)
                    else:
                        print(f'Empty response from Bing: {bing_query_string}')
        return
