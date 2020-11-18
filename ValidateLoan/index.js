module.exports = async function (context, req) {
    context.log('JavaScript HTTP trigger function processed a request.');

    const currentAmount = (req.query.currentAmount || (req.body && req.body.currentAmount));
    const loanAmount = (req.query.loanAmount || (req.body && req.body.loanAmount));
    var valid = Validate(currentAmount, loanAmount);
    
    var responseMessage = "";
    if (valid){
        responseMessage = {"Valid":"True", "Message":"Loan is valid"}
        context.res = {
            status: 200, 
            body: responseMessage
        };
    }
    else {
        responseMessage = {"Valid":"False", "Message":"Loan is invalid, not enough funds in account"}
        context.res = {
            status: 403, 
            body: responseMessage
        };
    }


}

function Validate(camount, lmaount){
    var validate = camount * 0.75;

    if(lmaount <= validate){
        return true;
    }
    else {
        return false;
    }
}