def convert_date(date):

    if date[5:7] == "01":
        month = "Janurary"
    elif date[5:7] == "02":
        month = "Feburary"
    elif date[5:7] == "03":
        month = "March"
    elif date[5:7] == "04":
        month = "April"
    elif date[5:7] == "05":
        month = "May"
    elif date[5:7] == "06":
        month = "June"
    elif date[5:7] == "07":
        month = "July"
    elif date[5:7] == "08":
        month = "August"
    elif date[5:7] == "09":
        month = "September"
    elif date[5:7] == "10":
        month = "October"
    elif date[5:7] == "11":
        month = "November"
    elif date[5:7] == "12":
        month = "December"
    else:
        raise Exception("No month")

    if date[8] == 0:
        day = date[8]
    else:
        day = date[8:10]

    if day[0] == "0":
        day = day[1:]

    if int(date[11:13]) > 12:
        time = f"{int(date[11:13]) - 12}{date[13:16]}pm"
    elif date[11:13] == "00":
        time = f"12{date[13:16]}am"
    else:
        time = f"{date[11:16]}am"

    if time[0] == "0":
        time = time[1:]

    return f"last updated at {time} on {month} {day}, {date[:4]}"