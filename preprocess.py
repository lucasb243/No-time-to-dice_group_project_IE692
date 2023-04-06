import pandas as pd
# Load raw data & Preprocess DataFrame (enrich with derived attributes)
log = 'bpic15_time_manipulated'

preprocess = True

if preprocess:
    fn = f'data/raw/{log}.csv'
else:
    fn = f'data/processed/{log}.csv'

if preprocess:
         
    if log == 'bpic15' or log == 'bpic15_time_manipulated':
        df = pd.read_csv(fn)[[
            'case:concept:name', 'activityNameEN', 'org:resource', 'time:timestamp',
            'case:last_phase', 'case:parts', 'action_code', 'r:municipality'
        ]]
        # Delete all rows were case_id = 4020737 --> Author response: "there is more than one value for attribute “ct:permit_type” "
        df = df[df['case:concept:name'] != 4020737]
        df = df.rename(columns={
            # Resource-related
            "activityNameEN": "activity label",
            # CT-related
            'case:last_phase': 'ct:last_phase', 
            # AT-related
            "action_code": "concept:name",
            # Additional
            'case:parts': 'case_parts',
        })
        # TODO: derive 'ct:permit_type', 'at:phase' --> specified by the author
        df = df[~df['case_parts'].isna()]
        df['ct:permit_type'] = df.apply(lambda row: 'Bouw' if 'Bouw' in str(row['case_parts']).split(',') else 'Non Bouw', axis=1)

        # only look at the main subprocess: "01_HOOFD"
        df = df[~df['concept:name'].isna()]
        df = df[df['concept:name'].str.startswith('01_HOOFD')]
        df['at:phase'] = df['concept:name'].apply(lambda code: code[:10])
        
        # filter meaningless values

    # Universal (on Disco outputs)
    # derive and append TT related candidate attributes
    df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df['tt:month'] = df['time:timestamp'].apply(lambda ts: MONTHS[ts.month-1])
    df['tt:day'] = df['time:timestamp'].apply(lambda ts: 'Day_{}'.format(ts.day))
    WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df['tt:weekday'] = df['time:timestamp'].apply(lambda ts: WEEKDAYS[ts.dayofweek])
    df['tt:ampm'] = df['time:timestamp'].apply(lambda ts: 'AM' if ts.hour < 12 else 'PM')
    
    print(df)
    df.to_csv(f'data/processed/{log}.csv')
else:
    df = pd.read_csv(fn, index_col=0)
    print(df)
