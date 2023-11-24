from requests.sessions import Session

from autofw.utilities.logger import logger


class HTTPVerbs:
    POST = "POST"
    PUT = "PUT"
    GET = "GET"
    PATCH = "PATCH"
    DELETE = "DELETE"


class RestRequestDriver(Session):
    def request(
                self,
                method,
                url,
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
                json=None
    ):
        logger.debug()
        return super().request(method=method,
                                url=url,
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

