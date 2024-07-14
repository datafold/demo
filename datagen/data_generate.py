#!/usr/bin/env python3

import os
import pandas as pd
import random
import math
from datetime import datetime, timedelta, timezone


def datetime_str_to_datetime(date_string):
    # Parse the string to a naive datetime object
    naive_datetime = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    
    # Make the datetime object timezone-aware (UTC)
    aware_datetime = naive_datetime.replace(tzinfo=timezone.utc)
    
    return aware_datetime


def random_datetime(start: datetime, end: datetime) -> datetime:
    # Ensure that start and end are in UTC
    start = start.astimezone(timezone.utc)
    end = end.astimezone(timezone.utc)

    # Get the total seconds between start and end
    delta = (end - start).total_seconds()

    # Generate a random number of seconds to add to the start time
    random_seconds = random.uniform(0, delta)

    # Create the new datetime by adding the random seconds to start time
    random_date = start + timedelta(seconds=random_seconds)

    return random_date



def generate_single_org_created_user_created(start_datetime: datetime, end_datetime: datetime, new_org_batch, new_user_batch) -> (dict, dict):
    if not new_org_batch == []:
        org_id = max(new_org_batch, key=lambda x: x['org_id'])['org_id'] + 1
    elif os.path.exists('org_created.csv'):
        df = pd.read_csv('org_created.csv')
        org_id = df['org_id'].max() + 1
    else:
        org_id = 100000001


    employee_ranges = ['0-9', '10-24', '25-49', '500-1000', '1000+', '100-249', '250-499', '50-99']
    employee_range = random.choice(employee_ranges)

    
    created_at = random_datetime(start_datetime, end_datetime)
    created_at = created_at.strftime('%Y-%m-%dT%H:%M:%SZ')


    def extract_domain(email: str) -> str:
        try:
            # Split the email by '@' and return the domain part
            return email.split('@')[1]
        except IndexError:
            # Handle the case where the email does not contain '@'
            return None

    person_pool = pd.read_csv('persons_pool.csv')
    person_pool['domain'] = person_pool['email'].apply(extract_domain)

    if not new_org_batch == [] and os.path.exists('org_created.csv'):
        used_domains_in_current_batch = [d['domain'] for d in new_org_batch if 'domain' in d]
        person_pool_fresh = person_pool[~person_pool['domain'].isin(used_domains_in_current_batch)]

        org_created = pd.read_csv('org_created.csv')
        person_pool_fresh = person_pool_fresh[~person_pool_fresh['domain'].isin(org_created['domain'])]

    elif not new_org_batch == [] and not os.path.exists('org_created.csv'):
        used_domains_in_current_batch = [d['domain'] for d in new_org_batch if 'domain' in d]
        person_pool_fresh = person_pool[~person_pool['domain'].isin(used_domains_in_current_batch)]

    elif new_org_batch == [] and os.path.exists('org_created.csv'):
        org_created = pd.read_csv('org_created.csv')
        person_pool_fresh = person_pool[~person_pool['domain'].isin(org_created['domain'])]
    else:
        person_pool_fresh = person_pool

    # dies here and only here if not enough person_pool
    random_new_person = person_pool_fresh.sample(n=1)

    random_new_person_dict = random_new_person.to_dict(orient='records')[0]

    org_name = random_new_person_dict['company_name']
    domain = random_new_person_dict['domain']


    org_created_new_record = {
        'org_id': org_id,
        'org_name': org_name,
        'domain': domain,
        'employee_range': employee_range,
        'created_at': created_at
    }
    print('org_created_new_record', org_created_new_record)


    # USER CREATED

    if not new_user_batch == []:
        user_id = max(new_user_batch, key=lambda x: x['user_id'])['user_id'] + 1
    elif os.path.exists('user_created.csv'):
        df = pd.read_csv('user_created.csv')
        user_id = df['user_id'].max() + 1
    else:
        user_id = 100000001


    first_name = random_new_person_dict['first_name']
    last_name = random_new_person_dict['last_name']
    email = random_new_person_dict['email']
    is_first_user = 'TRUE'


    user_created_new_record = {
        'user_id': user_id,
        'org_id': org_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'is_first_user': is_first_user,
        'created_at': created_at
    }
    print('user_created_new_record', user_created_new_record)

    
    return org_created_new_record, user_created_new_record



