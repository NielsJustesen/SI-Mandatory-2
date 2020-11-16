import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    currentAmount = req.params.get('CurrentAmount')
    loanAmount = req.params.get('LoanAmount')


    if (ValidateLoan(currentAmount, loanAmount)):
        return func.HttpResponse(
            f"The new loan has been validated, {loanAmount} will be deposited to the account",
            status_code=200
        )
    else:
        return func.HttpResponse(
             "The loan exceeds the allowed value, make sure the amount isn't greater than 75'%' of the users current amount",
             status_code=403
        )


def ValidateLoan(currentAmount, loanAmount):
    
    percentageCheck = 0.75
    validLoanAmount = currentAmount * percentageCheck
    if (validLoanAmount <= loanAmount):
        return True
    else:
        return False
    
