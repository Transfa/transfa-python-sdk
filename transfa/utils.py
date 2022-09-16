# utils and helpers


def get_default_log_message(response):
    return f"Response has failed with status {response.status_code} => {response.text}"