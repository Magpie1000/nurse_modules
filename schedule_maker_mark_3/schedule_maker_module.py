from heapq import heappop, heappush
from collections import deque
from schedule_maker_classes import PriorityRawData
import random
from schedule_maker_classes import PriorityRawData
from pprint import pprint

"""
구현 완료
"""
# def make_ideal_counter(needed_nurses_per_shift):
#     """
#     매개변수: 한 근무당 한 팀에서 필요한 간호사의 인원 수 N
#     출력: 리스트 == [0, N, N, N]
#     """
#     counter_list = [0] + [needed_nurses_per_shift] * 3
#     return counter_list


def make_daily_schedule(
    nurse_pk_list,
    nurse_info,
    ideal_schedule, 
    current_date
    ):
    """
    매개 변수 : 
    1. 현재 근무중인 간호사들의 pk_list 
    2. 간호사 정보 dict
    3. make_ideal_counter 함수의 실행 결과값.
    4. current_date : 오늘. 

    반환값:
    1. 제작 성공시 - 일간 스케쥴
    2. 실패시 - None
    """

    # 1. 종료조건 설정
    IDEAL_SCHEDULE = ideal_schedule
    
    # 2. 큐 제작
    priority_que = make_priority_que(
        nurse_pk_list,
        nurse_info,
        current_date
        )

    # 3. 큐를 활용해 스케쥴 제작
    daily_schedule, grade_checker = place_shifts(priority_que, IDEAL_SCHEDULE)

    # 4. 검증
    return daily_schedule, grade_checker


# 우선순위 큐 제작 함수.
def make_priority_que(nurse_pk_list, nurse_info, current_date):

    shift_que = []

    for nurse_pk in nurse_pk_list:
        nurse_detail = nurse_info[nurse_pk]
        for shift in range(4):
            
            priority = check_priority(nurse_detail, current_date, shift)

            if priority is not None:
                nurse_grade = nurse_detail[1]
                heappush(shift_que, (priority, nurse_pk, nurse_grade, shift)) 

    return shift_que


def check_priority(
    nurse_detail,
    current_date,
    shift
):
    """
    매개변수
    nurse_detail: ProrityRawData객체.
    """
    CURRENT_DAY = current_date
    CURRENT_SHIFT = shift

    # 1. 예외 처리
    # 1) 주 5회 이상 근무 
    if nurse_detail.shift_streaks >= 5 and CURRENT_SHIFT:
        return None
    
    # 2) NIGHT 8회 이상 근무 시도.
    # '부득이한 근무.. 조건 추가시 변경 필요.
    if nurse_detail.monthly_night_shift > 7 and CURRENT_SHIFT == 3:
        return None

    # 3) 비 오름차순 근무
    if CURRENT_SHIFT and nurse_detail.last_shift > CURRENT_SHIFT:
        return None

    # 4) 휴가 전날 NIGHT 근무

    # 2. off가 꼭 필요한 경우.
    # 1) 이틀 연속으로 쉬게 해주기. 
    if nurse_detail.off_streaks == 1 and not CURRENT_SHIFT:
        priority_token = random.randrange(1, 40)
        return priority_token

    # 2) 5연속 근무 이후 휴무
    if nurse_detail.shift_streaks >= 5 and not CURRENT_SHIFT:
        priority_token = random.randrange(1, 40)
        return priority_token

    # 3. 기타 연속 근무
    if CURRENT_SHIFT and nurse_detail.last_shift == CURRENT_SHIFT:
        priority_token = random.randrange(100, 500)
        return priority_token

    # 4. 그 외의 근무
    # 원래는 1000~ 1200. 수정해보자.. 
    if CURRENT_SHIFT:
        priority_token = random.randrange(150, 600)
        return priority_token

    else:   # 조건 없는 off. 원래는 1000 상수로 리턴했음. 
        priority_token = 700
        return priority_token


# def place_shifts(
#     priority_que,
#     ideal_schedule,
# ):
#     """
#     매개변수:
#     1. priority_que : 우선순위 큐
#     2. ideal_schedule: 한 shift당 한 팀에서 제공해야 하는 간호사 수.
    
#     반환값:
#     1. schedule_table : 스케쥴 테이블
#     2. grade_counter_bit : 저연차 간호사만 근무하는 것을 방지하기 위한 비트값. 
#     """
#     IDEAL_SCHEDULE = ideal_schedule
#     schedule_table = [[] for _ in range(4)] # 각각 off, day, evening, night.
#     current_schedule_counter = [0] * 4
#     # 비트마스킹을 활용, day, evening, night 에 근무자가 있는지 체크. 
#     grade_counter_bit = 0
#     placed_nurse_set = set()

