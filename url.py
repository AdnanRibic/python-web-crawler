from urllib.parse import urlparse
# Get sub domain name: something.telenor.no
def get_suburl(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
# Get domain url
def get_url(url):
    try:
        # We need to split domain name and beacuse we are now that hey are always splited with dots we will use one
        results = get_suburl(url).split('.')
        # No metter how long subdomains are we need last two -2 and -1
        return results[-2] + '.' + results[-1]
    except:
        #Return empty string
        return ''
