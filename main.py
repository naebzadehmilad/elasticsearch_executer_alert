from elasticsearch import Elasticsearch
import argparse
import json
import requests
import os

def execute_es_query():


    parser = argparse.ArgumentParser(description='Elasticsearch Query Executor')
    parser.add_argument('-f', '--file', help='filename/path containing the Elasticsearch query', required=True)
    parser.add_argument('-H', '--host', help='Elasticsearch url, e.g., http://127.0.0.1:9200', required=True)
    parser.add_argument('-u', '--user', help='Elasticsearch username', required=False)
    parser.add_argument('-p', '--password', help='Elasticsearch password', required=False)
    parser.add_argument('-i', '--index', help='Elasticsearch target index ', required=True)
    parser.add_argument('-S', '--slack', help='Enable Slack integration', action='store_true', required=False)
    parser.add_argument('-M', '--message', help='Custom message for Slack', required=False)
    args = parser.parse_args()

    if args.host:
        es = Elasticsearch([args.host], basic_auth=(args.user, args.password))

    try:
        with open(args.file, 'r') as file:
            query = json.load(file)

        result = es.search(index=args.index, body=query)
        aggregation_items = list(result['aggregations'].items())
        aggregation_items_edited = '\n'.join(map(str, aggregation_items)).replace(',', '\n')
        took_time = f'Took time for the query result: {result["took"]} ms'
        print(aggregation_items_edited)
        print('\n' * 3 + took_time)


    except Exception as e:
        print(f"An error occurred: {e}")

    if len(result.get('hits', [])) != 0:
      if args.slack:
         credentials = read_slack_credentials()
         if args.message:
            message = args.message
         else:
            message = "Use -M for a custom message."
         aggregated_message = f"{message}\n\n{aggregation_items_edited}"
         send_to_slack(
            aggregated_message,
            credentials["channel"],
            credentials["webhook_url"]
         )
    else:
      print("Elasticsearch query result is empty. Skipping Slack notification.")



def send_to_slack(message, channel, webhook_url):
    payload = {
        "text": message,
        "channel": channel
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message to Slack. Error: {response.text}")
    else:
        print("Message sent successfully to Slack!")

def read_slack_credentials(filename='slack_credentials.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            slack_credentials = json.load(file)
    else:
        print(f"\n\nThe file {filename} does not exist.")
        print('''
              {
               "channel": "your-channelname",
               "webhook_url": "https://hooks.slack.com/services/******************"

                                                                                      }
                                                                                       ''')
    return slack_credentials


if __name__ == "__main__":
    execute_es_query()
