from celery import task

from votingpayment.utils import check_pending_payments


@task
def task_check_pending_payments():
    return check_pending_payments()
