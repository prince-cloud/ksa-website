from .models import Election


def get_department_name(election: Election):
    return election.name.split(" ")[0].split("-")[-1]