#     while priority_que:
#         current_priority, nurse_number, nurse_grade, shift = heappop(priority_que)
        
#         # 휴가 제외, 현재 확인중인 shift 가 꽉 차있으면..
#         # 더 이상 근무를 배치하지 않음.
#         if shift and current_schedule_counter[shift] >= IDEAL_SCHEDULE[shift]:
#             continue
        
#         # 이미 배치된 간호사라면
#         if nurse_number in placed_nurse_set:
#             continue
        
#         current_schedule_counter[shift] += 1
#         schedule_table[shift].append(nurse_number)
#         placed_nurse_set.add(nurse_number)

#         # 간호사 grade가 1 이상이라면
#         # 비트에 1번...  
#         if nurse_grade > 0:
#             grade_counter_bit |= (1 << shift)
        
#     return schedule_table, grade_counter_bit


def update_nurse_infos(nurse_infos, temporary_schedule):
    """
    매개변수:

    nurse_infos: 딕셔너리.
    ㄴ key: nurse_pk
    ㄴ value: PriorityRawData 객체

    temporary_schedule:
    ㄴ 임시 스케쥴.

    출력: 업데이트된 nurse_info
    """

    # 모든 4개의 시프트를 순회하며    
    for shift in range(4):
        # 모든 간호사들 순회.
        for nurse_pk in temporary_schedule[shift]:
            nurse_infos[nurse_pk].update_self(shift)
            
    return nurse_infos



# counter_sorted_list를 개인별 딕셔너리 형태로 출력물을 전환하는 함수.
def transfer_table_to_dict(team_list, whole_schedule, nurse_pk_list, days_of_month):
    """
    연결리스트 형식으로 정렬된 스케쥴 리스트를 입력받아
    KEY는 간호사의 PK, Value는 개인의 한 달 스케쥴 리스트인 
    dict 개체를 반환하는 함수
    """

    result_dict = dict()
    # 팀 넘버마다 값을 받을 딕셔너리.. 추가. 
    for team_number in team_list:
        result_dict[team_number] = dict()

    for team_number in team_list:
        nurse_pk_by_team = nurse_pk_list[team_number]
        for nurse_pk in nurse_pk_by_team:
            result_dict[team_number][nurse_pk] = [0] * (days_of_month)
        # 인덱스 어떻게 맞출건지 협의 필. 

        for date in range(days_of_month):
            daily_schedule = whole_schedule[date][team_number]
            for shift in range(1, 4):
                for nurse in daily_schedule[shift]:
                    result_dict[team_number][nurse][date] = shift


    return result_dict


"""
push nurse info, push current schedule 두 개로 분화. 
"""
# # 분할 부분. 
# def divide_nurse_info_by_team(
#     team_list,
#     nurse_profile_dict,
#     last_months_schedule_dict
#     ):

#     """
#     매개변수:
#     0. team_list: 제작을 원하는 팀 번호가 담긴 리스트. 
#     1. nurse_profile_dict: view 함수 중 get_nurse_info의 출력값.
#     ㄴ key = pk
#     ㄴ value = [pk, level, team, off_cnt]
#     2. nurse_last_months_schedule_dict: get_last_schedule의 출력값.
#     ㄴ key = pk
#     ㄴ value = [한 달 개인 듀티표]

#     출력값:
#     Key: 팀 번호들
#     value: 딕셔너리. 
#     ㄴ key: 팀별 간호사 pk
#     ㄴ value: 팀별 간호사 PriorityRawData 객체.  
#     """
#     # 1. 선언
#     # 출력을 위한 dict 선언.
#     nurse_info_by_team = dict()
#     nurse_pk_by_team = dict()
#     for team_number in team_list:
#         nurse_info_by_team[team_number] = dict()
#         nurse_pk_by_team[team_number] = list()
    
#     # 2. 연산
#     for nurse_detail in nurse_profile_dict.values():
#         personal_data = PriorityRawData()

#         # 1) profile_dict에서 가져오는 부분
#         personal_data.nurse_pk = nurse_pk = nurse_detail[0]
#         personal_data.nurse_grade = nurse_detail[1]
#         personal_data.team_pk = nurse_team = nurse_detail[2]
#         personal_data.offs = nurse_detail[3]

#         # 2) schedule_dict에서 가져오는 부분.
#         last_month_schedule = last_months_schedule_dict[nurse_pk]
#         personal_data.fill_last_weeks_schedule(last_month_schedule)
#         personal_data.find_last_shift()
#         personal_data.find_off_streaks()

#         # 3) 딕셔너리에 삽입
#         nurse_pk_by_team[nurse_team].append(nurse_pk)
#         nurse_info_by_team[nurse_team][nurse_pk] = personal_data

#     return nurse_info_by_team, nurse_pk_by_team





