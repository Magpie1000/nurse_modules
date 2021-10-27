#  10/26 오후 1시 이전까지 작성한 내용. 

from schedule_maker_module import (
    make_daily_schedule,
    make_ideal_counter
)

from validation_checker_module import (
    check_validation
)

MONTHS_LAST_DAY = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
NUMBER_OF_NURSES = 32


def make_monthly_schedule(
    nurse_info,     # 1. 간호사 정보 - 이걸 어떻게 받을지가 관건. 
    number_of_nurses,       # 2. 간호사 인원 수 
    needed_nurses_per_shift,    # 3. shift당 필요한 간호사 수. 3의 배수로 기입 필수. 
    vacation_info,          # 4.연차 신청 정보. [딕셔너리. nurse_pk : set(날짜 묶음)]
    current_month,          # 5. 현재 월
    current_day,            # 6. 현재 날짜
):

    whole_schedule = []
    recursion_time = 0
    ideal_schedule = make_ideal_counter(needed_nurses_per_shift)

    # 1. 종료 조건
    # 정상 종료
    while current_day != MONTHS_LAST_DAY[current_month] + 1:

        # 2. 스케쥴 생성
        temporary_schedule = make_daily_schedule(nurse_info, ideal_schedule=ideal_schedule)
        
        # 3. 스케쥴 검증
        # is_validate = check_validation(temporary_schedule)

        # 1) 검증 실패
        # 재작성. 
        need_to_go_back = False
        for _ in range(100):
            temporary_schedule = make_daily_schedule(nurse_info, ideal_schedule)
            is_validate = check_validation(temporary_schedule)    
            if is_validate:
                break
        else:
            need_to_go_back = True

        # 4. 재귀
        if need_to_go_back:
            recursion_time += 1
            return make_monthly_schedule()
        
        else:
            current_day += 1

        if recursion_time >= 15:
            print('설정 변경 필요')
            return 

example_nurse_info = [
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [3, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [4, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [5, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [6, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [7, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [8, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [10, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [11, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [12, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [13, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1]
]


make_monthly_schedule(
    nurse_info=example_nurse_info,
    number_of_nurses=13,
    needed_nurses_per_shift=3,
    vacation_info=[],
    current_month=10,
    current_day=25,    
    )

