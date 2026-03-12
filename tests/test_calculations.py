import pytest
from app.calculations import add, multiply, substract, divide

@ pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (1, 1, 2),
    (0, 0, 0)
])
def test_add(a, b, expected):
    print('Testing add function')
    assert add(a, b) == expected

@ pytest.mark.parametrize("a, b, expected", [
    (5, 3, 2),
    (10, 4, 6),
    (0, 0, 0)
])
def test_substract(a, b, expected):
    print('Testing substract function')
    assert substract(a, b) == expected

def test_multiply():
    print('Testing multiply function')
    assert multiply(2, 3) == 6
    
def test_divide():
    print('Testing divide function')
    assert divide(6, 3) == 2
