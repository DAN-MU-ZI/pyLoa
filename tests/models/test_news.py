"""Tests for News models."""
import pytest
from pyloa.models.news import Notice, Event


def test_notice_from_dict_basic():
    """Notice should convert from API response format."""
    data = {
        'Title': '로스트아크 업데이트 안내',
        'Date': '2024-01-07',
        'Link': 'https://lostark.game.onstove.com/News/Notice/...',
        'Type': '공지'
    }
    
    notice = Notice.from_dict(data)
    
    assert notice.title == '로스트아크 업데이트 안내'
    assert notice.date == '2024-01-07'
    assert notice.link == 'https://lostark.game.onstove.com/News/Notice/...'
    assert notice.type == '공지'


def test_event_from_dict_all_fields():
    """Event should convert from API response with all fields."""
    data = {
        'Title': '신규 이벤트',
        'Thumbnail': 'https://cdn-lostark.game.onstove.com/...',
        'Link': 'https://lostark.game.onstove.com/News/Event/...',
        'StartDate': '2024-01-01',
        'EndDate': '2024-01-31',
        'RewardDate': '2024-02-07'
    }
    
    event = Event.from_dict(data)
    
    assert event.title == '신규 이벤트'
    assert event.thumbnail == 'https://cdn-lostark.game.onstove.com/...'
    assert event.link == 'https://lostark.game.onstove.com/News/Event/...'
    assert event.start_date == '2024-01-01'
    assert event.end_date == '2024-01-31'
    assert event.reward_date == '2024-02-07'


def test_event_from_dict_missing_reward_date():
    """Event should handle missing RewardDate."""
    data = {
        'Title': '신규 이벤트',
        'Thumbnail': 'https://cdn-lostark.game.onstove.com/...',
        'Link': 'https://lostark.game.onstove.com/News/Event/...',
        'StartDate': '2024-01-01',
        'EndDate': '2024-01-31'
    }
    
    event = Event.from_dict(data)
    
    assert event.reward_date is None


def test_notice_to_dict():
    """Notice should convert to dict."""
    notice = Notice(
        title='테스트 공지',
        date='2024-01-07',
        link='https://test.com',
        type='공지'
    )
    
    data = notice.to_dict()
    
    assert data['title'] == '테스트 공지'
    assert data['date'] == '2024-01-07'
    assert data['link'] == 'https://test.com'
    assert data['type'] == '공지'
