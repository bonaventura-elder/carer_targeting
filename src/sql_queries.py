
training_query = '''
SELECT DISTINCT
    s.placement_ad_id,
    s.match_request_id,
    s.carer_id,
    sent_at,
    h.updated_at,
    sms_type,
    if(HOUR(TIMEDIFF(valid_from,sent_at))<8,1,0) as carer_applied_in_8hrs,
    DATEDIFF(start_date,sent_at) as lead_time,
    if(end_date IS NULL,1,0) as ongoing,
    min_provider_rate,
    one_off_payments_total,
    if(driving_requirements='LICENSE_NEEDED',1,0) as licence_needed,
    if(driving_requirements='CAR_NEEDED',1,0) as car_needed,
    if(placement_requirements regexp 'MOVING_HANDLING',1,0) as moving_handling,
    if(placement_requirements regexp 'DEMENTIA',1,0) as dementia,
    if(placement_requirements regexp 'MENTAL_HEALTH_ISSUES',1,0) as mental_health_issues,
    if(placement_requirements regexp 'HOIST',1,0) as hoist,
    if(placement_requirements regexp 'PARKINSONS',1,0) as parkinsons,
    if(placement_requirements regexp 'STROKE',1,0) as stroke,
    if(placement_requirements regexp 'ALZHEIMERS',1,0) as alzheimers,
    if(placement_requirements regexp 'STOMA',1,0) as stoma,
    if(placement_requirements regexp 'DIABETES',1,0) as diabetes,
    if(placement_requirements regexp 'PEG',1,0) as peg,
    if(has_wifi=1,1,0) as has_wifi,
    if(smoking=1,1,0) as smoking,
    if(has_pets regexp 'DOGS',1,0) as has_dogs,
    if(has_pets regexp 'CATS',1,0) as has_cats,
    if(h.service_type_id LIKE '%%2_RECIPIENTS%%',1,0) AS has_two_crs,
    DATEDIFF(sent_at,dob.max_date_of_birth)/365.25 as max_cr_age,
    if(recipient_1_gender = 'MALE',1,0) as recipient_1_male,
    if( ethnicities_at_risk regexp 'WHITE_ALL',1,0) as ethnicities_at_risk_WHITE_ALL,
    if( ethnicities_at_risk regexp 'MIXED_ALL',1,0) as ethnicities_at_risk_MIXED_ALL,
    if( ethnicities_at_risk regexp 'BLACK_ALL',1,0) as ethnicities_at_risk_BLACK_ALL,
    if( ethnicities_at_risk regexp 'ASIAN_ALL',1,0) as ethnicities_at_risk_ASIAN_ALL,
    if(ethnicities_at_risk regexp 'ARAB_ALL',1,0) as ethnicities_at_risk_ARAB_ALL,
    latitude,
    longitude
FROM
     (
         SELECT
                placement_ad_id,
                carer_id,
                sent_at,
                sms_type,
                SUBSTRING(SUBSTRING(placement_ad_id,6),1,CHAR_LENGTH(SUBSTRING(placement_ad_id,6))-5) as match_request_id
         FROM live_STATS_MATCHING_MATCH_REQUEST_CARER_SMS
         UNION
         SELECT
                placement_ad_id,
                carer_id,
                sent_at,
                sms_type,
                SUBSTRING(SUBSTRING(placement_ad_id,6),1,CHAR_LENGTH(SUBSTRING(placement_ad_id,6))-5) as match_request_id
         FROM live_MO_CUSTOM_LIST_MATCH_REQUEST_CARER_SMS
    ) s
LEFT JOIN live_STATS_MATCHING_PLACEMENT_AD_APPLICATION a
    on (s.match_request_id = a.match_request_id AND s.carer_id = a.carer_id )
LEFT JOIN live_STATS_MATCHING_PLACEMENT_AD_HISTORY h
ON (s.placement_ad_id = h.placement_ad_id)
LEFT JOIN (
    select
           mr.match_request_id,
           if(recipient_2_date_of_birth IS NOT NULL,LEAST(recipient_1_date_of_birth, recipient_2_date_of_birth),recipient_1_date_of_birth) as max_date_of_birth,
           gender as recipient_1_gender,
           ethnicities_at_risk
    from live_STATS_MATCHING_MATCH_REQUEST mr
    LEFT JOIN live_STATS_CUSTOMERS c
    on mr.account_id = c.customer_id
    LEFT JOIN live_STATS_CUSTOMERS_CARE_APPRAISAL_RECIPIENT car
    on car.account_id = mr.account_id
    ) dob
on dob.match_request_id = s.match_request_id
WHERE s.placement_ad_id IS NOT NULL AND
      sent_at<'2021-08-18' AND
      sent_at>'2019-10-01' AND
      sms_type in ('urgentMatchSent','slowMatchingSent','preferredPlacementSent',
                    'initialPromotionSent','returningCarerSent','customListSent')
    AND (h.updated_at IS NULL
        OR h.updated_at = (
            SELECT MAX(h2.updated_at)
            FROM live_STATS_MATCHING_PLACEMENT_AD_HISTORY h2
            WHERE s.placement_ad_id = h2.placement_ad_id AND
                  s.sent_at>=h2.updated_at
                    )
    )
'''

