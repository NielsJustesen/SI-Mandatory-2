import logging

import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    amount = req.params.get('amount')
    if not amount:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            amount = req_body.get('amount')

    if amount:
        return func.HttpResponse(json.dumps(AddInterest(amount)), status_code=200)
    else:
        return func.HttpResponse(
             "This HTTP triggered function failed to get the amount or is missing an amount.",
             status_code=400
        )


def AddInterest(amount):
    interest = 0.02
    return {"amount": amount * 0.02 + amount }