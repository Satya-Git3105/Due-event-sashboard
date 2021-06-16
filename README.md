# Due-events-Dashboard

![Screenshot](images/DUE-engageEvents-dashboard.png)


Create Quicksight dashboard from Pinpoint/SES events
Please Refer - https://github.com/Satya-Git3105/Due-events-dashboard/blob/main/Pinpoint-Event-dashboard.docx 

Solution
This Solution extends DUE events database solution allowing all the events queried through Amazon Athena which will be integrated to Amazon Quicksight to display engagement events. This solution can be implemented into three steps in chronological order.
1.	Set up event database solution 
2.	Deploy the Athena View CloudFormation template
3.	Follow the blog to setup Amazon Quicksight to dashboard engagement event analytics and event dashboard

Use case(s)
User segmentation based on:
•	Deep dive into event insights. (eg : SMS events, Email events, Campaign events, Journey events)
•	Engagement event dashboard at individual user level.
•	Data/process mining 
•	User engagement benchmarking

Step 1 – Create AWS account & Pinpoint Project
Create an AWS account
Implement Event database solution 
Copy and save the 1/DUE database name 2/S3 Bucket name from DUE event database solution, this will be needed as input parameters in 

Step 2 – Create S3 bucket for Lambda code and upload the Zip file 
1.	This step explains on how to deploy the code ZIP file 
2.	Create an S3 bucket in the region that you have your Pinpoint projects and provide it a unique name
2.1.	Upload the zip file into the root folder: lambda_view_creator.zip. Install the cloud formation stack template within the same region as that of your DUE database is. Provide following details as input parameter to cloud formation stack and proceed with the installation. Zip Code package

Step 3 – Deploy Cloudformation template 

1.	This step creates several new amazon Athena views that’s to be act as a data source for Amazon Quicksight. Dashboard 
2.	Navigate to Cloud formation page in AWS console, click up right on “Create stack” and select the option “With new resources (standard)”
3.	Leave the “Prerequisite – Prepare template” to “Template is ready” and for the “Specify template” option, select “Upload a template file”. On the same page, click on “Choose file”, browse to find the file “DUE_analytics_dashboard.template” file and select it. Once the file is uploaded, click “Next” and deploy the stack
4.	See below information for each of the 6 fields under the section “Specify stack details”:
    a.	EventAthenaDatabaseName - As mentioned in Step1
    b.	LambdaCodes3bucket – S3 bucket name where you have installed the code zip file.
    c.	S3DataLogBucket- As mentioned in Step1
5.	This solution will create additional 5 Athena views which are 
    a.	All_email_events
    b.	All_SMS_events
    c.	All_custom_events (Custom events can be Mobile app/WebApp/Push Events)
    d.	All_campaign_events
    e.	All_journey_events

Step 4 – Create Amazon Quicksight engagement Dashboard
Please Refer - https://github.com/Satya-Git3105/Due-events-dashboard/blob/main/Pinpoint-Event-dashboard.docx 