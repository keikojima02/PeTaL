from uuid import uuid1


def generate_job(job_func, job_param, countdown = 0, job_id = None):
    if job_id is None:
        job_id = str(uuid1())
    try:
        return job_func.apply_async(kwargs = job_param, countdown = countdown,
                                    job_id = job_id)
    except (IOError, Exception) as exception:

        failure_uuid = str(uuid1())
        failure_dict = {
            'action': 'failed_job',
            'attempted_job': job_func.__name__,
            'job_info_kwargs': job_param,
            'failure_uuid': failure_uuid
        }
        # add_failure_to_queue(failure_dict)
        raise exception
