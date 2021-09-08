# sketched plan of action
- ## classification apps <- attributes
    - ### placement and carer attrs
<<<<<<< HEAD
        - age
        - yrs of experience/on Elder
        - type of soft preferences met 
        - location/distance
=======
        - age OK
        - yrs of experience/on Elder OK
        - type of soft preferences met OK
        - location/distance OK
>>>>>>> 569f04e (fixed fileds)
        - raw count/attributes of recent apps viewed/applied to
        - attributes of placements stayed at for more than X weeks
        - lead time end of previous placement start of the new one
        - SMS received for same placement
    - ### attrs of nearby placements
        - carers willing to apply to similar (time/location wise) placements
        - carers willing to apply to placements closer to them
    - ###interactions
- ## recommender placement attributes -> apps
- ## recommender carer attributes -> apps (cold start)

 - login OK
 - days worked WIP 
 - distance KM OK
 - NPS 

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 569f04e (fixed fileds)

 'sms_type', 
 'carer_applied_in_8hrs',
 'lead_time',
 'ongoing', 
 'max_cr_age', 
 'min_provider_rate',
 'one_off_payments_total',
 'carer_worked_in_7_days',
 'carer_worked_in_30_days'
 'has_wifi', 
 'carer_logged_in_7_days',


 'licence_needed', 
 'car_needed', 


 'moving_handling', 
 'dementia',
 'mental_health_issues',
 'hoist',
 'parkinsons', 
 'stroke',
 'alzheimers',
 'stoma', 
 'diabetes', 
 'peg', 

 'smoking',
'smokingClientsExclusion'

 'petsExclusion_CATS', 
 'petsExclusion_DOGS',
 'has_pets',

 'recipientNumberExclusion_2CRs',
 'has_two_crs',


 'ethnicities_at_risk_WHITE_ALL',
 'ethnicities_at_risk_MIXED_ALL',
 'ethnicities_at_risk_BLACK_ALL',
 'ethnicities_at_risk_ASIAN_ALL',
 'ethnicities_at_risk_ARAB_ALL',
 'ethnicityExclusion_ARAB_ALL',
 'ethnicityExclusion_ASIAN_ALL', 
 'ethnicityExclusion_BLACK_ALL',
 'ethnicityExclusion_MIXED_ALL',
 'ethnicityExclusion_WHITE_ALL',

 'genderExclusion_MALE', 
 'recipient_1_male',

 'distance_km', 
 'maxDistance_50', 
 'maxDistance_100',
 'maxDistance_400',


dates and join on interval

<<<<<<< HEAD
=======
=======
'latitude', 'longitude', set_at, match_request_id, subset excl


onehot 'sms_type', 
'lead_time', log and exp lead_time,
'ongoing', 
'min_provider_rate' or brackets,
'one_off_payments_total',
'licence_needed' with has_licence,
'car_needed' with has_car,
'moving_handling' with carer_mh,
'dementia',
'mental_health_issues',
'hoist',
'parkinsons',
'stroke',
'alzheimers',
'stoma',
'diabetes',
'peg',
'has_wifi',
'smoking' with no 'smokingClientsExclusion',
'has_dogs' with no 'petsExclusion_DOGS',
'has_cats' with no 'petsExclusion_CATS',
,
'has_two_crs' with 'recipientNumberExclusion_2CRs',
'max_cr_age',
'recipient_1_male' with 'genderExclusion_MALE',
'ethnicities_at_risk_WHITE_ALL',
'ethnicities_at_risk_MIXED_ALL',
'ethnicities_at_risk_BLACK_ALL',
'ethnicities_at_risk_ASIAN_ALL',
'ethnicities_at_risk_ARAB_ALL', 
'carer_logged_in_7_days',
'ethnicityExclusion_ARAB_ALL',
'ethnicityExclusion_ASIAN_ALL',
'ethnicityExclusion_BLACK_ALL',
'ethnicityExclusion_MIXED_ALL',
'ethnicityExclusion_WHITE_ALL',
'maxDistance_50',
'maxDistance_100',
'maxDistance_400',
'distance_km' in miles,
'carer_worked_in_7_days',
'carer_worked_in_30_days'



>>>>>>> c747ff2 (removed data from git & uninstalled lfs)
>>>>>>> 569f04e (fixed fileds)
