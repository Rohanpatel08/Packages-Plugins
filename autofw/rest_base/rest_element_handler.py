

class RestElementHandler:
    def __init__(self, method, url, driver):
        self.method = method
        self.url = url
        self.driver = driver

    def send(self,
             params=None,
             data=None,
             headers=None,
             cookies=None,
             files=None,
             auth=None,
             timeout=None,
             allow_redirects=True,
             proxies=None,
             hooks=None,
             stream=None,
             verify=None,
             cert=None,
             json=None,
             **kwargs
             ):
        if kwargs:
            _url = self.url.format(**kwargs)
        else:
            _url = self.url
        self.driver.send(method=self.method,
                         url=_url,
                         params=params,
                         data=data,
                         headers=headers,
                         cookies=cookies,
                         files=files,
                         auth=auth,
                         timeout=timeout,
                         allow_redirects=allow_redirects,
                         proxies=proxies,
                         hooks=hooks,
                         stream=stream,
                         verify=verify,
                         cert=cert,
                         json=json
                         )