# USER CREATED FOR EXISTING ORG

def generate_single_user_created(start_datetime: datetime, end_datetime: datetime, new_org_batch: list, new_user_batch: list) -> dict:

    if not new_user_batch == []:
        user_id = max(new_user_batch, key=lambda x: x['user_id'])['user_id'] + 1
    elif new_user_batch == [] and os.path.exists('user_created.csv'):
        user_created = pd.read_csv('user_created.csv')
        user_id = user_created['user_id'].max() + 1
    else:
        user_id = 100000001


    if os.path.exists('org_created.csv'):
        org_created = pd.read_csv('org_created.csv')
        random_existing_org = org_created.sample(n=1)
    elif len(new_org_batch) > 0:
        random_existing_org = random.choice(new_org_batch)
        random_existing_org = pd.json_normalize([random_existing_org])
    else:
        return None
    org_id = random_existing_org.iloc[0, random_existing_org.columns.get_loc('org_id')]
    org_created_at_str = random_existing_org.iloc[0, random_existing_org.columns.get_loc('created_at')]
    org_created_at = datetime_str_to_datetime(org_created_at_str)

    
    person_pool = pd.read_csv('persons_pool.csv')
    random_person1 = person_pool.sample(n=1)
    first_name = random_person1.iloc[0, random_person1.columns.get_loc('first_name')]
    random_person2 = person_pool.sample(n=1)
    last_name = random_person2.iloc[0, random_person1.columns.get_loc('last_name')]


    email = first_name.lower() + '.' + last_name.lower() + '@' + random_existing_org.iloc[0, random_existing_org.columns.get_loc('domain')]

    
    is_first_user = 'FALSE'

    
    created_at = random_datetime(max(start_datetime, org_created_at), end_datetime)
    created_at = created_at.strftime('%Y-%m-%dT%H:%M:%SZ')

    
    user_created_new_record = {
        'user_id': user_id,
        'org_id': org_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'is_first_user': is_first_user,
        'created_at': created_at
    }
    print('user_created_new_record', user_created_new_record)


    return user_created_new_record



# signed in

def generate_single_signed_in(start_datetime: datetime, end_datetime: datetime, new_org_batch: list) -> dict:

    if os.path.exists('org_created.csv'):
        org_created = pd.read_csv('org_created.csv')
        random_existing_org = org_created.sample(n=1)
    elif len(new_org_batch) > 0:
        random_existing_org = random.choice(new_org_batch)
        random_existing_org = pd.json_normalize([random_existing_org])
    else:
        return None
    org_id = random_existing_org.iloc[0, random_existing_org.columns.get_loc('org_id')]
    org_created_at_str = random_existing_org.iloc[0, random_existing_org.columns.get_loc('created_at')]
    org_created_at = datetime_str_to_datetime(org_created_at_str)


    event_timestamp = random_datetime(max(start_datetime, org_created_at), end_datetime)
    event_timestamp = event_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')


    activity = 'signed in'


    signed_in_new_record = {
        'org_id': org_id,
        'event_timestamp': event_timestamp,
        'activity': activity
    }
    print('signed_in_new_record', signed_in_new_record)

    
    return signed_in_new_record


# FEATURE USED

def generate_single_feature_used(start_datetime: datetime, end_datetime: datetime, new_org_batch: list) -> dict:

    if os.path.exists('org_created.csv'):
        org_created = pd.read_csv('org_created.csv')
        random_existing_org = org_created.sample(n=1)
    elif len(new_org_batch) > 0:
        random_existing_org = random.choice(new_org_batch)
        random_existing_org = pd.json_normalize([random_existing_org])
    else:
        return None
    org_id = random_existing_org.iloc[0, random_existing_org.columns.get_loc('org_id')]
    org_created_at_str = random_existing_org.iloc[0, random_existing_org.columns.get_loc('created_at')]
    org_created_at = datetime_str_to_datetime(org_created_at_str)


    event_timestamp = random_datetime(max(start_datetime, org_created_at), end_datetime)
    event_timestamp = event_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')


    activity = random.choice(['feature A', 'feature A', 'feature A', 'feature B', 'feature B', 'feature C'])


    feature_used_new_record = {
        'org_id': org_id,
        'event_timestamp': event_timestamp,
        'activity': activity
    }
    print('feature_used_new_record', feature_used_new_record)

    
    return feature_used_new_record



