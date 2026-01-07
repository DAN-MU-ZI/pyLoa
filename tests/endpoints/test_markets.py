"""Tests for MarketsEndpoint."""
import pytest
from unittest.mock import Mock
from pyloa.client import LostArkAPI
from pyloa.endpoints.markets import MarketsEndpoint
from pyloa.models.market import MarketItem, Trade


def test_markets_endpoint_initialization():
    """MarketsEndpoint should have correct base_path."""
    client = Mock(spec=LostArkAPI)
    endpoint = MarketsEndpoint(client)
    
    assert endpoint.base_path == "/markets"
    assert endpoint.client == client


def test_get_options():
    """get_options should call _request with GET /options."""
    client = Mock(spec=LostArkAPI)
    endpoint = MarketsEndpoint(client)
    endpoint._request = Mock(return_value={'Categories': [], 'ItemGrades': []})
    
    options = endpoint.get_options()
    
    endpoint._request.assert_called_once_with('GET', '/options')
    assert 'Categories' in options


def test_get_item():
    """get_item should call _request with GET /items/{id}."""
    client = Mock(spec=LostArkAPI)
    endpoint = MarketsEndpoint(client)
    endpoint._request = Mock(return_value={
        'Id': 123,
        'Name': '테스트',
        'Grade': '일반',
        'Icon': 'https://...',
        'BundleCount': 10,
        'TradeRemainCount': 5
    })
    
    item = endpoint.get_item(123)
    
    endpoint._request.assert_called_once_with('GET', '/items/123')
    assert isinstance(item, MarketItem)
    assert item.id == 123


def test_search_items():
    """search_items should call _request with POST /items."""
    client = Mock(spec=LostArkAPI)
    endpoint = MarketsEndpoint(client)
    endpoint._request = Mock(return_value={
        'PageNo': 1,
        'PageSize': 10,
        'TotalCount': 1,
        'Items': [{
            'Id': 123,
            'Name': '테스트',
            'Grade': '일반',
            'Icon': 'https://...',
            'BundleCount': 10,
            'TradeRemainCount': 5
        }]
    })
    
    result = endpoint.search_items(ItemName="테스트", PageNo=1)
    
    # Should call POST with json body
    endpoint._request.assert_called_once_with(
        'POST',
        '/items',
        json={'ItemName': '테스트', 'PageNo': 1}
    )
    assert result['TotalCount'] == 1


def test_get_trades():
    """get_trades should call _request with POST /trades."""
    client = Mock(spec=LostArkAPI)
    endpoint = MarketsEndpoint(client)
    endpoint._request = Mock(return_value=[
        {'Date': '2024-01-07T10:00:00', 'Price': 100, 'Quantity': 5},
        {'Date': '2024-01-07T11:00:00', 'Price': 105, 'Quantity': 3}
    ])
    
    trades = endpoint.get_trades(ItemName="테스트")
    
    #Should call POST with json body
    endpoint._request.assert_called_once_with(
        'POST',
        '/trades',
        json={'ItemName': '테스트'}
    )
    assert len(trades) == 2
    assert isinstance(trades[0], Trade)
    assert trades[0].price == 100
