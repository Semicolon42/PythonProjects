import requests

def call_google(event=None, context=None):
    print (f"Starting Lambda Logic event=\"{event}\" context={context}")
    url = "https://www.google.com"
    r = requests.get(url)
    print (f"Python request result url={url} result={r}")