# SUBSCRIPTION CREATED

def generate_single_subscription_created(start_datetime: datetime, end_datetime: datetime, new_org_batch: list, new_subsctiption_created_batch: list) -> dict:


    if os.path.exists('org_created.csv'):
        org_created = pd.read_csv('org_created.csv')
    elif len(new_org_batch) > 0:
        org_created = pd.json_normalize(new_org_batch)
    else:
        return None

    if new_subsctiption_created_batch == [] and os.path.exists('subscription_created.csv'):
        subscription_created = pd.read_csv('subscription_created.csv')
    elif not new_subsctiption_created_batch == [] and not os.path.exists('subscription_created.csv'):
        subscription_created = pd.json_normalize(new_subsctiption_created_batch)
    elif not new_subsctiption_created_batch == [] and os.path.exists('subscription_created.csv'):
        subscription_created1 = pd.read_csv('subscription_created.csv')
        subscription_created2 = pd.json_normalize(new_subsctiption_created_batch)
        subscription_created = pd.concat([subscription_created1, subscription_created2], axis=0, ignore_index=True)
    else:
        data = {'org_id': [], 'org_name': [], 'domain': [], 'employee_range': [], 'created_at': []}
        subscription_created = pd.DataFrame.from_dict(data)

    who_can_subscribe = org_created[~org_created['org_id'].isin(subscription_created['org_id'])]

    if len(who_can_subscribe) == 0:
        return None
    
    random_existing_org_who_can_subsribe = who_can_subscribe.sample(n=1)
    
    org_id = random_existing_org_who_can_subsribe.iloc[0, random_existing_org_who_can_subsribe.columns.get_loc('org_id')]
    org_created_at_str = random_existing_org_who_can_subsribe.iloc[0, random_existing_org_who_can_subsribe.columns.get_loc('created_at')]
    org_created_at = datetime_str_to_datetime(org_created_at_str)


    event_timestamp = random_datetime(max(start_datetime, org_created_at), end_datetime)
    event_timestamp = event_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

    
    activity = 'subscribed'

    
    plans = ['Team', 'Business']
    plan = random.choice(plans)
    if plan == 'Team':
        price = 99
    elif plan == 'Business':
        price = 399
    else:
        price = 0

        
    deployments = ['SaaS', 'On-prem']
    deployment = random.choice(deployments)

    
    subscription_created_new_record = {
        'org_id': org_id,
        'event_timestamp': event_timestamp,
        'activity': activity,
        'plan': plan,
        'price': price,
        'deployment': deployment
    }
    print('subscription_created_new_record', subscription_created_new_record)

    
    return subscription_created_new_record



def generate_multiple_org_created_user_created(n: int, start_datetime: datetime, end_datetime: datetime) -> (list[dict], list[dict]):
    new_org_batch = []
    new_user_batch = []
    for i in range(0, n):
        new_org, new_user = generate_single_org_created_user_created(start_datetime, end_datetime, new_org_batch, new_user_batch)
        new_org_batch.append(new_org)
        new_user_batch.append(new_user)

    return new_org_batch, new_user_batch
        

def generate_multiple_user_created(n: int, start_datetime: datetime, end_datetime: datetime, new_org_batch, new_user_batch) -> list[dict]:
    for i in range(0, n):
        new_user = generate_single_user_created(start_datetime, end_datetime, new_org_batch, new_user_batch)
        if not new_user == None:
            new_user_batch.append(new_user)
        else:
            return new_user_batch
    return new_user_batch


def generate_multiple_signed_in(n: int, start_datetime: datetime, end_datetime: datetime, new_org_batch) -> list[dict]:
    new_signed_in_batch = []
    for i in range(0, n):
        new_signed_in = generate_single_signed_in(start_datetime, end_datetime, new_org_batch)
        if not new_signed_in == None:
            new_signed_in_batch.append(new_signed_in)
        else:
            return new_signed_in_batch
    return new_signed_in_batch


def generate_multiple_feature_used(n: int, start_datetime: datetime, end_datetime: datetime, new_org_batch) -> list[dict]:
    new_feature_used_batch = []
    for i in range(0, n):
        new_feature_used = generate_single_feature_used(start_datetime, end_datetime, new_org_batch)
        if not new_feature_used == None:
            new_feature_used_batch.append(new_feature_used)
        else:
            return new_feature_used_batch
    return new_feature_used_batch


