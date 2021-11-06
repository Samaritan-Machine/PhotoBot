import json
import boto3
import requests

def detect_labels(photo, bucket):
    labels_res = []

    client=boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)

    print('Detected labels for ' + photo) 
    print()   
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        labels_res.append(label['Name'])
        # print ("Confidence: " + str(label['Confidence']))
        # print ("Instances:")
        # for instance in label['Instances']:
        #     print ("  Bounding box")
        #     print ("    Top: " + str(instance['BoundingBox']['Top']))
        #     print ("    Left: " + str(instance['BoundingBox']['Left']))
        #     print ("    Width: " +  str(instance['BoundingBox']['Width']))
        #     print ("    Height: " +  str(instance['BoundingBox']['Height']))
        #     print ("  Confidence: " + str(instance['Confidence']))
        #     print()

        # print ("Parents:")
        # for parent in label['Parents']:
        #     print ("   " + parent['Name'])
        # print ("----------")
        # print ()
    return labels_res

def lambda_handler(event, context):
    # TODO implement
    print(event)
    bucket = "picturesb2"
    for record in event['Records']:
        image_name = record["s3"]["object"]["key"]
        eventtime = record["eventTime"]
        #metadata = s3client.head_object(Bucket=bucket_name, Key=key_name)
       # print("metdata", metadata)
        #given_labels = metadata['Metadata']["customlabel"].split(",")
       # given_labels = [x.strip() for x in given_labels]
        given_labels=[]
        print("given_labels", given_labels)
        print(image_name,eventtime)
        labels_res=detect_labels(image_name, bucket)
        print(labels_res)
        labels_res += given_labels
        temp=[]
        url = "https://search-photosindex-nhstcgewxc644dwhjtcaqel3zi.us-west-2.es.amazonaws.com/photos/_doc"
        headers = {"Content-Type": "application/json"}
        format={'objectkey':image_name,'timstamp':eventtime,'bucket':bucket,'labels':labels_res}
        response = requests.post(url, data=json.dumps(format).encode("utf-8"), headers=headers,auth=('admin', 'Admin@123'))
        dat=json.loads(response.text)
        print (dat)
        # lex = boto3.client('lex-runtime')
        # incoming_msg = "show me cats and dogs"
        # user_id = '111000'
        # bot_name = 'LexSearchBot'
        # response = lex.post_text(
        # botName=bot_name,
        # botAlias=bot_name,
        # userId=user_id,
        # inputText=incoming_msg,
        # )
        # print(response)
        print ("Something")
    return {
        'statusCode': 200,
        'body': json.dumps('Labels added to ES')
    }