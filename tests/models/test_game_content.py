"""ContentsCalendar 모델 테스트."""
import pytest
from pyloa.models.game_content import ContentsCalendar, LevelRewardItems, RewardItem


def test_reward_item_from_dict():
    """Reward item은 API 응답에서 변환되어야 합니다."""
    data = {
        'Name': '전설 카드 팩',
        'Icon': 'https://...',
        'Grade': '전설'
    }
    
    item = RewardItem.from_dict(data)
    
    assert item.name == '전설 카드 팩'
    assert item.icon == 'https://...'
    assert item.grade == '전설'


def test_level_reward_items_from_dict():
    """LevelRewardItems는 중첩된 RewardItem 리스트를 포함해야 합니다."""
    data = {
        'ItemLevel': 1415,
        'Items': [
            {
                'Name': '파괴강석',
                'Icon': '...',
                'Grade': '일반'
            }
        ]
    }
    
    level_rewards = LevelRewardItems.from_dict(data)
    
    assert level_rewards.item_level == 1415
    assert len(level_rewards.items) == 1
    assert level_rewards.items[0].name == '파괴강석'


def test_contents_calendar_from_dict():
    """ContentsCalendar는 중첩된 레벨별 보상을 포함하여 API 응답에서 변환되어야 합니다."""
    data = {
        'CategoryName': '필드 보스',
        'ContentsName': '모아케',
        'ContentsIcon': 'https://...',
        'MinItemLevel': 1415,
        'StartTimes': [
            '2024-01-08T11:00:00'
        ],
        'Location': '파푸니카',
        'RewardItems': [
            {
                'ItemLevel': 0,
                'Items': [
                    {
                        'Name': '오르페우스의 별 #5',
                        'Icon': 'https://...',
                        'Grade': '유물'
                    }
                ]
            }
        ]
    }
    
    content = ContentsCalendar.from_dict(data)
    
    assert content.category_name == '필드 보스'
    assert content.contents_name == '모아케'
    assert content.min_item_level == 1415
    assert len(content.reward_items) == 1
    assert content.reward_items[0].items[0].name == '오르페우스의 별 #5'


def test_contents_calendar_to_dict():
    """ContentsCalendar는 중첩된 보상을 포함하여 딕셔너리로 변환되어야 합니다."""
    content = ContentsCalendar(
        category_name='가디언 토벌',
        contents_name='데스칼루다',
        contents_icon='...',
        min_item_level=1415,
        start_times=['2024-01-08'],
        location='가디언 토벌 게시판',
        reward_items=[
            LevelRewardItems(
                item_level=1415,
                items=[
                    RewardItem(name='파괴석', icon='...', grade='일반')
                ]
            )
        ]
    )
    
    data = content.to_dict()
    
    assert data['category_name'] == '가디언 토벌'
    assert data['reward_items'][0]['items'][0]['name'] == '파괴석'