def generate_multiple_subscription_created(n: int, start_datetime: datetime, end_datetime: datetime, new_org_batch) -> list[dict]:
    new_subsctiption_created_batch = []
    for i in range(0, n):
        new_subsctiption_created = generate_single_subscription_created(start_datetime, end_datetime, new_org_batch, new_subsctiption_created_batch)
        if not new_subsctiption_created == None:
            new_subsctiption_created_batch.append(new_subsctiption_created)
        else:
            return new_subsctiption_created_batch
    return new_subsctiption_created_batch


# ##############################################################################
# BREAKERS
# ##############################################################################

def get_random_element_and_rest(input_list):
    if not input_list:
        return None, []

    # Get a random index
    random_index = random.randint(0, len(input_list) - 1)

    # Get the random element
    random_element = input_list[random_index]

    # Get the rest of the elements
    rest_elements = input_list[:random_index] + input_list[random_index + 1:]

    return random_element, rest_elements


def break__subscription_created__negative_price(subscription_created_record):
    result = subscription_created_record.copy()
    result['price'] = round(random.uniform(-1000, 0) * random.choices([0, 1], weights=[0.3, 0.7], k=1)[0])
    return result

def break_batch__subscription_created__negative_price(new_subscription_created_batch):
    if new_subscription_created_batch:
        element_to_break, rest = get_random_element_and_rest(new_subscription_created_batch)
        broken_element = break__subscription_created__negative_price(element_to_break)
        return [broken_element] + rest
    return new_subscription_created_batch


def break__user_created__damaged_email(user_created_record):
    result = user_created_record.copy()
    result['email'] = user_created_record['email'].replace('@', '$')
    return result

def break_batch__user_created__damaged_email(new_user_batch):
    if new_user_batch:
        element_to_break, rest = get_random_element_and_rest(new_user_batch)
        broken_element = break__user_created__damaged_email(element_to_break)
        return [broken_element] + rest
    return new_user_batch


def break__feature_used__activity_null(feature_used_record):
    result = feature_used_record.copy()
    result['activity'] = ''
    return result

def break_batch__feature_used__activity_null(feature_used_batch):
    if feature_used_batch:
        element_to_break, rest = get_random_element_and_rest(feature_used_batch)
        broken_element = break__feature_used__activity_null(element_to_break)
        return [broken_element] + rest
    return feature_used_batch

def break_batch_30__feature_used__activity_null(feature_used_batch):
    for _ in range(0, math.ceil(len(feature_used_batch) / 3.3 * random.uniform(0.7, 1.3))):
        feature_used_batch = break_batch__feature_used__activity_null(feature_used_batch)
    return feature_used_batch


def break_data(new_org_batch, new_user_batch, new_signed_in_batch, new_subscription_created_batch, new_feature_used_batch):
    possible_breakage_codes = [1, 2, 3]
    number_of_breakages_needed = random.randint(0, 1)
    breakage_codes_for_today = []
    for i in range(0, number_of_breakages_needed):
        breakage_codes_for_today.append(random.choice(possible_breakage_codes))

    for breakage_code in breakage_codes_for_today:
        if breakage_code == 1:
            new_subscription_created_batch = break_batch__subscription_created__negative_price(new_subscription_created_batch)
        elif breakage_code == 2:
            new_user_batch = break_batch__user_created__damaged_email(new_user_batch)
        elif breakage_code == 3:
            new_feature_used_batch = break_batch_30__feature_used__activity_null(new_feature_used_batch)

    return new_org_batch, new_user_batch, new_signed_in_batch, new_subscription_created_batch, new_feature_used_batch

# ##############################################################################
# END OF BREAKERS
# ##############################################################################


