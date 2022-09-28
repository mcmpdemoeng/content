(function process( /*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    var apiKey = request.queryParams['apiKey'];
	
	var event = request.body.data;

	var HTTPrequest = new sn_ws.RESTMessageV2();
	HTTPrequest.setEndpoint('<baseUrl>/api/now/v1/table/incident');
	HTTPrequest.setHttpMethod('POST');

	//Eg. UserName="admin", Password="admin" for this code sample.

	var user = '<user>';

	var password = '<password>';
	//var number = event.data.context.activityLog.properties.trackingId;
	HTTPrequest.setBasicAuth(user,password);
	var body = {
		"short_description" : event.data.essentials.description,
		"description" : event.data.essentials,
		"urgency": "1",
		"priority": "1",
		"severity": "1",
		"impact": "1",
		"assignment_group":"Incident Management",
		"correlation_id": event.data.essentials.alertId
	};
	var stringBody = "{0}".format(body);
	HTTPrequest.setRequestBody(JSON.stringify(body));
	HTTPrequest.setRequestHeader('content-type','application/json');
	var incresp = HTTPrequest.execute();

	var responsedata = incresp.getBody();
	var status = incresp.getStatusCode();


	response.setBody(
	{
		"status": status,
		"body": responsedata,
		
	}
	);


})(request, response);
