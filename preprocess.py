import pandas as pd
# Load raw data & Preprocess DataFrame (enrich with derived attributes)
log = 'bpic15'

preprocess = True

#abragen, ob schon fertig preprocessed
if preprocess:
    fn = f'data/raw/{log}.csv'
else:
    fn = f'data/processed/{log}.csv'

#für versch. Logs unterschiedliches Preprocessing
if preprocess:
         
    if log == 'bpic15':
        #liest nicht alle Spalten ein, nur die die gebraucht
        df = pd.read_csv(fn)[[
            'case:concept:name', 'activityNameEN', 'org:resource', 'time:timestamp',
            'case:last_phase', 'case:parts', 'action_code', 'r:municipality'
        ]]
        
        #umbenennen der Spalten
        df = df.rename(columns={
            # Resource-related
            'municipality': 'r:municipality',
            'case:concept:name' : 'Case ID',
            'time:timestamp': 'Complete timestamp',
            "org:resource": "resource",
            "activityNameEN": "activity label",
            # CT-related
            'case:last_phase': 'ct:last_phase', 
            # AT-related
        })
        df = df.rename(columns={
            'case:parts': 'case_parts'
        })
        # TODO: derive 'ct:permit_type', 'at:phase'
        df = df[~df['case_parts'].isna()]
        #bennent um nach Bau und Nicht-Bau
        df['ct:permit_type'] = df.apply(lambda row: 'Bouw' if 'Bouw' in str(row['case_parts']).split(',') else 'Non Bouw', axis=1)

        # only look at the main subprocess: "01_HOOFD"
        df = df[~df['action_code'].isna()]
        df = df[df['action_code'].str.startswith('01_HOOFD')]
        df['at:phase'] = df['action_code'].apply(lambda code: code[:10])
        
        # filter meaningless values

    # Universal (on Disco outputs)
    # derive and append TT related candidate attributes
    df['Complete Timestamp'] = pd.to_datetime(df['Complete Timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df['tt:month'] = df['Complete Timestamp'].apply(lambda ts: MONTHS[ts.month-1])
    df['tt:day'] = df['Complete Timestamp'].apply(lambda ts: 'Day_{}'.format(ts.day))
    WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df['tt:weekday'] = df['Complete Timestamp'].apply(lambda ts: WEEKDAYS[ts.dayofweek])
    df['tt:ampm'] = df['Complete Timestamp'].apply(lambda ts: 'AM' if ts.hour < 12 else 'PM')
    
    print(df)
    df.to_csv(f'data/processed/{log}.csv')
else:
    df = pd.read_csv(fn, index_col=0)
    print(df)
