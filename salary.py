def predict_salary(salary_from, salary_to):
    if salary_from > 0:
        if salary_to > 0:
            return (int(salary_from) + int(salary_to)) / 2
        else:
            return int(salary_from) * 1.2
    elif salary_to > 0:
        return int(salary_to) * 0.8
        