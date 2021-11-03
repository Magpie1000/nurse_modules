from schedule_maker_module import (
    make_daily_schedule,
    make_ideal_counter,
    update_nurse_info,
    transfer_table_to_dict,
    divide_nurse_info_by_team
)

from validation_checker_module import (
    check_validation
)

from pprint import pprint
import time

MONTHS_LAST_DAY = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def make_monthly_schedule(
    team_list, # -1. 팀 정보. 리스트. 
    nurse_pk_list,  # 0. 간호사 PK 정보. 
    needed_nurses_shift_by_team,    # 3. shift당 필요한 간호사 수. 3의 배수로 기입 필수. 
    vacation_info,          # 4.연차 신청 정보. [딕셔너리. nurse_pk : set(날짜 묶음)]
    current_month,          # 5. 현재 월
    current_date,            # 6. 현재 날짜
    nurse_profile_dict,         # 간호사 프로필 딕셔너리
    nurse_last_month_schedule_dict, # 지난 달 근무표
):

    """
    매개변수:
    0. team_list. list 형태로 팀 정보를 받는다.
    1. nurse_pk_list. list. 현재 근무중인 간호사의 pk를 리스트 형태로 입력.
    2. number_of_nurses. int. 간호사 인원 수.
    3. needed_nurses_shift_by_team. int. shift당 한 팀에 필요한 간호사 수.
    4. vacation_info. dict. key = 간호사, value = set 혹은 list로 '날짜' 정보
    5. current_month = 생성 시작을 원하는  월
    6. current_date = 생성 시작을 원하는 날짜.  
    """

    # 1. 선언
    # 1) 최종 결과값을 저장할 리스트 .
    whole_schedule = []
    NUMBER_OF_NURSES = len(nurse_pk_list)
    NUMBER_OF_TEAMS = len(team_list)

    # 2) 예외 처리를 위한 변수들 선언
    # (1) 이전 시점의 nurse_info정보를  저장하는 스택
    nurse_info_stack = [[] for _ in range(NUMBER_OF_TEAMS + 1)]   
    # (2) 무한루프 방지를 위한 변수.
    recursion_time = 0

    # 2. 연산
    # 1) 연산 전 준비
    # nurse_profile_dict 자료형 맞춰야 함. 
    ideal_schedule = make_ideal_counter(needed_nurses_shift_by_team)
    nurse_info, nurse_pk_list = divide_nurse_info_by_team(
        team_list=team_list,
        nurse_profile_dict=nurse_profile_dict,
        nurse_last_months_schedule_dict=nurse_last_month_schedule_dict
    )
    pprint(nurse_info)
    pprint(nurse_pk_list)


    # 이 부분을 위의 함수에서 실제로 받아오는 방식대로 처리해야 한다. 
    # nurse_pk_list = example_nurse_pk_dict
    # 1. 종료 조건
    # 정상 종료
    while current_date != MONTHS_LAST_DAY[current_month] + 1:

        # 2. 선언
        # 비트마스킹 형태로 grade의 참여 여부 확인. 
        whole_team_temp_schedule = []

        # 2. 스케쥴 생성
        # 팀별 스케쥴 제작 및 검증 알고리즘 필요함. 제작중. 
        is_enough_grade = False

        while not is_enough_grade and recursion_time < 15:

            teamed_up_schedule = dict()
            whole_team_grade_checker = 1    
            
            # 여기 매개변수로 팀별 인원수가 들어가야 함. 
            for team_number in team_list:           
                temporary_schedule, grade_counter_bit\
                    = make_daily_schedule(
                    nurse_pk_list = nurse_pk_list[team_number],
                    nurse_info = nurse_info[team_number],
                    ideal_schedule = ideal_schedule,
                    current_date = current_date
                    )
                # 팀 
                teamed_up_schedule[team_number] = temporary_schedule
                whole_team_grade_checker |= grade_counter_bit

            if whole_team_grade_checker == 15:
                whole_team_temp_schedule.append(teamed_up_schedule)
                is_enough_grade = True
                
            else:
                recursion_time += 1

        if recursion_time >= 15:
            print('설정 변경 필요')
            return 

        # 4. 스케쥴 업데이트
        for team_number in team_list:
            nurse_info[team_number] = update_nurse_info(nurse_info[team_number], teamed_up_schedule[team_number])
        whole_schedule.append(teamed_up_schedule)
        current_date += 1

    whole_schedule_dict = transfer_table_to_dict(
        team_list=team_list,
        whole_schedule=whole_schedule,
        nurse_pk_list=nurse_pk_list,
        days_of_month = MONTHS_LAST_DAY[current_month]
        )

    return whole_schedule_dict, nurse_info


