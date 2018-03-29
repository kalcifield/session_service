
you need a dynamodb running

how to start session microservice:
-set variables in config.json (host, port etc..)
-run app.py

how to start integration test:
-set config.json
-run request_test.py
-in order to run session expiry tests, switch
      go to database.py check_session_creation, check_session_last_use
On WINDOWS:
timezone has to be set to utc 0:00 for dynamodb to work properly.
(https://github.com/boto/boto3/issues/1238)
 ¯\_(ツ)_/¯
