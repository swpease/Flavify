

def search(request):
    """
    Using a
    ref: https://docs.djangoproject.com/en/1.11/ref/templates/api/#context-processors
    :param request: an HttpRequest
    :return: a dictionary representing context to be included by default with all rendered templates on the site.
    """
    context = {"search": "what"}
    return context