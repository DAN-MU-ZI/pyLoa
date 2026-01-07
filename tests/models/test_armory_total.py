"""Armory Total (Summary) 모델 테스트."""
from pyloa.models.armory import ArmoryTotal, ArmoryProfile, ArmoryEquipment


def test_armory_total_deserialization():
    """ArmoryTotal은 API 응답에서 올바르게 역직렬화되어야 합니다."""
    data = {
        "ArmoryProfile": {
            "CharacterName": "TestChar",
            "ExpeditionLevel": 100,
            # ... minimal fields
            "CharacterImage": "", "PvpGradeName": "", "TownLevel": 0, "TownName": "", "Title": "", 
            "GuildMemberGrade": "", "GuildName": "", "Stats": [], "Tendencies": [], "ServerName": "", 
            "CharacterLevel": 0, "CharacterClassName": "", "ItemAvgLevel": "0", "ItemMaxLevel": "0"
        },
        "ArmoryEquipment": [
            {
                "Type": "Weapon",
                "Name": "Sword",
                "Icon": "", "Grade": "", "Tooltip": ""
            }
        ]
    }
    
    total = ArmoryTotal.from_dict(data)
    
    assert total.armory_profile is not None
    assert isinstance(total.armory_profile, ArmoryProfile)
    assert total.armory_profile.character_name == "TestChar"
    
    assert total.armory_equipment is not None
    assert len(total.armory_equipment) == 1
    assert isinstance(total.armory_equipment[0], ArmoryEquipment)
    assert total.armory_equipment[0].name == "Sword"
