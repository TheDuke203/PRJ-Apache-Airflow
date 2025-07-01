import os
import datetime

def BackupCleanup(location: str, prefix: str, suffix: str = ""):
    files = os.listdir(location)
    files = list(filter(lambda file: file.startswith(prefix) , files))

    if suffix != "":
        dates = list(map(lambda file: datetime.datetime.strptime(file[len(prefix) : -1 * len(suffix)],"%Y-%m-%d"), files))
    else:
        dates = list(map(lambda file: datetime.datetime.strptime(file[len(prefix):],"%Y-%m-%d"), files))
        
    dates = sorted(dates)
    while len(dates) > 2:
        fileToDelete = prefix + dates[0].strftime('%Y-%m-%d') + suffix
        os.remove(location + "/" + fileToDelete)
        dates.pop(0)