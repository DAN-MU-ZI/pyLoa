"""AuctionsEndpoint 테스트."""

import pytest
from unittest.mock import Mock
from pyloa.client import LostArkAPI
from pyloa.endpoints.auctions import AuctionsEndpoint
from pyloa.models.auction import AuctionItem, ItemOption, Auction


def test_auctions_endpoint_initialization():
    """AuctionsEndpoint는 올바른 base_path를 가져야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = AuctionsEndpoint(client)

    assert endpoint.base_path == "/auctions"
    assert endpoint.client == client


def test_get_options():
    """get_options는 GET /options로 _request를 호출해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = AuctionsEndpoint(client)
    endpoint._request = Mock(return_value={"Categories": []})

    options = endpoint.get_options()

    endpoint._request.assert_called_once_with("GET", "/options")
    assert "Categories" in options


def test_get_items():
    """get_items는 POST /items로 _request를 호출해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = AuctionsEndpoint(client)
    endpoint._request = Mock(
        return_value={
            "PageNo": 1,
            "PageSize": 10,
            "TotalCount": 1,
            "Items": [
                {
                    "Name": "고대 목걸이",
                    "Grade": "고대",
                    "Tier": 3,
                    "Level": 1600,
                    "Icon": "...",
                    "GradeQuality": 100,
                    "AuctionInfo": {
                        "StartPrice": 1000,
                        "EndDate": "2024-01-08",
                        "BidCount": 0,
                        "BidStartPrice": 1000,
                        "IsCompetitive": False,
                        "TradeAllowCount": 2,
                    },
                    "Options": [],
                }
            ],
        }
    )

    result = endpoint.get_items(ItemName="목걸이")

    endpoint._request.assert_called_once_with(
        "POST", "/items", json={"ItemName": "목걸이"}
    )

    assert len(result.items) == 1
    assert isinstance(result.items[0], AuctionItem)
