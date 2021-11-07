



nurse_profile_dict = get_nurse_info(pk_list=example_nurse_pk_list)
nurse_schedule_dict = get_last_schedule(pk_list=example_nurse_pk_list)

dict_duties, modified_nurse_info = make_monthly_schedule(
    team_list=[1, 2, 3],
    needed_nurses_shift_by_team=1,
    vacation_info=[],
    current_month=int(month),
    current_date=1,
    nurse_profile_dict= nurse_profile_dict,
    nurse_last_month_schedule_dict=nurse_schedule_dict,    
    )