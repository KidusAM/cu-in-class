import json
import boto3
from datetime import datetime, date

dynamodb = boto3.client('dynamodb')
ATTENDANCES_TABLE = 'attendance'
QUESTIONS_TABLE = 'questions'

def make_attendance_id(class_id, date):
    return str(class_id) + '+' + str(date)

def mark_present(event):
    request_body = json.loads(event['body'])
    class_id = request_body['class_id']
    student_id = request_body['student_id']
    key = {
        'class_id' : {'S' : make_attendance_id(class_id, date.today())}
    }
    update = {
        student_id : {
            'Value' : {'S' : '1'}
        }
    }

    dynamodb.update_item(
        TableName = ATTENDANCES_TABLE, Key=key, AttributeUpdates = update)

    return {
        'statusCode': 200,
        'headers': {
             'Access-Control-Allow-Origin' : '*'
        },
        'body' : student_id + " has been marked present"
    }

def ask_question(event):
    request_body = json.loads(event['body'])
    class_id = request_body['class_id']
    student_id = request_body['student_id']
    question_text = request_body['question_text']
    key = {
        'class_id' : {'S' : make_attendance_id(class_id, date.today())}
    }
    question_key = student_id + '+' + str(datetime.now())
    update = {
        question_key : {
            'Value' : {'S' : question_text}
        }
    }

    dynamodb.update_item(
        TableName = QUESTIONS_TABLE, Key=key, AttributeUpdates = update)

    return {
        'statusCode': 200,
        'headers': {
             'Access-Control-Allow-Origin' : '*'
        },
        'body' : json.dumps("question has been posted")
    }

def get_values_by_class_id(table_name, class_id):
    key = {
        'class_id'  : {'S' : make_attendance_id(class_id, date.today())}
    }
    result = dynamodb.get_item(TableName = table_name, Key = key)

    return result['Item'] if 'Item' in result else {}

def get_questions(event):
    request_params = event['queryStringParameters']
    class_id = request_params['class_id']

    output_results = {}
    for key,question_text in get_values_by_class_id(QUESTIONS_TABLE, class_id).items():
        if key == 'class_id':
            continue
        student_id, _, question_time = key.partition('+')
        output_results[key] = {
            "student_id" : student_id,
            "question_time" : question_time,
            "question_text" : question_text["S"]
        }

    return {
        'statusCode' : 200,
        'headers': {
             'Access-Control-Allow-Origin' : '*'
        },
        'body' : json.dumps(output_results)
    }

def get_attendances(event):
    class_id = event['queryStringParameters']['class_id']

    output_results = {}
    for uni, is_present in get_values_by_class_id(ATTENDANCES_TABLE, class_id).items():
        if uni == 'class_id':
            continue
        output_results[uni] = int(is_present['S'])

    return {
        'statusCode' : 200,
        'headers': {
             'Access-Control-Allow-Origin' : '*'
        },
        'body' : json.dumps(output_results)
    }

handlers = {
    "/post_question" : ask_question,
    "/mark_present" : mark_present,
    "/get_questions" : get_questions,
    "/get_attendances" : get_attendances,
}

def lambda_handler(event, context):
    print(json.dumps(event))
    handler_function = handlers.get(event['resource'], None)
    if not handler_function:
        return {
            'statusCode': 500,
            'body' : "No handler for resource " + event['resource']
        }

    return handler_function(event)
