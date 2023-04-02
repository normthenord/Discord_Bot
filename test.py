import datetime

timeArr = []

for i in range(0,24):
    timeArr.append(datetime.time(hour=i, tzinfo=datetime.timezone.utc))

print([datetime.time(hour=i, tzinfo=datetime.timezone.utc) for i in range(24)])

