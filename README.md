# elasticsearch_executer_alert <br />
create an Elasticsearch alert to slack from query<br />



Usage<br />
Run the script main.py with the following command-line arguments:<br />

-H or --host: Elasticsearch URL, e.g., http://elasticsearch_ip:9200<br />
-u or --user: Elasticsearch username (if required) <br />
-p or --password: Elasticsearch password (if required) <br />
-i or --index: Elasticsearch target index pattern, for example, *nginx* <br /> 
-f or --file: Path to the Elasticsearch DSL query file <br /> 
-S or --slack: Enable sending notifications to Slack <br />
-M or --message: Title message for the Slack alert <br />

Example command:  <br />

python3.8 main.py -H http://elasticsearch_ip:9200 -u USER -p PASSWORD -i *nginx* -f ./dsl-query/200.json -S -M 'alert----elasticsearch'
