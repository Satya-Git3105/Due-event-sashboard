import cfnresponse
import os
import logging
import traceback
import boto3
import json
import time

athena = boto3.client('athena')
sesv2 = boto3.client('sesv2')


def execute_named_queries(namedQueries):
   
    try:
        response = athena.batch_get_named_query(
            NamedQueryIds=namedQueries
        )
        
        for q in response['NamedQueries']:
            start_query_response = athena.start_query_execution(
                QueryString=q['QueryString'],
                QueryExecutionContext={
                  'Database': q['Database']
                },
                ResultConfiguration={
                  'OutputLocation': 's3://%s/temp/' % (os.environ.get('S3_DATA_BUCKET'))
                }
            )
            while True:
                time.sleep(4)

                get_query_response = athena.get_query_execution(
                    QueryExecutionId=start_query_response['QueryExecutionId']
                )

                if get_query_response['QueryExecution']['Status']['State'] == 'SUCCEEDED' or get_query_response['QueryExecution']['Status']['State'] == 'FAILED':
                    logging.info('Query Result for Satya check1: %s' % (q['Name']), get_query_response)
                    break
    except Exception as error:
        logging.error('execute_named_queries error: %s' % (error))
        logging.error('execute_named_queries trace: %s' % traceback.format_exc())
        raise

def set_pinpoint_event_destination(snames):
    try:
        for sn in snames:
            if sn == '':
                break
            response = sesv2.create_configuration_set_event_destination(
                ConfigurationSetName=sn,
                EventDestinationName='event-database',
                EventDestination={
                  'Enabled': True,
                  'MatchingEventTypes': [
                      'SEND','REJECT','BOUNCE','COMPLAINT','DELIVERY','OPEN','CLICK','RENDERING_FAILURE',
                  ],
                  'PinpointDestination': {
                      'ApplicationArn': os.environ.get('PINPOINT_PROJECT_ARN')
                  }
                }
            )
            logging.info('SN Response for: %s' % (sn), response)
    except Exception as error:
        logging.error('set_pinpoint_event_destination error: %s' % (error))
        logging.error('set_pinpoint_event_destination trace: %s' % traceback.format_exc())
        raise

def lambda_handler(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully- Satya - 2!",
        "input": event
    }
    '''
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    # return response
    '''
    log_level = str(os.environ.get('LOG_LEVEL')).upper()
    if log_level not in [
                      'DEBUG', 'INFO',
                      'WARNING', 'ERROR',
                      'CRITICAL'
                  ]:
      log_level = 'DEBUG'

    time.sleep(5)
    logging.getLogger().setLevel(log_level)
    bucketname = os.environ.get('S3_DATA_BUCKET')
    logging.info('Event value ------ : %s' % event)
    logging.info('S3_DATA_BUCKET ENV variable :----  %s' % bucketname)
    try:
        if event['ResourceProperties']['CustomResourceAction'] == 'SetupSampleFiles':
            #execute_named_queries([os.environ.get('ALL_EVENT_TABLE')])
            execute_named_queries([
                os.environ.get('EMAIL_ALL_EVENTS'),
                os.environ.get('JOURNEY_ALL_EVENTS'),
                os.environ.get('SMS_ALL_EVENTS'),
                os.environ.get('CAMPAIGN_ALL_EVENTS'),
                os.environ.get('CUSTOM_ALL_EVENTS'),
               # os.environ.get('OPEN_NQ')  
            ])
            '''     
            #####commented out as we dont need this method to 
            #####get called which is to update the configuration sets 
            set_pinpoint_event_destination(os.environ.get('EXISTING_CS').split(','))
            '''
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {"success": True}, 'SetupSampleFiles')
        else:
            logging.error('Missing CustomResourceAction - no action to perform')
            cfnresponse.send(event, context, cfnresponse.FAILED, {"success": False, "error": "Missing CustomResourceAction"}, "error")

    except Exception as error:
        logging.error('lambda_handler error: %s' % (error))
        logging.error('lambda_handler trace: %s' % traceback.format_exc())
        cfnresponse.send(event, context, cfnresponse.FAILED, {"success": False, "error": "See Lambda Logs"}, "error")