prefs_query = '''
SELECT DISTINCT
    s.carer_id,
    s.placement_ad_id,
    s.sent_at,
    set_at,
    if(ethnicityExclusion_ARAB_ALL IS NULL,0,ethnicityExclusion_ARAB_ALL) as ethnicityExclusion_ARAB_ALL,
        if(ethnicityExclusion_ASIAN_ALL IS NULL,0,ethnicityExclusion_ASIAN_ALL) as ethnicityExclusion_ASIAN_ALL,
    if(ethnicityExclusion_BLACK_ALL IS NULL,0,ethnicityExclusion_BLACK_ALL) as ethnicityExclusion_BLACK_ALL,
    if(ethnicityExclusion_MIXED_ALL IS NULL,0,ethnicityExclusion_MIXED_ALL) as ethnicityExclusion_MIXED_ALL,
    if(ethnicityExclusion_WHITE_ALL IS NULL,0,ethnicityExclusion_WHITE_ALL) as ethnicityExclusion_WHITE_ALL,
    if(genderExclusion_MALE IS NULL,0,genderExclusion_MALE) as genderExclusion_MALE,
    if(maxDistance_50 IS NULL,0,maxDistance_50) as maxDistance_50,
    if(maxDistance_100 IS NULL,0,maxDistance_100) as maxDistance_100,
    if(maxDistance_400 IS NULL,0,maxDistance_400) as maxDistance_400,
    if(petsExclusion_CATS IS NULL,0,petsExclusion_CATS) as petsExclusion_CATS,
    if(petsExclusion_DOGS IS NULL,0,petsExclusion_DOGS) as petsExclusion_DOGS,
    if(recipientNumberExclusion_2CRs IS NULL,0,recipientNumberExclusion_2CRs) as recipientNumberExclusion_2CRs,
    if(smokingClientsExclusion IS NULL,0,smokingClientsExclusion) as smokingClientsExclusion,
   if(has_licence IS NULL,0,has_licence) AS has_licence,
   if(has_car IS NULL,0,has_car) as has_car,
   if(moving_handling IS NULL,0,moving_handling) as moving_handling,
   if(dementia IS NULL,0,dementia) as dementia,
   if(mental_health_issues IS NULL,0, mental_health_issues) as mental_health_issues,
   if(hoist IS NULL,0, hoist) as hoist,
   if(parkinsons IS NULL,0, parkinsons) as parkinsons,
   if(stroke IS NULL,0, stroke) as stroke,
   if(alzheimers IS NULL,0,alzheimers) as alzheimers,
   if(stoma IS NULL,0,stoma) as stoma,
   if(diabetes IS NULL,0,diabetes) AS diabetes,
   if(peg IS NULL,0,peg) AS peg
FROM
     (
         SELECT
                placement_ad_id,
                carer_id,
                sent_at,
                sms_type,
                SUBSTRING(SUBSTRING(placement_ad_id,6),1,CHAR_LENGTH(SUBSTRING(placement_ad_id,6))-5) as match_request_id
         FROM live_STATS_MATCHING_MATCH_REQUEST_CARER_SMS
         UNION
         SELECT
                placement_ad_id,
                carer_id,
                sent_at,
                sms_type,
                SUBSTRING(SUBSTRING(placement_ad_id,6),1,CHAR_LENGTH(SUBSTRING(placement_ad_id,6))-5) as match_request_id
         FROM live_MO_CUSTOM_LIST_MATCH_REQUEST_CARER_SMS
    ) s
LEFT JOIN
    (
    select distinct
        carer_id,
        set_at,
        SUM(if(preference_name='ethnicityExclusion' and UPPER(preference_value) = 'WHITE_ALL',1 ,0)) as ethnicityExclusion_WHITE_ALL,
        SUM(if(preference_name='ethnicityExclusion' and UPPER(preference_value) = 'BLACK_ALL',1 ,0)) as ethnicityExclusion_BLACK_ALL,
        SUM(if(preference_name='ethnicityExclusion' and UPPER(preference_value) = 'MIXED_ALL',1 ,0)) as ethnicityExclusion_MIXED_ALL,
        SUM(if(preference_name='ethnicityExclusion' and UPPER(preference_value) = 'ASIAN_ALL',1 ,0)) as ethnicityExclusion_ASIAN_ALL,
        SUM(if(preference_name='ethnicityExclusion' and UPPER(preference_value) = 'ARAB_ALL',1 ,0)) as ethnicityExclusion_ARAB_ALL,
        SUM(if(preference_name='genderExclusion' AND UPPER(preference_value) = 'MALE',1,0)) as genderExclusion_MALE,
        SUM(if(preference_name='maxDistance' AND UPPER(preference_value)='ONE_HUNDRED',1,0)) as maxDistance_100,
        SUM(if(preference_name='maxDistance' AND UPPER(preference_value)='FOUR_HUNDRED',1,0)) as maxDistance_400,
        SUM(if(preference_name='maxDistance' AND UPPER(preference_value)='FIFTY',1,0)) as maxDistance_50,
        SUM(if(preference_name='petsExclusion' AND UPPER(preference_value)='DOGS',1,0)) AS petsExclusion_DOGS,
        SUM(if(preference_name='petsExclusion' AND UPPER(preference_value)='CATS',1,0)) AS petsExclusion_CATS,
        -- if(preference_name='placementTypeExclusion',UPPER(preference_value),0),
        SUM(if(preference_name='recipientNumberExclusion' AND UPPER(preference_value)='TWO_RECIPIENTS',1,0)) AS recipientNumberExclusion_2CRs,
        SUM(if(preference_name='smokingClientsExclusion' and UPPER(preference_value)='TRUE',1,0)) AS smokingClientsExclusion
    from live_STATS_CARER_PLACEMENT_PREFERENCE
    where preference_type = 'SOFT'
    group by carer_id, set_at
    ) prefs
ON (s.carer_id = prefs.carer_id and s.sent_at>=prefs.set_at)
LEFT JOIN (
    SELECT DISTINCT
        carer_id,
        if(driving='HAS_LICENCE',1,0) as has_licence,
        if(driving='HAS_OWN_CAR',1,0) as has_car,
        if(placement_requirements regexp 'MOVING_HANDLING',1,0) as moving_handling,
        if(placement_requirements regexp 'DEMENTIA',1,0) as dementia,
        if(placement_requirements regexp 'MENTAL_HEALTH_ISSUES',1,0) as mental_health_issues,
        if(placement_requirements regexp 'HOIST',1,0) as hoist,
        if(placement_requirements regexp 'PARKINSONS',1,0) as parkinsons,
        if(placement_requirements regexp 'STROKE',1,0) as stroke,
        if(placement_requirements regexp 'ALZHEIMERS',1,0) as alzheimers,
        if(placement_requirements regexp 'STOMA',1,0) as stoma,
        if(placement_requirements regexp 'DIABETES',1,0) as diabetes,
        if(placement_requirements regexp 'PEG',1,0) as peg
    FROM live_BI_CARER_PREFERENCES
) bcp
ON s.carer_id = bcp.carer_id
WHERE s.placement_ad_id IS NOT NULL AND
      sent_at<'2021-08-18' AND
      sent_at>'2019-10-01' AND
      sms_type in ('urgentMatchSent','slowMatchingSent','preferredPlacementSent',
                    'initialPromotionSent','returningCarerSent','customListSent')
    AND (prefs.set_at IS NULL
    OR prefs.set_at = (
        SELECT MAX(prefs2.set_at)
        FROM live_STATS_CARER_PLACEMENT_PREFERENCE prefs2
        WHERE s.carer_id = prefs2.carer_id
          AND s.sent_at >= prefs2.set_at
            )
    )
'''

