from driver import driver
import time
from constants import AccountSwitchCooldown, Accounts

i = 1
count = 0
while True:
    if i > len(Accounts):
        i = 1
    try:
        if driver(i) == True:
            count+=1
            time.sleep(AccountSwitchCooldown)
    except Exception as e:
        print("Driver Failed for {}".format(i))   
    i+=1
    if (i > len(Accounts) and count == 0):
        print("No accounts available")
        break
    if (i > len(Accounts) and count > 0):
        count = 0

print(count)