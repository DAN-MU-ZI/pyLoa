"""Auction 모델 테스트."""

import pytest
from pyloa.models.auction import AuctionItem, ItemOption, AuctionInfo, Auction


def test_auction_item_from_dict():
    """AuctionItem은 API 응답에서 변환되어야 합니다."""
    data = {
        "Name": "고대 목걸이",
        "Grade": "고대",
        "Tier": 3,
        "Level": 1600,
        "Icon": "https://...",
        "GradeQuality": 100,
        "AuctionInfo": {
            "StartPrice": 1000,
            "BuyPrice": 1500,
            "BidPrice": 1200,
            "EndDate": "2024-01-08T00:00:00",
            "BidCount": 1,
            "BidStartPrice": 1000,
            "IsCompetitive": True,
            "TradeAllowCount": 2,
            "UpgradeLevel": 0,
        },
        "Options": [{"Type": "STAT", "OptionName": "특화", "Value": 600}],
    }

    item = AuctionItem.from_dict(data)

    assert item.name == "고대 목걸이"
    assert item.grade == "고대"
    assert item.tier == 3
    assert item.grade_quality == 100

    # Nested AuctionInfo
    assert isinstance(item.auction_info, AuctionInfo)
    assert item.auction_info.buy_price == 1500
    assert item.auction_info.is_competitive is True
    assert item.auction_info.upgrade_level == 0

    # Nested Options
    assert len(item.options) == 1
    assert isinstance(item.options[0], ItemOption)
    assert item.options[0].type == "STAT"
    assert item.options[0].value == 600


def test_auction_info_optional_fields():
    """AuctionInfo는 선택적 가격을 처리해야 합니다."""
    data = {
        "StartPrice": 1000,
        "EndDate": "2024-01-08",
        "BidCount": 0,
        "BidStartPrice": 1000,
        "IsCompetitive": False,
        "TradeAllowCount": 3,
        # BuyPrice, BidPrice, UpgradeLevel missing
    }

    info = AuctionInfo.from_dict(data)

    assert info.start_price == 1000
    assert info.buy_price is None
    assert info.bid_price is None
    assert info.upgrade_level is None


def test_auction_item_to_dict():
    """AuctionItem은 중첩된 객체를 포함하여 딕셔너리로 변환되어야 합니다."""
    item = AuctionItem(
        name="테스트",
        grade="고대",
        tier=3,
        level=1600,
        icon="...",
        grade_quality=90,
        auction_info=AuctionInfo(
            start_price=100,
            end_date="2024-01-01",
            bid_count=0,
            bid_start_price=100,
            is_competitive=False,
            trade_allow_count=1,
        ),
        options=[ItemOption(type="STAT", option_name="치명", value=500)],
    )

    data = item.to_dict()

    assert data["name"] == "테스트"
    assert data["auction_info"]["start_price"] == 100
    assert data["options"][0]["option_name"] == "치명"


def test_auction_from_dict():
    """Auction은 API 응답에서 변환되어야 합니다."""
    data = {"PageNo": 1, "PageSize": 10, "TotalCount": 5, "Items": []}

    result = Auction.from_dict(data)

    assert result.total_count == 5
    assert result.items == []
