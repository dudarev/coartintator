from coartintator.downloading_strategy.youtube import get_video_id


def test_get_video_id():
    # Test case 1: YouTube short URL
    url1 = "https://youtu.be/2_uyZ7XEt58?si=7rsh-ee9hS1450qD"
    assert get_video_id(url1) == "2_uyZ7XEt58"

    # Test case 2: YouTube long URL with watch path
    url2 = "https://www.youtube.com/watch?v=2_uyZ7XEt58&ab_channel=Every"
    assert get_video_id(url2) == "2_uyZ7XEt58"

    # Test case 3: YouTube long URL with embed path
    url3 = "https://www.youtube.com/embed/2_uyZ7XEt58?si=hH8PE5x20DcvwKAS"
    assert get_video_id(url3) == "2_uyZ7XEt58"

    # Test case 4: YouTube long URL with v path
    url4 = "https://www.youtube.com/v/2_uyZ7XEt58"
    assert get_video_id(url4) == "2_uyZ7XEt58"

    # Test case 5: Invalid YouTube URL
    url5 = "https://www.example.com"
    assert get_video_id(url5) is None
