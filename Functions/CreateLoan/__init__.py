import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    currentAmount = req.params.get('CurrentAmount')
    newAmount = req.params.get('NewAmount')


    if (ValidateLoan):
        return func.HttpResponse(
            f"The new loan has been validated, {newAmount} will be deposited to the account",
            status_code=200
        )
    else:
        return func.HttpResponse(
             "The loan exceeds the allowed value, make sure the amount isn't greater than 75'%' of the users current amount",
             status_code=403
        )


def ValidateLoan(currentAmount, newAmount):
    
    percentageCheck = 0.75
    valid = currentAmount * percentageCheck
    if (valid >= currentAmount):
        return True
    else:
        return False
    
