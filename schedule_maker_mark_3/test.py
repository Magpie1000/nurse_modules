from CustomModules.Classes.ScheduleManager import ScheduleManager
import time

example_team_list = [1, 2, 3]

example_nurse_profile = {
    1: [1, 0, 1, 0],
    2: [2, 1, 1, 0],
    3: [3, 2, 1, 0],
    4: [4, 0, 1, 0],
    5: [5, 1, 1, 0],
    6: [6, 2, 1, 0],
    7: [7, 0, 2, 0],
    8: [8, 1, 2, 0],
    9: [9, 2, 2, 0],
    10: [10, 0, 2, 0],
    11: [11, 1, 2, 0],
    12: [12, 2, 2, 0],
    13: [13, 0, 3, 0],
    14: [14, 1, 3, 0],
    15: [15, 2, 3, 0],
    16: [16, 0, 3, 0],
    17: [17, 1, 3, 0],
    18: [18, 2, 3, 0],
    19: [19, 2, 1, 0],
    20: [20, 2, 2, 0],
    21: [21, 2, 1, 0],
    22: [22, 2, 2, 0],
    23: [23, 2, 3, 0],
    24: [24, 2, 3, 0],

}

example_nurse_last_schedule = {
    1: [1, 1, 0, 0, 1, 2, 3, 3, 3, 0, 0, 2, 3, 3, 3, 0, 0, 0, 2, 3, 3, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0],
    3: [1, 1, 0, 0, 1, 2, 3, 3, 3, 0, 0, 2, 3, 3, 3, 0, 0, 0, 2, 3, 3, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0],
    2: [0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 1, 2, 0, 0, 2, 2, 0, 0, 2, 0, 0, 1, 1, 1, 1, 1, 0, 0, 2],
    4: [3, 3, 0, 0, 0, 1, 2, 0, 0, 3, 3, 3, 0, 0, 0, 3, 3, 0, 0, 2, 0, 0, 2, 2, 0, 0, 3, 0, 0, 1, 1],
    5: [2, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 0, 0, 0, 2, 2, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 0, 3, 3, 0],
    6: [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 3, 0, 0, 0, 2, 3, 3, 0, 0, 0, 3, 0, 0, 3],
    7: [1, 0, 0, 2, 0, 0, 3, 3, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 3, 3, 0, 0, 2, 2, 2, 3, 0, 0, 1, 1, 0],
    8: [0, 2, 2, 3, 3, 3, 0, 0, 3, 0, 0, 0, 3, 3, 0, 0, 2, 2, 0, 0, 1, 1, 1, 1, 3, 0, 0, 3, 0, 0, 1],
    9: [2, 0, 0, 1, 2, 0, 0, 0, 1, 2, 2, 0, 0, 2, 0, 0, 3, 3, 0, 0, 3, 3, 3, 0, 0, 2, 2, 2, 2, 0, 0],
    10: [0, 1, 1, 0, 0, 0, 0, 0, 2, 3, 0, 0, 1, 1, 1, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 1, 3, 0, 0],
    11: [0, 0, 3, 0, 0, 2, 2, 2, 0, 0, 1, 1, 2, 0, 0, 3, 0, 0, 1, 2, 2, 0, 0, 0, 1, 1, 1, 0, 0, 3, 3],
    12: [3, 3, 0, 0, 1, 1, 1, 1, 0, 0, 3, 3, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 2, 2],
    13: [3, 3, 3, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 2, 2],
    14: [2, 2, 2, 2, 2, 0, 0, 3, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 3, 0, 0, 0, 1, 1, 1],
    15: [0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 2, 3, 0, 0, 2, 0, 0, 0, 2, 3, 0, 0, 0],
    16: [1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 2, 3, 3, 0, 0, 0, 2, 3, 3, 3, 0, 0, 0, 1, 3, 3, 3],
    17: [0, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 2, 2, 2, 0, 0, 1, 0, 0, 2, 3, 0, 0, 2, 2, 3, 3, 0, 0, 0, 0],
    18: [0, 0, 0, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 2, 2, 2, 0, 0, 1, 1, 1, 0, 0, 1, 1, 2, 2, 0, 0],
    19: [3, 3, 3, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 2, 2],
    20: [0, 0, 3, 0, 0, 2, 2, 2, 0, 0, 1, 1, 2, 0, 0, 3, 0, 0, 1, 2, 2, 0, 0, 0, 1, 1, 1, 0, 0, 3, 3],
    21: [2, 0, 0, 1, 2, 0, 0, 0, 1, 2, 2, 0, 0, 2, 0, 0, 3, 3, 0, 0, 3, 3, 3, 0, 0, 2, 2, 2, 2, 0, 0],
    22: [0, 1, 1, 0, 0, 0, 0, 0, 2, 3, 0, 0, 1, 1, 1, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 1, 3, 0, 0],
    23: [0, 0, 3, 0, 0, 2, 2, 2, 0, 0, 1, 1, 2, 0, 0, 3, 0, 0, 1, 2, 2, 0, 0, 0, 1, 1, 1, 0, 0, 3, 3],
    24: [3, 3, 0, 0, 1, 1, 1, 1, 0, 0, 3, 3, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 2, 2],
}

starttime  = time.time()
example_date = '2021-11-01'
current_month = ScheduleManager(team_number_list=example_team_list)
current_month.push_nurse_info(example_nurse_profile)
current_month.push_last_schedules(example_nurse_last_schedule)
current_month.set_needed_nurses_by_team(2)
current_month.create_monthly_schedule(date=example_date)

for row in current_month.get_stack():
    print(row)
for key, value in current_month.get_whole_schedule().items():
    print(key, value)



print(current_month.nurses_team_dict)
print(current_month.team_nurse_dict)

endtime = time.time()

print(f'실행시간 {(endtime - starttime)*1000} ms')