import pandas as pd
import numpy as np
import requests
import json
import csv
import yaml
import boto3
import os
from io import StringIO



def saveData(URL, headers, outputFile):
    print("Starting " + outputFile + "...")

    s3 = boto3.resource('s3')  
    outputFilePath = "representatives/" + outputFile
    bucket = 'gov-connect'

    response = requests.get(url = URL, headers = headers)
    df = json.loads(response.text)
    outputDF = pd.DataFrame(df['results'][0]['members'])

    csv_buffer = StringIO()
    outputDF.to_csv(csv_buffer)
    s3.Object(bucket, outputFilePath).put(Body=csv_buffer.getvalue())
    print("--- Created " + outputFile)


def main():
    #load in configurations
    with open("keys.yml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    # save house members list
    URL = 'https://api.propublica.org/congress/v1/116/house/members.json'
    headers = {'x-api-key': config['keys.propublica']}
    saveData(URL=URL, headers=headers, outputFile='house_members.csv')

    # save senate members list
    URL = 'https://api.propublica.org/congress/v1/116/senate/members.json'
    saveData(URL=URL, headers=headers, outputFile='senate_members.csv')


# if __name__ == "__main__":
    # main()

def lambda_handler(event, lambda_context):
    main()