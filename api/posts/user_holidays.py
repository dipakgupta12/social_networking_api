import holidays
from datetime import date

def is_today_holiday_in_user_country(country):
    if country:
        country_holidays = holidays.CountryHoliday(country.title())
        return date.today() in country_holidays
    else:
        return False
