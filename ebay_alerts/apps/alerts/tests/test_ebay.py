from django.test import TestCase
from unittest import skip
from ..ebay_data import get_ebay_data, get_ebay_data_fake


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

    def test_get_data_from_fake_ebay(self):
        response = get_ebay_data_fake("a")
        assert type(response) == list
        if response:
            item = response[0]
            assert "a" in item["title"]
