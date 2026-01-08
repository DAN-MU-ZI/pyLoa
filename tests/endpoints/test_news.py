"""NewsEndpoint 테스트."""

import pytest
from unittest.mock import Mock
from requests import Response
from pyloa.client import LostArkAPI
from pyloa.endpoints.news import NewsEndpoint
from pyloa.models.news import NoticeList, Event, OpenAPIUserAlarm


def test_news_endpoint_initialization():
    """NewsEndpoint는 올바른 base_path를 가져야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = NewsEndpoint(client)

    assert endpoint.base_path == "/news"
    assert endpoint.client == client


def test_get_notices_no_params():
    """get_notices는 올바른 경로로 _request를 호출해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = NewsEndpoint(client)

    # Mock _request to return sample data
    endpoint._request = Mock(
        return_value=[
            {
                "Title": "테스트 공지",
                "Date": "2024-01-07",
                "Link": "https://test.com",
                "Type": "공지",
            }
        ]
    )

    notices = endpoint.get_notices()

    # Should call _request with GET /notices
    endpoint._request.assert_called_once_with("GET", "/notices", params={})

    # Should return list of NoticeList objects
    assert len(notices) == 1
    assert isinstance(notices[0], NoticeList)
    assert notices[0].title == "테스트 공지"


def test_get_notices_with_params():
    """get_notices는 파라미터를 올바르게 전달해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = NewsEndpoint(client)
    endpoint._request = Mock(return_value=[])

    endpoint.get_notices(searchText="업데이트", type="공지")

    # Should pass both params
    endpoint._request.assert_called_once_with(
        "GET", "/notices", params={"searchText": "업데이트", "type": "공지"}
    )


def test_get_notices_with_partial_params():
    """get_notices는 부분 파라미터를 처리해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = NewsEndpoint(client)
    endpoint._request = Mock(return_value=[])

    endpoint.get_notices(searchText="업데이트")

    # Should only include provided param
    endpoint._request.assert_called_once_with(
        "GET", "/notices", params={"searchText": "업데이트"}
    )


def test_get_events():
    """get_events는 올바른 경로로 _request를 호출해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = NewsEndpoint(client)

    # Mock _request to return sample data
    endpoint._request = Mock(
        return_value=[
            {
                "Title": "신규 이벤트",
                "Thumbnail": "https://cdn.test.com/img.png",
                "Link": "https://test.com/event",
                "StartDate": "2024-01-01",
                "EndDate": "2024-01-31",
                "RewardDate": "2024-02-07",
            }
        ]
    )

    events = endpoint.get_events()

    # Should call _request with GET /events
    endpoint._request.assert_called_once_with("GET", "/events")

    # Should return list of Event objects
    assert len(events) == 1
    assert isinstance(events[0], Event)
    assert events[0].title == "신규 이벤트"
    assert events[0].reward_date == "2024-02-07"


def test_get_events_missing_reward_date():
    """get_events는 RewardDate 누락을 처리해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = NewsEndpoint(client)

    endpoint._request = Mock(
        return_value=[
            {
                "Title": "신규 이벤트",
                "Thumbnail": "https://cdn.test.com/img.png",
                "Link": "https://test.com/event",
                "StartDate": "2024-01-01",
                "EndDate": "2024-01-31",
            }
        ]
    )

    events = endpoint.get_events()

    assert events[0].reward_date is None


def test_get_alarms():
    """get_alarms는 올바른 경로로 _request를 호출해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = NewsEndpoint(client)

    # Mock _request to return sample data
    endpoint._request = Mock(
        return_value={
            "RequirePolling": True,
            "Alarms": [
                {
                    "AlarmType": "All",
                    "Contents": "Test Alarm",
                    "StartDate": "2024-01-01",
                    "EndDate": "2024-01-02",
                }
            ],
        }
    )

    alarm = endpoint.get_alarms()

    # Should call _request with GET /alarms
    endpoint._request.assert_called_once_with("GET", "/alarms")

    # Should return OpenAPIUserAlarm object
    assert isinstance(alarm, OpenAPIUserAlarm)
    assert alarm.require_polling is True
    assert len(alarm.alarms) == 1
    assert alarm.alarms[0].contents == "Test Alarm"
