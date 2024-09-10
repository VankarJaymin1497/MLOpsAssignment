from bigquery_sdk.bigquery_client import MultiProjectBigQueryClient
from bigquery_sdk.auth import get_credentials_from_service_account

# Service account key paths and project IDs
project_ids = ["mlops-project-exercise-3", "new-project-exercise5"] # Add all the project IDs here
key_paths = ["/Users/Jaymin/Desktop/MLOps Assignment/Exercise5/mlops-project-exercise-3-92deec2bc326.json", 
             "/Users/Jaymin/Desktop/MLOps Assignment/Exercise5/new-project-exercise5-784b8b84d03d.json"] #add path of all the JSON key files here

# Initialize the MultiProject client
client = MultiProjectBigQueryClient(project_ids, key_paths)

# Listing datasets across all projects
datasets = client.list_all_datasets()
print(dict(datasets))

# Running a query on a specific project
results = client.run_query_in_project("SELECT * FROM `new-project-exercise5.exercise5Data.my_table1_exercise5`", "new-project-exercise5")

#print(results)
for row in results:
    print(dict(row))

#Many more queries can be run here. Ex, INSERT INTO table, Select * From table, etc.


