from celery import shared_task
from .models import UserLocationDetail, User
from .user_holidays import is_today_holiday_in_user_country


@shared_task
def save_user_ip_location_holiday(geolocation, user_id):
    print("save_user_ip_location_holiday - Started")
    location_detail = {
        "user": User.objects.get(pk=user_id),
        "ip": geolocation["ip"],
        "country": geolocation["county"]["name"],
        "geo": geolocation["geo"],
        "is_holiday": is_today_holiday_in_user_country(geolocation["county"]["name"])
    }
    UserLocationDetail.objects.create(**location_detail)
    print("save_user_ip_location_holiday - End")