"""
테스트용 -- 리스트의 각 열이 의미하는 바는 아래와 같습니다.
0 NURSE_NUMBER 간호사 일련번호
1 NURSE_GRADE 간호사 grade
2 TEAM_NUMBER 팀넘버
3 SHIFTS, 이번 달 근무 일수 
4 SHIFT_STREAKS, 연속 근무일 수 
5 OFFS, 그.. 마크다운에 있는 'OFF' 참조.
6 MONTHLY_NIGHT_SHIFTS, 한 달에 night 근무한 횟수
7 VACATION_INFO,   휴가 정보(외부 딕셔너리로 수정 예정)
8 OFF_STREAKS,         연속 휴무 
9 LAST_SHIFT,           마지막 근무 정보

+++ 팀 정보 들어가야함. 
"""


example_nurse_profile_dict = {
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
}



example_nurse_pk_dict = {
    1: [1, 2, 3, 4, 5, 6],
    2: [7, 8, 9, 10, 11, 12],
    3: [13, 14, 15, 16, 17, 18],
}

example_nurse_last_month_schedule = {
    1: [0, 2, 3, 3, 3, 3, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 1, 2, 0],
    2: [1, 1, 0, 0, 1, 2, 3, 3, 3, 0, 0, 2, 3, 3, 3, 0, 0, 0, 2, 3, 3, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0],
    3: [0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 1, 2, 0, 0, 2, 2, 0, 0, 2, 0, 0, 1, 1, 1, 1, 1, 0, 0, 2],
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
}



example_nurse_pk_list = [
    1, 2, 3, 4, 5, 6,
    7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18
    ]

start_time = time.time()


result, modified_nurse_info = make_monthly_schedule(
    team_list=[1, 2, 3],
    nurse_pk_list=example_nurse_pk_list,
    needed_nurses_shift_by_team=1,
    vacation_info=[],
    current_month=10,
    current_date=1,
    nurse_profile_dict= example_nurse_profile_dict,
    nurse_last_month_schedule_dict=example_nurse_last_month_schedule,    
    )


print('디버깅용 딕셔너리')
pprint(modified_nurse_info)
print()

for team_number in [1, 2, 3]:
    for nums in example_nurse_pk_dict[team_number]:
        print(nums, result[team_number][nums])

end_time = time.time()
print('실행 시간')
print(f'{(end_time - start_time)*1000}ms')





example_nurse_info_dict = {
    1 : {
        1: [1, 0, 1, 0, 0, 0, 0, 0, 2, 0],
        2: [2, 1, 1, 0, 0, 0, 0, 0, 2, 0],
        3: [3, 2, 1, 0, 0, 0, 0, 0, 2, 0],
        4: [4, 0, 1, 0, 0, 0, 0, 0, 2, 0],
        5: [5, 1, 1, 0, 0, 0, 0, 0, 2, 0],
        6: [6, 2, 1, 0, 0, 0, 0, 0, 2, 0]
    },

    2: {
        7: [1, 0, 2, 0, 0, 0, 0, 0, 2, 0],
        8: [2, 1, 2, 0, 0, 0, 0, 0, 2, 0],
        9: [3, 2, 2, 0, 0, 0, 0, 0, 2, 0],
        10: [4, 0, 2, 0, 0, 0, 0, 0, 2, 0],
        11: [5, 1, 2, 0, 0, 0, 0, 0, 2, 0],
        12: [6, 2, 2, 0, 0, 0, 0, 0, 2, 0],
    },

    3: {
        13: [1, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        14: [2, 1, 0, 0, 0, 0, 0, 0, 2, 0],
        15: [3, 2, 0, 0, 0, 0, 0, 0, 2, 0],
        16: [4, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        17: [5, 1, 0, 0, 0, 0, 0, 0, 2, 0],
        18: [6, 2, 0, 0, 0, 0, 0, 0, 2, 0],
    }
}