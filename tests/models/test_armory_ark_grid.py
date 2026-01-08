"""Armory Ark Grid 모델 테스트."""

from pyloa.models.armory import ArkGrid, ArkGridSlot, ArkGridGem, ArkGridEffect


def test_ark_grid_deserialization():
    """ArkGrid는 API 응답에서 올바르게 역직렬화되어야 합니다."""
    data = {
        "Slots": [
            {
                "Index": 1,
                "Icon": "icon_url",
                "Name": "Slot 1",
                "Point": 5,
                "Grade": "Legendary",
                "Tooltip": "Tooltip Text",
                "Gems": [
                    {
                        "Index": 0,
                        "Icon": "gem_icon",
                        "IsActive": True,
                        "Grade": "Relic",
                        "Tooltip": "Gem Tooltip",
                    }
                ],
            }
        ],
        "Effects": [{"Name": "Effect 1", "Level": 3, "Tooltip": "Effect Tooltip"}],
    }

    grid = ArkGrid.from_dict(data)

    assert len(grid.slots) == 1
    assert isinstance(grid.slots[0], ArkGridSlot)
    assert grid.slots[0].name == "Slot 1"

    assert len(grid.slots[0].gems) == 1
    assert isinstance(grid.slots[0].gems[0], ArkGridGem)
    assert grid.slots[0].gems[0].grade == "Relic"

    assert len(grid.effects) == 1
    assert isinstance(grid.effects[0], ArkGridEffect)
    assert grid.effects[0].level == 3
