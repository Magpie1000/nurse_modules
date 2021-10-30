from schedule_maker_module import (
    make_daily_schedule,
    make_ideal_counter,
    update_nurse_info,
    transfer_table_to_dict
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
    nurse_info,     # 1. 간호사 정보. pk가 key, value가 아래와 같은 딕셔너리.  
    needed_nurses_shift_by_team,    # 3. shift당 필요한 간호사 수. 3의 배수로 기입 필수. 
    vacation_info,          # 4.연차 신청 정보. [딕셔너리. nurse_pk : set(날짜 묶음)]
    current_month,          # 5. 현재 월
    current_date,            # 6. 현재 날짜
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

    # 2) 예외 처리를 위한 변수들 선언
    # (1) 이전 시점의 nurse_info정보를  저장하는 스택
    nurse_info_stack = []   
    # (2) 무한루프 방지를 위한 변수.
    recursion_time = 0

    NUMBER_OF_NURSES = len(nurse_pk_list)
    NUMBER_OF_TEAMS = len(team_list)

    # 2. 연산
    ideal_schedule = make_ideal_counter(needed_nurses_shift_by_team)

    # 1. 종료 조건
    # 정상 종료
    while current_date != MONTHS_LAST_DAY[current_month] + 1:

        # 2. 스케쥴 생성
        temporary_schedule = make_daily_schedule(
            nurse_pk_list = nurse_pk_list,
            nurse_info = nurse_info,
            ideal_schedule = ideal_schedule,
            current_date = current_date
            )

        # 3. 스케쥴 검증(미구현)

        # 4. 스케쥴 업데이트
        nurse_info = update_nurse_info(nurse_info, temporary_schedule)
        whole_schedule.append(temporary_schedule)

        current_date += 1

        if recursion_time >= 15:
            print('설정 변경 필요')
            return 

    # 출력 형식 변경. 
    whole_schedule_dict = transfer_table_to_dict(
        whole_schedule,
        nurse_pk_list,
        MONTHS_LAST_DAY[current_month]
        )

    return whole_schedule_dict, nurse_info

# 3. 스케쥴 검증
        # is_validate = check_validation(temporary_schedule)

        # 1) 검증 실패
        # 재작성. 
        # need_to_go_back = False
        # for _ in range(100):
        #     temporary_schedule = make_daily_schedule(nurse_info, ideal_schedule)
        #     is_validate = check_validation(temporary_schedule)    
        #     if is_validate:
        #         break
        # else:
        #     need_to_go_back = True

        # 4. 재귀
        # if need_to_go_back:
        #     recursion_time += 1
        #     return make_monthly_schedule()        



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
"""

example_nurse_info = {
    1: [1, 0, 1, 0, 0, 0, 0, 0, 2, 0],
    2: [2, 1, 1, 0, 0, 0, 0, 0, 2, 0],
    3: [3, 2, 1, 0, 0, 0, 0, 0, 2, 0],
    4: [4, 0, 1, 0, 0, 0, 0, 0, 2, 0],
    5: [5, 1, 1, 0, 0, 0, 0, 0, 2, 0],
    6: [6, 2, 1, 0, 0, 0, 0, 0, 2, 0],
    # 7: [7, 0, 0, 0, 0, 0, 2, 0],
    # 8: [8, 0, 0, 0, 0, 0, 2, 0],
    # 9: [9, 0, 0, 0, 0, 0, 0, 0],
    # 10:[10, 0, 0, 0, 0, 0, 2, 0],
    # 11: [11, 0, 0, 0, 0, 0, 2, 0],
    # 12: [12, 0, 0, 0, 0, 0, 2, 0],
    # 13: [13, 0, 0, 0, 0, 0, 2, 0]
}

example_nurse_pk_list = [1, 2, 3, 4, 5, 6] #  7, 8, 9, 10, 11, 12, 13

start_time = time.time()
result, modified_nurse_info = make_monthly_schedule(
    team_list=[1],
    nurse_pk_list=example_nurse_pk_list,
    nurse_info=example_nurse_info,
    needed_nurses_shift_by_team=1,
    vacation_info=[],
    current_month=10,
    current_date=1,    
    )
print('디버깅용 딕셔너리')
pprint(modified_nurse_info)
print()
i = 1

for nums in example_nurse_pk_list:
    print(nums, result[nums])

end_time = time.time()
print('실행 시간')
print(end_time - start_time)