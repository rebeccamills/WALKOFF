from datetime import datetime

import core.case.subscription as case_subscription
import core.case.database as case_database


def setup_subscriptions_for_step(workflow_names, step_names):
    step_sub = case_subscription.Subscription(events=['FunctionExecutionSuccess'])
    if type(step_names) == list:
        step_subs = case_subscription.Subscription(subscriptions={name: step_sub for name in step_names})
    else:
        step_subs = case_subscription.Subscription(subscriptions={step_names: step_sub})
    if type(workflow_names) == list:
        workflow_subs = case_subscription.Subscription(subscriptions={workflow_name: step_subs
                                                                      for workflow_name in workflow_names})
    else:
        workflow_subs = case_subscription.Subscription(subscriptions={workflow_names: step_subs})

    subs = {'defaultController': workflow_subs}
    case_subscription.set_subscriptions({'case1': case_subscription.CaseSubscriptions(subscriptions=subs)})


def executed_steps(controller_name, workflow_name, start_time, end_time):
    events = case_database.case_db.session.query(case_database.Event). \
        filter(case_database.Event.ancestry.startswith('{0},{1}'.format(controller_name, workflow_name))).all()
    events = [event.as_json() for event in events]
    out = []
    for event in events:
        if start_time <= datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S.%f') <= end_time:
            out.append(event)
    return out