login_query = '''
SELECT DISTINCT s.placement_ad_id,
               s.carer_id,
               sent_at,
               if(DATEDIFF(sent_at, timestamp) <= 7, 1, 0)       as carer_logged_in_7_days
FROM (
        SELECT placement_ad_id,
               carer_id,
               sent_at,
               sms_type,
               SUBSTRING(SUBSTRING(placement_ad_id, 6), 1,
                         CHAR_LENGTH(SUBSTRING(placement_ad_id, 6)) - 5) as match_request_id
        FROM live_STATS_MATCHING_MATCH_REQUEST_CARER_SMS
        UNION
        SELECT placement_ad_id,
               carer_id,
               sent_at,
               sms_type,
               SUBSTRING(SUBSTRING(placement_ad_id, 6), 1,
                         CHAR_LENGTH(SUBSTRING(placement_ad_id, 6)) - 5) as match_request_id
        FROM live_MO_CUSTOM_LIST_MATCH_REQUEST_CARER_SMS
    ) s
        LEFT JOIN (SELECT carer_id, timestamp
                   FROM live_STATS_CARER_ACCOUNT_LOGS
                   WHERE event_type = 'LOGIN' and impersonated != 1) cal
                  on (cal.carer_id = s.carer_id and sent_at >= timestamp)
WHERE s.placement_ad_id IS NOT NULL
 AND sent_at < '2021-08-18'
 AND sent_at > '2019-10-01'
 AND sms_type in ('urgentMatchSent', 'slowMatchingSent', 'preferredPlacementSent',
                  'initialPromotionSent', 'returningCarerSent', 'customListSent')
 AND cal.timestamp = (
    SELECT MAX(cal2.timestamp)
    FROM live_STATS_CARER_ACCOUNT_LOGS cal2
    WHERE s.carer_id = cal2.carer_id
      AND s.sent_at >= cal2.timestamp
    )
'''

