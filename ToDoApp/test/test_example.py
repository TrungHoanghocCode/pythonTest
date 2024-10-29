import pytest


# def test_equal_or_not():
#     assert 3 == 3
#     assert 7 > 3
#
#
# def test_is_instance():
#     assert isinstance("this is Str", str)
#     assert not isinstance("String - not int", int)
#
#
# def test_boolean():
#     a = True
#     assert a is True
#     assert ("so 10" == 10) is False
#
#
# def test_type():
#     assert type("so 10" is str)
#     assert type("so 10" is not int)
#
#
# def test_list():
#     b = [1, 2, 3,]
#     c = [0, False]
#     assert type(b is list)
#     assert 2 in b
#     assert 7 not in b
#     assert all(b)
#     # all(b) nghia la tat ca cac phan tu cua b la true thi pass
#     assert not any(c)
#     # not any(c) nghia la tat ca cac phan tu cua b la fasle thi pass


# class nay duoc tao de lam vi du
class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


# doi voi cach test nay, moi lan test lai phai tao 1 p tuong ung de test
# def test_person_inittialiazation():
#     # phai khoi tao p de test
#     p = Student("Dead", "Pool", "IT", 4)
#     # phan sau "Dead" chi nham muc dich hint
#     assert p.first_name == 'Dead', 'First name should be Dead or ...'
#     assert p.last_name == 'Pool', 'Last name should be Doe - not wrong'
#     assert p.major == 'IT', "hint"
#     assert p.years == 4, 987654321

# cach nay tan dung pytest, nhanh hon, khong can khoi tao p mau choi moi ham
# tao 1 default_employee 1 lan duy nhat
@pytest.fixture
def default_employee():
    return Student('Dead', 'Pool', 'Computer Science', 3)


# va sau do test
def test_person_initialization(default_employee):
    assert default_employee.first_name == 'Dead', 'First name should be Dead or ...'
    assert default_employee.last_name == 'Pool', 'Last name should be Doe - not wrong'
    assert default_employee.major == 'Computer Science', "hint"
    assert default_employee.years == 3, 987654321
