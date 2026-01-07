"""OpenAPIUserAlarm 모델 테스트."""
from pyloa.models.news import OpenAPIUserAlarm, OpenAPIUserAlarmContent


def test_user_alarm_deserialization():
    """OpenAPIUserAlarm은 API 응답에서 올바르게 역직렬화되어야 합니다."""
    data = {
        "RequirePolling": True,
        "Alarms": [
            {
                "AlarmType": "All",
                "Contents": "Alarm Content 1",
                "StartDate": "2024-01-01T00:00:00",
                "EndDate": "2024-01-02T00:00:00"
            }
        ]
    }
    
    alarm = OpenAPIUserAlarm.from_dict(data)
    
    assert alarm.require_polling is True
    assert len(alarm.alarms) == 1
    assert isinstance(alarm.alarms[0], OpenAPIUserAlarmContent)
    assert alarm.alarms[0].alarm_type == "All"
    assert alarm.alarms[0].contents == "Alarm Content 1"
    assert alarm.alarms[0].start_date == "2024-01-01T00:00:00"
    assert alarm.alarms[0].end_date == "2024-01-02T00:00:00"

