"""Tests for GameContent models."""
import pytest
from pyloa.models.game_content import GameContent, GameContentRewardItem


def test_game_content_reward_item_from_dict():
    """Reward item should convert from API response."""
    data = {
        'Name': '전설 카드 팩',
        'Icon': 'https://...',
        'Grade': '전설'
    }
    
    item = GameContentRewardItem.from_dict(data)
    
    assert item.name == '전설 카드 팩'
    assert item.icon == 'https://...'
    assert item.grade == '전설'


def test_game_content_from_dict():
    """GameContent should convert from API response including nested rewards."""
    data = {
        'CategoryName': '필드 보스',
        'ContentsName': '모아케',
        'ContentsIcon': 'https://...',
        'MinItemLevel': 1415,
        'StartTimes': [
            '2024-01-08T11:00:00',
            '2024-01-08T12:00:00'
        ],
        'Location': '파푸니카',
        'RewardItems': [
            {
                'Name': '오르페우스의 별 #5',
                'Icon': 'https://...',
                'Grade': '유물'
            }
        ]
    }
    
    content = GameContent.from_dict(data)
    
    assert content.category_name == '필드 보스'
    assert content.contents_name == '모아케'
    assert content.min_item_level == 1415
    assert len(content.start_times) == 2
    assert content.location == '파푸니카'
    
    # Nested rewards
    assert len(content.reward_items) == 1
    assert isinstance(content.reward_items[0], GameContentRewardItem)
    assert content.reward_items[0].name == '오르페우스의 별 #5'


def test_game_content_to_dict():
    """GameContent should convert to dict including nested rewards."""
    content = GameContent(
        category_name='가디언 토벌',
        contents_name='데스칼루다',
        contents_icon='...',
        min_item_level=1415,
        start_times=['2024-01-08'],
        location='가디언 토벌 게시판',
        reward_items=[
            GameContentRewardItem(
                name='파괴석',
                icon='...',
                grade='일반'
            )
        ]
    )
    
    data = content.to_dict()
    
    assert data['category_name'] == '가디언 토벌'
    assert data['reward_items'][0]['name'] == '파괴석'
