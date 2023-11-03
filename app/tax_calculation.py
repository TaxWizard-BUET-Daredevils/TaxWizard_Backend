def calculate_basic_tax(taxable: int, above_income: int) -> int:
    total_tax = 0

    # for the next 100000, the person will pay 5% tax
    if taxable > 0:
        next_slab = min(taxable, 100000)
        total_tax += next_slab * 0.05
        taxable -= next_slab

    # for the next 300000, the person will pay 10% tax
    if taxable > 0:
        next_slab = min(taxable, 300000)
        total_tax += next_slab * 0.1
        taxable -= next_slab

    # for the next 400000, the person will pay 15% tax
    if taxable > 0:
        next_slab = min(taxable, 400000)
        total_tax += next_slab * 0.15
        taxable -= next_slab

    # for the next 500000, the person will pay 20% tax
    if taxable > 0:
        next_slab = min(taxable, 500000)
        total_tax += next_slab * 0.2
        taxable -= next_slab

    # for income above 1700000 or 1650000 the person will pay 25% tax
    if above_income > 0:
        total_tax += above_income * 0.25

    return int(total_tax)


def get_taxable_income(amount: int, gender: str, age: int) -> int:
    if gender == "female" or age > 65:
        untaxable = 400000
    else:
        untaxable = 350000

    taxable = amount - untaxable
    return max(taxable, 0)


def get_above_income(amount: int, gender: str, age: int) -> int:
    if gender == "female" or age > 65:
        above_income = amount - 1700000
    else:
        above_income = amount - 1650000
    return above_income


def calculate_final_tax(amount: int, gender: str, age: int, location: str) -> int:
    if location == "dhaka" or location == "chittagong":
        min_amount = 5000

    if location == "city":
        min_amount = 4000
    else:
        min_amount = 3000

    taxable = get_taxable_income(amount, gender, age)
    above_income = get_above_income(amount, gender, age)

    if taxable <= 0:
        return 0

    else:
        return max(calculate_basic_tax(taxable, above_income), min_amount)
