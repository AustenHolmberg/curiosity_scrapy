def ext_from_url(url):
    ext = url[url.rfind('.'):]
    return ext.lower()
