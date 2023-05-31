def processStatusCode(code):
    if code == 204:
        return "204: No Content"
    elif code == 304:
        return "304: Not Modified. See Conditional requests."
    elif code == 400:
        return "400: Bad Request"
    elif code == 401:
        return "401: Unauthorized "
    elif code == 403:
        return "403: Forbidden"
    elif code == 404:
        return "404: NotFound"
    elif code == 429:
        return "429: Too Many Requests - Rate limiting has been applied."
    elif code == 500:
        return "500: Internal Server Error. "
    elif code == 502:
        return "502: Bad Gateway"
    elif code == 503:
        return "503: Service Unavailable"
    else:
        return "Succeeded"
