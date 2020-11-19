module.exports = async function (context, req) {
    context.log('JavaScript HTTP trigger function processed a request.');

    const deposit = (req.query.Deposit || (req.body && req.body.deposit));
    
    var responseMessage = "";
    if (deposit !== undefined && parseInt(deposit) > 0){
        addInterest = InterestAmount(parseInt(deposit));
        responseMessage = {"Message":"Added interest to deposit", "Deposit":addInterest};
        context.res = {
            status: 200, 
            body: responseMessage
        };
    }
    else {
        responseMessage = {"Message":"Bad Request"};
        context.res = {
            status: 400, 
            body: responseMessage
        };
    }
    


}

function InterestAmount(amount){
    return amount * 1.02;
}