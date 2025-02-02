import azure.functions as func
import logging
import re


app = func.FunctionApp()

def calculate_digit(cpf_part, multipliers):
        total = sum(int(digit) * multiplier for digit, multiplier in zip(cpf_part, multipliers))
        remainder = (total * 10) % 11
        return 0 if remainder == 10 else remainder

def is_cpf_valid(cpf: str) -> bool:
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    first_digit = calculate_digit(cpf[:9], range(10, 1, -1))
    second_digit = calculate_digit(cpf[:10], range(11, 1, -1))
    return int(cpf[9]) == first_digit and int(cpf[10]) == second_digit

@app.route(auth_level=func.AuthLevel.ANONYMOUS)
def validate_cpf(req: func.HttpRequest) -> func.HttpResponse:
    cpf = req.params.get('cpf', '')
    if not cpf:
        return func.HttpResponse(
            "Required query param \"cpf\".",
            status_code=400
        )
    return func.HttpResponse(
        f"CPF {cpf} OK!" if is_cpf_valid(cpf) else f"Invalid CPF {cpf}!",
        status_code=200
    )