dist_query = '''
SELECT DISTINCT
    s.placement_ad_id,
    s.carer_id,
    sent_at,
    t.distance_km
FROM
     (
         SELECT
                placement_ad_id,
                carer_id,
                sent_at,
                sms_type,
                UPPER(postcode_area) as postcode_area
         FROM live_STATS_MATCHING_MATCH_REQUEST_CARER_SMS
         LEFT JOIN live_STATS_PROFESSIONAL p
            on p.professional_id = carer_id
         UNION
         SELECT
                placement_ad_id,
                carer_id,
                sent_at,
                sms_type,
                UPPER(postcode_area) as postcode_area
         FROM live_MO_CUSTOM_LIST_MATCH_REQUEST_CARER_SMS
         LEFT JOIN live_STATS_PROFESSIONAL p
            on p.professional_id = carer_id
    ) s
LEFT JOIN live_STATS_MATCHING_PLACEMENT_AD h
ON (s.placement_ad_id = h.placement_ad_id)
LEFT JOIN (SELECT * from BI_POSTCODE_AREA_TRAVEL_TIME where travel_method = 'transit') t
    on (t.from = s.postcode_area AND t.to = if(h.postcode_sector REGEXP'[A-Z][A-Z]',substring(h.postcode_sector,1,2),substring(h.postcode_sector,1,1)))
WHERE s.placement_ad_id IS NOT NULL AND
      sent_at<'2021-08-18' AND
      sent_at>'2019-10-01' AND
      sms_type in ('urgentMatchSent','slowMatchingSent','preferredPlacementSent',
                    'initialPromotionSent','returningCarerSent','customListSent')
'''

worked_query = '''
SELECT DISTINCT s.placement_ad_id,
               s.match_request_id,
               s.carer_id,
               sent_at,
               start_date_time,
                if(DATEDIFF(sent_at, start_date_time) <= 7, 1, 0)       as carer_worked_in_7_days,
               if(DATEDIFF(sent_at, start_date_time) <= 30, 1, 0)       as carer_worked_in_30_days
FROM (
        SELECT placement_ad_id,
               carer_id,
               sent_at,
               sms_type,
               SUBSTRING(SUBSTRING(placement_ad_id, 6), 1,
                         CHAR_LENGTH(SUBSTRING(placement_ad_id, 6)) - 5) as match_request_id
        FROM live_STATS_MATCHING_MATCH_REQUEST_CARER_SMS
        UNION
        SELECT placement_ad_id,
               carer_id,
               sent_at,
               sms_type,
               SUBSTRING(SUBSTRING(placement_ad_id, 6), 1,
                         CHAR_LENGTH(SUBSTRING(placement_ad_id, 6)) - 5) as match_request_id
        FROM live_MO_CUSTOM_LIST_MATCH_REQUEST_CARER_SMS
    ) s
        LEFT JOIN  live_STATS_NON_CANCELLED_VISITS ncv
                  on (ncv.professional_id = s.carer_id and sent_at >= start_date_time)
WHERE s.placement_ad_id IS NOT NULL
 AND sent_at < '2021-08-18'
 AND sent_at > '2019-10-01'
 AND sms_type in ('urgentMatchSent', 'slowMatchingSent', 'preferredPlacementSent',
                  'initialPromotionSent', 'returningCarerSent', 'customListSent')
 AND ncv.start_date_time = (
    SELECT MAX(ncv2.start_date_time)
    FROM live_STATS_NON_CANCELLED_VISITS ncv2
    WHERE s.carer_id = ncv2.professional_id
      AND s.sent_at >= ncv2.start_date_time
    )
'''

