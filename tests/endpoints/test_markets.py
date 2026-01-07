"""MarketsEndpoint 테스트."""
import pytest
from unittest.mock import Mock
from pyloa.client import LostArkAPI
from pyloa.endpoints.markets import MarketsEndpoint
from pyloa.models.market import MarketItem, TradeMarketItem, Market, TradeMarket, MarketItemStats


def test_markets_endpoint_initialization():
    """MarketsEndpoint는 올바른 base_path를 가져야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = MarketsEndpoint(client)
    
    assert endpoint.base_path == "/markets"
    assert endpoint.client == client


def test_get_options():
    """get_options는 GET /options로 _request를 호출해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = MarketsEndpoint(client)
    endpoint._request = Mock(return_value={'Categories': [], 'ItemGrades': []})
    
    options = endpoint.get_options()
    
    endpoint._request.assert_called_once_with('GET', '/options')
    assert 'Categories' in options


def test_get_item():
    """get_item은 GET /items/{id}로 _request를 호출해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = MarketsEndpoint(client)
    endpoint._request = Mock(return_value=[{
        'Name': '파괴강석',
        'BundleCount': 10,
        'Stats': [
            {'Date': '2024-01-08', 'AvgPrice': 4.5, 'TradeCount': 1000}
        ]
    }])
    
    items = endpoint.get_item(123)
    
    endpoint._request.assert_called_once_with('GET', '/items/123')
    assert len(items) == 1
    assert isinstance(items[0], MarketItemStats)
    assert items[0].name == '파괴강석'


def test_search_items():
    """search_items는 POST /items로 _request를 호출해야 합니다."""
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
    
    endpoint._request.assert_called_once_with(
        'POST',
        '/items',
        json={'ItemName': '테스트', 'PageNo': 1}
    )
    assert result.total_count == 1
    assert isinstance(result.items[0], MarketItem)


def test_get_trades():
    """get_trades는 POST /trades로 _request를 호출해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = MarketsEndpoint(client)
    endpoint._request = Mock(return_value={
        'PageNo': 1,
        'PageSize': 10,
        'TotalCount': 1,
        'Items': [
            {'Id': 1, 'Name': '테스트', 'Grade': '일반', 'Icon': '...', 'BundleCount': 1, 'RecentPrice': 100}
        ]
    })
    
    result = endpoint.get_trades(ItemName="테스트")
    
    endpoint._request.assert_called_once_with(
        'POST',
        '/trades',
        json={'ItemName': '테스트'}
    )
    assert result.total_count == 1
    assert isinstance(result.items[0], TradeMarketItem)
    assert result.items[0].recent_price == 100
