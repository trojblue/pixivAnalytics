from datetime import datetime
from typing import *
import inspect

def retrieve_name(var):
    """返回变量var名字的string格式
    """
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


def get_time_string():
    return datetime.now().strftime("%y.%m.%d_%H%M")



def get_hourly_time_difference(past_date, current_date):
    """计算投稿时间和爬虫开始时间之间的小时差
    past_date: string
    current_date: datetime object
    """
    # Parse the past_date string into a datetime object
    past_date = datetime.fromisoformat(past_date)

    # Calculate the difference in hours between the past_date and the current time
    difference_in_hours = (current_date - past_date).total_seconds() / 3600

    return difference_in_hours