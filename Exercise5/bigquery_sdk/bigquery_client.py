from google.cloud import bigquery
from bigquery_sdk.auth import get_credentials_from_service_account

class BigQueryClient:
    def __init__(self, project_id=None, key_path=None):
        if key_path:
            self.credentials = get_credentials_from_service_account(key_path)
        else:
            self.credentials = None
        self.client = bigquery.Client(project=project_id, credentials=self.credentials)

    def run_query(self, query):
        """Run a SQL query and return the results."""
        query_job = self.client.query(query)
        results = query_job.result()
        return results

    def get_datasets(self):
        """List all datasets in the project."""
        datasets = list(self.client.list_datasets())
        return datasets

    def get_tables(self, dataset_id):
        """List all tables in a dataset."""
        dataset_ref = self.client.dataset(dataset_id)
        tables = list(self.client.list_tables(dataset_ref))
        return tables

class MultiProjectBigQueryClient:
    def __init__(self, project_ids, key_paths):
        self.clients = {}
        for project_id, key_path in zip(project_ids, key_paths):
            self.clients[project_id] = BigQueryClient(project_id, key_path)

    def run_query_in_project(self, query, project_id):
        if project_id in self.clients:
            return self.clients[project_id].run_query(query)
        raise ValueError(f"Project {project_id} not found in configured clients.")

    def list_all_datasets(self):
        datasets = {}
        for project_id, client in self.clients.items():
            datasets[project_id] = client.get_datasets()
        return datasets
