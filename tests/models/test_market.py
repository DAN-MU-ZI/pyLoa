"""Market 모델 테스트."""
import pytest
from pyloa.models.market import MarketItem, TradeMarketItem, TradeMarket, MarketItemStats, MarketStatsInfo


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
        'RecentPrice': 11,
        'CurrentMinPrice': 10
    }
    
    item = MarketItem.from_dict(data)
    
    assert item.id == 66110221
    assert item.name == '명예의 파편 주머니(소)'
    assert item.grade == '일반'
    assert item.bundle_count == 10
    assert item.y_day_avg_price == 10.5
    assert item.recent_price == 11


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


def test_trade_market_item_from_dict():
    """TradeMarketItem은 API 응답에서 변환되어야 합니다."""
    data = {
        'Id': 66102004,
        'Name': '파괴강석',
        'Grade': '일반',
        'Icon': '...',
        'BundleCount': 10,
        'RecentPrice': 4
    }
    
    item = TradeMarketItem.from_dict(data)
    
    assert item.name == '파괴강석'
    assert item.recent_price == 4


def test_market_item_stats_from_dict():
    """MarketItemStats는 중첩된 통계 정보를 포함해야 합니다."""
    data = {
        'Name': '파괴강석',
        'BundleCount': 10,
        'Stats': [
            {
                'Date': '2024-01-08',
                'AvgPrice': 4.5,
                'TradeCount': 1000
            }
        ]
    }
    
    stats = MarketItemStats.from_dict(data)
    
    assert stats.name == '파괴강석'
    assert len(stats.stats) == 1
    assert stats.stats[0].avg_price == 4.5


def test_trade_market_from_dict():
    """TradeMarket 검색 결과는 API 응답에서 변환되어야 합니다."""
    data = {
        'PageNo': 1,
        'PageSize': 10,
        'TotalCount': 1,
        'Items': [
            {
                'Id': 1, 'Name': '아이템', 'Grade': '일반', 'Icon': '...', 'BundleCount': 1
            }
        ]
    }
    
    result = TradeMarket.from_dict(data)
    
    assert result.total_count == 1
    assert len(result.items) == 1
    assert result.items[0].name == '아이템'

