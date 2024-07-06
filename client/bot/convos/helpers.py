from datetime import datetime

def parse_event(event_str):
    date_str, event_name = event_str.split(" ", 1)
    # check if date_str is in yyyy-mm-dd format. If it is not, ValueError will be raised
    datetime.strptime(date_str, '%Y-%m-%d')
    return date_str, event_name

def check_month(date_str):
    # check if date_str is in yyyy-mm format. If it is not, ValueError will be raised
    datetime.strptime(date_str, '%Y-%m')
    return date_str

def events_to_md(data, month_str):
    year = int(month_str[0:4])
    month = int(month_str[5:7])
    reply = ""
    for day_str in data:
        day = int(day_str)
        date = datetime(year, month, day)
        date_str = date.strftime("%Y-%m-%d").replace("-", "\-")  #escape hyphen
        day_of_week = date.strftime('%a')
        reply += f"*{date_str} \({day_of_week}\)* \n"
        for event in data[day_str]:
            reply += f"{event["event_name"]} \n"
        reply += "\n" 
        print(reply)
    return reply

def check_day(date_str):
    # check if date_str is in yyyy-mm-dd format. If it is not, ValueError will be raised
    datetime.strptime(date_str, '%Y-%m-%d')
    return date_str



