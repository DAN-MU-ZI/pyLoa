"""Market 모델 테스트."""
import pytest
from pyloa.models.market import MarketItem, Trade


def test_market_item_from_dict():
    """MarketItem은 API 응답에서 변환되어야 합니다."""
    data = {
        'Id': 66110221,
        'Name': '명예의 파편 주머니(소)',
        'Grade': '일반',
        'Icon': 'https://cdn-lostark.game.onstove.com/...',
        'BundleCount': 10,
        'TradeRemainCount': 3,
        'YDayAvgPrice': 10.5,
        'RecentPrice': 11.0,
        'CurrentMinPrice': 10.0
    }
    
    item = MarketItem.from_dict(data)
    
    assert item.id == 66110221
    assert item.name == '명예의 파편 주머니(소)'
    assert item.grade == '일반'
    assert item.bundle_count == 10
    assert item.y_day_avg_price == 10.5
    assert item.recent_price == 11.0


def test_market_item_optional_prices():
    """MarketItem은 None 가격을 처리해야 합니다."""
    data = {
        'Id': 123,
        'Name': '테스트 아이템',
        'Grade': '희귀',
        'Icon': 'https://...',
        'BundleCount': 1,
        'TradeRemainCount': 0
    }
    
    item = MarketItem.from_dict(data)
    
    assert item.id == 123
    assert item.y_day_avg_price is None
    assert item.recent_price is None
    assert item.current_min_price is None


def test_trade_from_dict():
    """Trade는 API 응답에서 변환되어야 합니다."""
    data = {
        'Date': '2024-01-07T10:30:00',
        'Price': 1000,
        'Quantity': 5
    }
    
    trade = Trade.from_dict(data)
    
    assert trade.date == '2024-01-07T10:30:00'
    assert trade.price == 1000
    assert trade.quantity == 5


def test_market_item_to_dict():
    """MarketItem은 딕셔너리로 변환되어야 합니다."""
    item = MarketItem(
        id=123,
        name='테스트',
        grade='일반',
        icon='https://...',
        bundle_count=10,
        trade_remain_count=5,
        y_day_avg_price=100.0,
        recent_price=110.0,
        current_min_price=95.0
    )
    
    data = item.to_dict()
    
    assert data['id'] == 123
    assert data['name'] == '테스트'
    assert data['y_day_avg_price'] == 100.0
