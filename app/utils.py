def format_date(date):
    return date.strftime("%d-%m-%y")


def apply_interest(amount, interest_rate=0.25):
    return (amount * interest_rate) + amount
