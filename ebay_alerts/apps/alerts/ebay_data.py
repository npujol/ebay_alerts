import datetime
from django.conf import settings
from ebaysdk.finding import Connection
from .fake_ebay import get_filtered_data


def get_ebay_data(search_term):
    try:
        api = Connection(
            domain="svcs.sandbox.ebay.com",
            appid=settings.EBAY_APPID,
            config_file=None,
        )
        request = {
            "keywords": search_term,
            "itemFilter": [{"name": "condition", "value": "new"}],
            "paginationInput": {"entriesPerPage": 10, "pageNumber": 1},
            "sortOrder": "PricePlusShippingLowest",
        }
        response = api.execute("findItemsAdvanced", request)
    except ConnectionError as e:
        raise e

    return response


def get_ebay_data_fake(search_term):
    return get_filtered_data(search_term, limit=2)