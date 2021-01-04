from unittest import skip

from django.test import TestCase

from ..ebay_data import get_ebay_data


class TestEbayData(TestCase):
    @skip
    def test_get_data_from_ebay(self):
        response = get_ebay_data("legos")
        assert response.reply.ack == "Success"
        assert type(response.reply.timestamp) == datetime.datetime
        assert type(response.reply.searchResult.item) == list

        item = response.reply.searchResult.item[0]
        assert type(item.listingInfo.endTime) == datetime.datetime
        assert type(response.dict()) == dict
