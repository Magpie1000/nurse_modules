import random
from datetime import date
"""
number_of_nurses: 간호사 총 인원 수

last_duties: 이전 근무 기록을 담은 리스트.
인덱스는 간호사 번호, 값은 스케쥴을 의미함.

today_schedule: 현재 근무 기록을 담은 리스트.



"""


def generate_random_token(number_of_nurses, last_duties):

    nurse_generator_token = [0] * number_of_nurses

    for nurse in range(number_of_nurses):
        token = last_duties[nurse] + random.random() + random.random()
        nurse_generator_token[nurse] = token

    return nurse_generator_token


def check_ascendance(number_of_nurses, today_schedule, last_duties):
    print('checking ascendance')
    print(today_schedule)

    for nurse in range(number_of_nurses):
        if today_schedule[nurse] != 0\
                and today_schedule[nurse] < last_duties[nurse]:

            print(f'{nurse}의 오름차순 근무 불가')
            return False

    print()
    return True


def ascend_shift(schedule_token_list):

    for i in range(len(schedule_token_list)):
        schedule_token_list[i] += 1

    return schedule_token_list


def make_daily_schedule(number_of_nurses, random_token_list):
    # 이후 구현할 것 = day_off_list 받아서..

    daily_schedule = [-1] * number_of_nurses

    for nurse in range(number_of_nurses):
        daily_schedule[nurse] = int(random_token_list[nurse] % 4)

    print(daily_schedule)
    return daily_schedule


def check_enough_grade(today_schedule, number_of_nurses, nurse_grade, exceptions=0):
    # 모든 등급의 간호사가 1 명 이상 근무할 때.

    grade_zeros = 0
    grade_ones = 0
    grade_twos = 0

    for i in range(number_of_nurses):
        if not today_schedule[i]:
            continue

        if nurse_grade[i] == 0:
            grade_zeros += 1

        elif nurse_grade[i] == 1:
            grade_ones += 1

        elif nurse_grade[i] == 2:
            grade_twos += 1

    if grade_ones and grade_ones and grade_twos:
        return True

    return False


def check_enough_nurse(today_schedule, needed_nurse, number_of_nurses):
    nurse_counter = 0
    print('checking enough nurses....')
    print(number_of_nurses)
    print(today_schedule)

    day_worker = 0
    afternoon_worker = 0
    night_worker = 0

    for nurse in range(number_of_nurses):

        if today_schedule[nurse] == 1:
            day_worker += 1

        elif today_schedule[nurse] == 2:
            afternoon_worker += 1

        elif today_schedule[nurse] == 3:
            night_worker += 1

    if day_worker and afternoon_worker and night_worker:
        return True

    print('근무 인원 부족')
    return False
    # print(f'필요 인원: {needed_nurse}')
    # if nurse_counter < needed_nurse:
    #     print(f"오늘 근무 인원 {needed_nurse - nurse_counter} 부족")
    #     return False
    #
    # if nurse_counter == needed_nurse:
    #     print(f"오늘 근무 인원 충분")
    #
    # if nurse_counter > needed_nurse:
    #     print(f"인원 {nurse_counter - needed_nurse}명 초과 근무")

