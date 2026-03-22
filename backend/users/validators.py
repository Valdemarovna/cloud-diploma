import re
from django.core.exceptions import ValidationError

def validate_password(value):
    if len(value) < 6:
        raise ValidationError("Пароль должен быть не менее 6 символов")

    if not re.search(r'[A-Z]', value):
        raise ValidationError("Пароль должен содержать заглавную букву")

    if not re.search(r'\d', value):
        raise ValidationError("Пароль должен содержать цифру")

    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
        raise ValidationError("Пароль должен содержать спецсимвол")