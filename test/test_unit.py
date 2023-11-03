from app.utils import calculate_final_tax


def test_calculate_tax():
    assert (
        calculate_final_tax(amount=1000000, gender="male", age=40, location="major")
        == 72500
    )
    assert (
        calculate_final_tax(amount=400000, gender="male", age=25, location="non_city")
        == 3000
    )

    assert (
        calculate_final_tax(amount=400000, gender="female", age=25, location="non_city")
        == 3000
    )
