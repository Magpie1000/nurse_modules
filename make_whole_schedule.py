from nurse_schedune_setters import (
    generate_random_token,
    make_daily_schedule,
    check_ascendance,
    check_enough_nurse,
    check_enough_grade,
    ascend_shift
)

NURSES = 8
DAY_PER_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
nurse_grades = [0, 2, 1, 1, 2, 0, 1, 2]
nurse_last_duty = [0, 2, 1, 3, 2, 0, 3, 2]


def set_nurse_schedule(month,
                       random_token_list,
                       nurse_last_duty,
                       NURSE_GRADES,
                       grade_exceptions=0,
                       NEEDED_NURSE=4,
                       start_day=0
                       ):

    print()
    print(f'{month}월 {start_day}일 스케쥴 작성중')

    # 1. 종료 조건
    # 한 달의 마지막 날짜까지 스케쥴을 다 만들었다.
    if start_day == DAY_PER_MONTH[month]:
        # 기능 추가 -> 여기서 다 만들어진 리스트를 return하는 함수.
        print('스케쥴 작성 완료')
        return

    # 2. 생성 시작.
    # 1) 랜덤 토큰 생성
    if start_day == 0:     # 함수가 처음 시행되었다면
        random_token_list = generate_random_token(NURSES, nurse_last_duty)  # 랜덤 토큰을 생성한다.

    # 2) 임시 시간표 생성.
    temporary_schedule = make_daily_schedule(NURSES, random_token_list)

    # 3) 유효성 검사
    validation_checks = [
        check_ascendance(NURSES, temporary_schedule, nurse_last_duty),
        check_enough_nurse(temporary_schedule, NEEDED_NURSE, NURSES),
        check_enough_grade(temporary_schedule, NURSES, NURSE_GRADES)
    ]

    # 분기
    # A. 유효성 검사를 통과하지 못했을 때
    validation_check_runs = 0
    while False in validation_checks:

        # 1) 종료 조건
        if validation_check_runs > 4000:    # 4000번 이내에 만족스러운 시간표를 만들 수 없을 때
            print('유효성 검사 실패. 조건을 변경해보세요.')
            return  # 함수 실행 종료.

        # 2) 4000번까지
        # (1) 랜덤 토큰을 다시 만들고
        random_token_list = generate_random_token(NURSES, nurse_last_duty)

        # (2) 스케쥴을 다시 제작
        temporary_schedule = make_daily_schedule(NURSES, nurse_last_duty)

        # (3) 유효성 검사 결과 목록 업데이트.
        validation_checks = [
            check_ascendance(NURSES, temporary_schedule, nurse_last_duty),
            check_enough_nurse(temporary_schedule, NEEDED_NURSE, NURSES),
            check_enough_grade(temporary_schedule, NURSES, NURSE_GRADES)
        ]

    # B. 유효성 검사를 통과했을 때
    random_token_list = ascend_shift(random_token_list) # 랜덤 토큰을 업데이트.

    # 개선 필요 - 함수화 시킬것.
    for nurse in range(NURSES):
        schedule_table[nurse][start_day] = temporary_schedule[nurse]

    nurse_last_duty = temporary_schedule

    # 4. 종료
    # 다음 날의 스케쥴을 짜는 함수를 소환.
    return set_nurse_schedule(month,
                              random_token_list,
                              nurse_last_duty,
                              NURSE_GRADES,
                              grade_exceptions,
                              NEEDED_NURSE,
                              start_day + 1
                              )


schedule_table = [[-1] * 31 for _ in range(NURSES)]
set_nurse_schedule(10, [], [0, 2, 1, 3, 2, 0, 3, 2], nurse_grades)

for nurse in range(NURSES):
    print(f'GRADE{nurse_grades[nurse]} 간호사 {nurse}의 일정:{schedule_table[nurse]}')


"""
10/12 개선 필요 사항

1. 스케쥴 리스트 출력을 함수화 시킬것.
2. 변수명 통일시키기.
3. 특정 등급의 간호사가 아침, 점심, 저녁 모두 X명 있는지 확인해야 함
=> 현재는 
1) 특정 등급의 간호사가 하루에 한 명 이상 근무하는지,
2) 아침 밤 야간 모두 1명 이상의 간호사가 근무하는지
까지만 검출함. 
--> 

"""