def generate_events_day(start_datetime: datetime, end_datetime: datetime):

    hours = round((end_datetime - start_datetime).total_seconds() / 3600)

    number_of_signed_in_events_anomaly_factor = random.choices([1, 0], weights=[1, 10], k=1)[0]
    
    hourly_probs = {
        'new_org': 4/24 * random.uniform(0.7, 1.3),
        'new_user': 2/24 * random.uniform(0.7, 1.3),

        # no anomalies, week day seasonality
        # 'signed_in': 2/24 * random.uniform(0.9, 1.1) * (abs((start_datetime.weekday()) - 4) + 1),
        # shift by 4 days
        # 'signed_in': 2/24 * random.uniform(0.9, 1.1) * (abs(((start_datetime + timedelta(days=4) * number_of_signed_in_events_anomaly_factor).weekday()) - 4) + 1),
        # x3
        'signed_in': 2/24 * random.uniform(0.9, 1.1) * (abs((start_datetime.weekday()) - 4) + 1) * (2 * number_of_signed_in_events_anomaly_factor + 1),

        'subscription_created': 2/24 * random.uniform(0.7, 1.3),
        'feature_used': 10/24 * random.uniform(0.7, 1.3)
    }

    number_of_new_events = {
        'new_org': round(hours * hourly_probs['new_org']),
        'new_user': round(hours * hourly_probs['new_user']),
        'signed_in': round(hours * hourly_probs['signed_in']),
        'subscription_created': round(hours * hourly_probs['subscription_created']),
        'feature_used': round(hours * hourly_probs['feature_used']),
    }

    if number_of_signed_in_events_anomaly_factor == 1:
        print('>>>signed_in    anomaly in number of events:', number_of_new_events['signed_in'])
    else:
        print('>>>signed_in no anomaly in number of events:', number_of_new_events['signed_in'])

    new_org_batch, new_user_batch = generate_multiple_org_created_user_created(number_of_new_events['new_org'], start_datetime, end_datetime)
    new_user_batch = generate_multiple_user_created(number_of_new_events['new_user'], start_datetime, end_datetime, new_org_batch, new_user_batch)
    new_signed_in_batch = generate_multiple_signed_in(number_of_new_events['signed_in'], start_datetime, end_datetime, new_org_batch)
    new_subsctiption_created_batch = generate_multiple_subscription_created(number_of_new_events['subscription_created'], start_datetime, end_datetime, new_org_batch)
    new_feature_used_batch = generate_multiple_feature_used(number_of_new_events['feature_used'], start_datetime, end_datetime, new_org_batch)


    new_org_batch_broken, new_user_batch_broken, new_signed_in_batch_broken, new_subscription_created_batch_broken, new_feature_used_batch_broken = break_data(new_org_batch, new_user_batch, new_signed_in_batch, new_subsctiption_created_batch, new_feature_used_batch)

    
    # import shutil
    # shutil.copy('org_created.csv', f"org_created_backup_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.csv")
    # shutil.copy('user_created.csv', f"user_created_backup_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.csv")
    # shutil.copy('signed_in.csv', f"signed_in_backup_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.csv")
    # shutil.copy('subscription_created.csv', f"subscription_created_backup_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.csv")
    # shutil.copy('feature_used.csv', f"feature_used_backup_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.csv")

    if len(new_org_batch) > 0:
        if os.path.exists('org_created.csv'):
            pd.json_normalize(new_org_batch).to_csv('org_created.csv', mode='a', header=False, index=False)
        else:
            pd.json_normalize(new_org_batch).to_csv('org_created.csv', index=False)

    if len(new_user_batch) > 0:
        if os.path.exists('user_created.csv'):
            pd.json_normalize(new_user_batch).to_csv('user_created.csv', mode='a', header=False, index=False)
        else:
            pd.json_normalize(new_user_batch).to_csv('user_created.csv', index=False)

    if len(new_signed_in_batch) > 0:
        if os.path.exists('signed_in.csv'):
            pd.json_normalize(new_signed_in_batch).to_csv('signed_in.csv', mode='a', header=False, index=False)
        else:
            pd.json_normalize(new_signed_in_batch).to_csv('signed_in.csv', index=False)

    if len(new_subsctiption_created_batch) > 0:
        if os.path.exists('subscription_created.csv'):
            pd.json_normalize(new_subsctiption_created_batch).to_csv('subscription_created.csv', mode='a', header=False, index=False)
        else:
            pd.json_normalize(new_subsctiption_created_batch).to_csv('subscription_created.csv', index=False)

    if len(new_feature_used_batch) > 0:
        if os.path.exists('feature_used.csv'):
            pd.json_normalize(new_feature_used_batch).to_csv('feature_used.csv', mode='a', header=False, index=False)
        else:
            pd.json_normalize(new_feature_used_batch).to_csv('feature_used.csv', index=False)


    if len(new_org_batch_broken) > 0:
        if os.path.exists('org_created_broken.csv'):
            pd.json_normalize(new_org_batch_broken).to_csv('org_created_broken.csv', mode='a', header=False, index=False)
        else:
            pd.json_normalize(new_org_batch_broken).to_csv('org_created_broken.csv', index=False)

    if len(new_user_batch_broken) > 0:
        if os.path.exists('user_created_broken.csv'):
            pd.json_normalize(new_user_batch_broken).to_csv('user_created_broken.csv', mode='a', header=False, index=False)
        else:
            pd.json_normalize(new_user_batch_broken).to_csv('user_created_broken.csv', index=False)

    if len(new_signed_in_batch_broken) > 0:
        if os.path.exists('signed_in_broken.csv'):
            pd.json_normalize(new_signed_in_batch_broken).to_csv('signed_in_broken.csv', mode='a', header=False, index=False)
        else:
            pd.json_normalize(new_signed_in_batch_broken).to_csv('signed_in_broken.csv', index=False)

    if len(new_subscription_created_batch_broken) > 0:
        if os.path.exists('subscription_created_broken.csv'):
            pd.json_normalize(new_subscription_created_batch_broken).to_csv('subscription_created_broken.csv', mode='a', header=False, index=False)
        else:
            pd.json_normalize(new_subscription_created_batch_broken).to_csv('subscription_created_broken.csv', index=False)

    if len(new_feature_used_batch_broken) > 0:
        if os.path.exists('feature_used_broken.csv'):
            pd.json_normalize(new_feature_used_batch_broken).to_csv('feature_used_broken.csv', mode='a', header=False, index=False)
        else:
            pd.json_normalize(new_feature_used_batch_broken).to_csv('feature_used_broken.csv', index=False)

        
