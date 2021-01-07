import datetime

from django.conf import settings
from ebaysdk.finding import Connection


def get_ebay_data(search_term, limit=10, interval_time=30, only_new=False):
    try:
        api = Connection(
            domain="svcs.sandbox.ebay.com", appid=settings.EBAY_APPID, config_file=None
        )
        now = datetime.datetime.utcnow()
        now_minus_interval = now - datetime.timedelta(minutes=int(interval_time))
        if only_new:
            request = {
                "keywords": search_term,
                "itemFilter": [
                    {"name": "condition", "value": "new"},
                    {"name": "StartTimeFrom", "value": now_minus_interval.isoformat()},
                ],
                "paginationInput": {"entriesPerPage": limit, "pageNumber": 1},
                "sortOrder": "PricePlusShippingLowest",
            }
        else:
            request = {
                "keywords": search_term,
                "itemFilter": [{"name": "condition", "value": "new"}],
                "paginationInput": {"entriesPerPage": limit, "pageNumber": 1},
                "sortOrder": "PricePlusShippingLowest",
            }
        response = api.execute("findItemsAdvanced", request)
    except Exception:
        return []
    if response.reply.ack == "Success":
        if response.reply.searchResult._count != "0":
            if response.reply.searchResult.item:
                return response.reply.searchResult.item
    return []
