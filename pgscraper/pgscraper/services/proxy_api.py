from scrapy.utils.project import get_project_settings
from urllib.parse import urlencode


def generate_proxy_url(url):
    settings=get_project_settings()
    payload = {
        'api_key': settings.get('PROXY_SERVICE_API_KEY'),
        'url': url
    }
    return settings.get('PROXY_SERVICE_API_URL') + urlencode(payload)
    