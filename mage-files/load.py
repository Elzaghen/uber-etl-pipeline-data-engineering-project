from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery

    
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    table_ids = [
        "datetime_dim",
        "passenger_count_dim",
        "trip_distance_dim",
        "rate_code_dim",
        "pickup_location_dim",
        "dropoff_location_dim",
        "payment_type_dim",
        "fact_table"
    ]
    project_id = "'data-with-darshil.uber_data_engineering_yt"
    
    bigquery_client = BigQuery.with_config(ConfigFileLoader(config_path, config_profile))

    for i, table_name in enumerate(table_ids):
        bigquery_client.export(
            df[i],
            table_id=f"{project_id}.{table_name}",
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