def generate_events_days(period_start_datetime: datetime, period_end_datetime: datetime):


    one_day = timedelta(days=1)

    start_datetime = period_start_datetime
    start_datetime__next_midnight = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0) + one_day

    # end_datetime = min(start_datetime + one_day, period_end_datetime)
    end_datetime = min(start_datetime__next_midnight, period_end_datetime)

    while start_datetime < period_end_datetime:

        # 24-h processing
        print(start_datetime, end_datetime)
        generate_events_day(start_datetime, end_datetime)
        # end of 24-h processing

        start_datetime += one_day
        end_datetime = min(start_datetime + one_day, period_end_datetime)


if __name__ == "__main__":

    if os.path.exists('org_created.csv') or os.path.exists('user_created.csv') or os.path.exists('signed_in.csv') or os.path.exists('subscription_created.csv') or os.path.exists('feature_used.csv'):
        latest_event_org_created = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        if os.path.exists('org_created.csv'):
            df = pd.read_csv('org_created.csv')
            latest_event_org_created = max(latest_event_org_created, df['created_at'].apply(datetime_str_to_datetime).max())

        if os.path.exists('user_created.csv'):
            df = pd.read_csv('user_created.csv')
            latest_event_org_created = max(latest_event_org_created, df['created_at'].apply(datetime_str_to_datetime).max())

        if os.path.exists('signed_in.csv'):
            df = pd.read_csv('signed_in.csv')
            latest_event_org_created = max(latest_event_org_created, df['event_timestamp'].apply(datetime_str_to_datetime).max())

        if os.path.exists('subscription_created.csv'):
            df = pd.read_csv('subscription_created.csv')
            latest_event_org_created = max(latest_event_org_created, df['event_timestamp'].apply(datetime_str_to_datetime).max())

        if os.path.exists('feature_used.csv'):
            df = pd.read_csv('feature_used.csv')
            latest_event_org_created = max(latest_event_org_created, df['event_timestamp'].apply(datetime_str_to_datetime).max())

        period_start_datetime = latest_event_org_created
    else:
        period_start_datetime = (datetime.now() + timedelta(days=-100)).replace(tzinfo=timezone.utc)

    period_end_datetime = datetime.now(timezone.utc)

    # period_start_datetime = datetime(2024, 7, 8, 1, 0, 0, tzinfo=timezone.utc)
    # period_end_datetime = datetime(2024, 7, 11, 2, 0, 0, tzinfo=timezone.utc)

    generate_events_days(period_start_datetime, period_end_datetime)
