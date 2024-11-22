from prometheus_api_client import *
import pandas
from utility import *
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt


def checkSearchMetrics(start_time, end_time, step):
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Checking Memory Usage across the cluster")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    pc = promConnect()

    searchAPIRequestDuration(pc, start_time, end_time, step)
    searchAPIRequestCount(pc, start_time, end_time, step)
    searchAPIDBConnectionFailed(pc, start_time, end_time, step)
    searchAPIDBQueryDuration(pc, start_time, end_time, step)
    searchIndexerRequestCount(pc, start_time, end_time, step)
    searchIndexerRequestDuration(pc, start_time, end_time, step)
    searchIndexerRequestsInFlight(pc, start_time, end_time, step)
    searchIndexerRequestSize(pc, start_time, end_time, step)

    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Memory Health Check  - ", "PLEASE CHECK to see if the results are concerning!! ")
    print("************************************************************************************************")
    print(Style.RESET_ALL)

    return True

def searchAPIRequestDuration(pc, start_time, end_time, step):
    print("95th Percentile Search API Request Duration")

    try:
        # histogram_quantile(0.95, sum(search_api_request_duration_bucket) by (le)) or vector(0) instant value
        search_api_request_duration = pc.custom_query('histogram_quantile(0.95, sum(rate(search_api_request_duration_bucket[30m])) by (le)) or vector(0)')
        search_api_request_duration_df = MetricSnapshotDataFrame(search_api_request_duration)
        search_api_request_duration_df.rename(columns={"value": "SearchAPIRequestDuration95Pctle"}, inplace=True)
        print(search_api_request_duration_df[["SearchAPIRequestDuration95Pctle"]].to_markdown())

        # histogram_quantile(0.95, sum(search_api_request_duration_bucket) by (le)) or vector(0) timeseries
        search_api_request_duration_trend = pc.custom_query_range(
            query="histogram_quantile(0.95, sum(search_api_request_duration_bucket) by (le)) or vector(0)",
            start_time=start_time,
            end_time=end_time,
            step=step,
        )
        search_api_request_duration_trend_df = MetricRangeDataFrame(search_api_request_duration_trend)
        search_api_request_duration_trend_df["value"] = search_api_request_duration_trend_df["value"].astype(float)
        search_api_request_duration_trend_df.index = pandas.to_datetime(search_api_request_duration_trend_df.index, unit="s")
        search_api_request_duration_trend_df.rename(columns={"value": "SearchAPIRequestDuration95Pctle"}, inplace=True)
        search_api_request_duration_trend_df.plot(title="Search API Request Duration 95 Percentile", figsize=(30, 15))
        plt.savefig('../../output/search-api-request-duration-95-percentile.png')
        saveCSV(search_api_request_duration_trend_df, "search-api-request-duration-95-percentile", True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED + "Error getting 95th Percentile Search API Request Duration: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchAPIRequestCount(pc, start_time, end_time, step):
    print("Search API Request Count")

    try:
        # sum(rate(search_api_request_duration_count[30])) or vector(0) instant value
        search_api_request_count = pc.custom_query('sum(rate(search_api_request_duration_count[30m])) or vector(0)')
        search_api_request_count_df = MetricSnapshotDataFrame(search_api_request_count)
        search_api_request_count_df.rename(columns={"value": "SearchAPIRequestCount"}, inplace=True)
        print(search_api_request_count_df[["SearchAPIRequestCount"]].to_markdown())

        # sum(rate(search_api_request_duration_count[30])) or vector(0) timeseries
        search_api_request_count_trend = pc.custom_query_range(
            query="sum(rate(search_api_request_duration_count[30m])) or vector(0)",
            start_time=start_time,
            end_time=end_time,
            step=step,
        )
        search_api_request_count_trend_df = MetricRangeDataFrame(search_api_request_count_trend)
        search_api_request_count_trend_df["value"] = search_api_request_count_trend_df["value"].astype(float)
        search_api_request_count_trend_df.index = pandas.to_datetime(search_api_request_count_trend_df.index, unit="s")
        search_api_request_count_trend_df.rename(columns={"value": "SearchAPIRequestCount"}, inplace=True)
        search_api_request_count_trend_df.plot(title="Search API Request Count", figsize=(30, 15))
        plt.savefig('../../output/search-api-request-count.png')
        saveCSV(search_api_request_count_trend_df, "search-api-request-count", True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED + "Error getting Search API Request Count: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchAPIDBConnectionFailed(pc, start_time, end_time, step):
    print("Search API DB Connection Failed")

    try:
        # search_api_db_connection_failed instant value
        db_conn_failed = pc.custom_query('search_api_db_connection_failed')
        db_conn_failed_df = MetricSnapshotDataFrame(db_conn_failed)
        db_conn_failed_df.rename(columns={"value": "SearchAPIDBConnectionFailed"}, inplace=True)
        print(db_conn_failed_df[["SearchAPIDBConnectionFailed"]].to_markdown())

        # search_api_db_connection_failed timeseries
        db_conn_failed_trend = pc.custom_query_range(
            query="search_api_db_connection_failed",
            start_time=start_time,
            end_time=end_time,
            step=step,
        )
        db_conn_failed_trend_df = MetricRangeDataFrame(db_conn_failed_trend)
        db_conn_failed_trend_df["value"] = db_conn_failed_trend_df["value"].astype(float)
        db_conn_failed_trend_df.index = pandas.to_datetime(db_conn_failed_trend_df.index, unit="s")
        db_conn_failed_trend_df.sort_index(inplace=True)  # records not always presented in proper time order
        db_conn_failed_trend_df.rename(columns={"value": "SearchAPIDBConnectionFailed"}, inplace=True)
        db_conn_failed_trend_df.plot(title="Search API DB Connection Failed", figsize=(30, 15))
        plt.savefig('../../output/search-api-db-connection-failed.png')
        saveCSV(db_conn_failed_trend_df, "search-api-db-connection-failed", True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED + "Error getting Search API DB Connection Failed: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchAPIDBQueryDuration(pc, start_time, end_time, step):
    print("95th Percentile Search API DB Query Duration")

    try:
        # histogram_quantile(0.95, sum(search_api_db_query_duration_bucket) by (le)) or vector(0) instant value
        search_api_db_query_duration = pc.custom_query('histogram_quantile(0.95, sum(rate(search_api_db_query_duration_bucket[30m])) by (le)) or vector(0)')
        search_api_db_query_duration_df = MetricSnapshotDataFrame(search_api_db_query_duration)
        search_api_db_query_duration_df.rename(columns={"value": "SearchAPIDBQueryDuration95Pctle"}, inplace=True)
        print(search_api_db_query_duration_df[["SearchAPIDBQueryDuration95Pctle"]].to_markdown())

        # histogram_quantile(0.95, sum(search_api_db_query_duration_bucket) by (le)) or vector(0) timeseries
        search_api_db_query_duration_trend = pc.custom_query_range(
            query="histogram_quantile(0.95, sum(search_api_db_query_duration_bucket) by (le)) or vector(0)",
            start_time=start_time,
            end_time=end_time,
            step=step,
        )
        search_api_db_query_duration_trend_df = MetricRangeDataFrame(search_api_db_query_duration_trend)
        search_api_db_query_duration_trend_df["value"] = search_api_db_query_duration_trend_df["value"].astype(float)
        search_api_db_query_duration_trend_df.index = pandas.to_datetime(search_api_db_query_duration_trend_df.index, unit="s")
        search_api_db_query_duration_trend_df.rename(columns={"value": "SearchAPIDBQueryDuration95Pctle"}, inplace=True)
        search_api_db_query_duration_trend_df.plot(title="Search API DB Query Duration 95 Percentile", figsize=(30, 15))
        plt.savefig('../../output/search-api-db-query-duration-95-percentile.png')
        saveCSV(search_api_db_query_duration_trend_df, "search-api-db-query-duration-95-percentile", True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED + "Error getting 95th Percentile Search API DB Query Duration: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchIndexerRequestCount(pc, start_time, end_time, step):
    print("Search Indexer Request Count")

    try:
        # search_indexer_request_count instant value
        search_indexer_request_count = pc.custom_query('sum(search_indexer_request_count)')
        search_indexer_request_count_df = MetricSnapshotDataFrame(search_indexer_request_count)
        search_indexer_request_count_df.rename(columns={"value": "SearchIndexerRequestCount"}, inplace=True)
        print(search_indexer_request_count_df[["SearchIndexerRequestCount"]].to_markdown())

        # search_indexer_request_count timeseries
        search_indexer_request_count_trend = pc.custom_query_range(
            query="sum(search_indexer_request_count)",
            start_time=start_time,
            end_time=end_time,
            step=step,
        )
        search_indexer_request_count_trend_df = MetricRangeDataFrame(search_indexer_request_count_trend)
        search_indexer_request_count_trend_df["value"] = search_indexer_request_count_trend_df["value"].astype(float)
        search_indexer_request_count_trend_df.index = pandas.to_datetime(search_indexer_request_count_trend_df.index, unit="s")
        search_indexer_request_count_trend_df.sort_index(inplace=True)  # records not always presented in proper time order
        search_indexer_request_count_trend_df.rename(columns={"value": "SearchIndexerRequestCount"}, inplace=True)
        search_indexer_request_count_trend_df.plot(title="Search Indexer Request Count", figsize=(30, 15))
        plt.savefig('../../output/search-indexer-request-count.png')
        saveCSV(search_indexer_request_count_trend_df, "search-indexer-request-count", True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED + "Error getting Search Indexer Request Count: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchIndexerRequestDuration(pc, start_time, end_time, step):
    print("95th Percentile Search Indexer Request Duration")

    try:
        # histogram_quantile(0.95, sum(search_indexer_request_duration_bucket) by (le)) or vector(0) instant value
        search_indexer_request_duration = pc.custom_query('histogram_quantile(0.95, sum(rate(search_indexer_request_duration_bucket[30m])) by (le)) or vector(0)')
        search_indexer_request_duration_df = MetricSnapshotDataFrame(search_indexer_request_duration)
        search_indexer_request_duration_df.rename(columns={"value": "SearchIndexerRequestDuration95Pctle"}, inplace=True)
        print(search_indexer_request_duration_df[["SearchIndexerRequestDuration95Pctle"]].to_markdown())

        # histogram_quantile(0.95, sum(search_indexer_request_duration_bucket) by (le)) or vector(0) timeseries
        search_indexer_request_duration_trend = pc.custom_query_range(
            query="histogram_quantile(0.95, sum(search_indexer_request_duration_bucket) by (le)) or vector(0)",
            start_time=start_time,
            end_time=end_time,
            step=step,
        )
        search_indexer_request_duration_trend_df = MetricRangeDataFrame(search_indexer_request_duration_trend)
        search_indexer_request_duration_trend_df["value"] = search_indexer_request_duration_trend_df["value"].astype(float)
        search_indexer_request_duration_trend_df.index = pandas.to_datetime(search_indexer_request_duration_trend_df.index, unit="s")
        search_indexer_request_duration_trend_df.rename(columns={"value": "SearchIndexerRequestDuration95Pctle"}, inplace=True)
        search_indexer_request_duration_trend_df.plot(title="Search Indexer Request Duration 95 Percentile", figsize=(30, 15))
        plt.savefig('../../output/search-indexer-request-duration-95-percentile.png')
        saveCSV(search_indexer_request_duration_trend_df, "search-indexer-request-duration-95-percentile", True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED + "Error getting 95th Percentile Search Indexer Request Duration: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchIndexerRequestsInFlight(pc, start_time, end_time, step):
    print("Search Indexer Requests In Flight")

    try:
        # search_indexer_requests_in_flight instant value
        search_indexer_requests_in_flight = pc.custom_query('sum(search_indexer_requests_in_flight)')
        search_indexer_requests_in_flight_df = MetricSnapshotDataFrame(search_indexer_requests_in_flight)
        search_indexer_requests_in_flight_df.rename(columns={"value": "SearchIndexerRequestsInFlight"}, inplace=True)
        print(search_indexer_requests_in_flight_df[["SearchIndexerRequestsInFlight"]].to_markdown())

        # search_indexer_requests_in_flight timeseries
        search_indexer_requests_in_flight_trend = pc.custom_query_range(
            query="sum(search_indexer_requests_in_flight)",
            start_time=start_time,
            end_time=end_time,
            step=step,
        )
        search_indexer_requests_in_flight_trend_df = MetricRangeDataFrame(search_indexer_requests_in_flight_trend)
        search_indexer_requests_in_flight_trend_df["value"] = search_indexer_requests_in_flight_trend_df["value"].astype(float)
        search_indexer_requests_in_flight_trend_df.index = pandas.to_datetime(search_indexer_requests_in_flight_trend_df.index, unit="s")
        search_indexer_requests_in_flight_trend_df.rename(columns={"value": "SearchIndexerRequestsInFlight"}, inplace=True)
        search_indexer_requests_in_flight_trend_df.plot(title="Search Indexer Requests In Flight", figsize=(30, 15))
        plt.savefig('../../output/search-indexer-requests-in-flight.png')
        saveCSV(search_indexer_requests_in_flight_trend_df, "search-indexer-requests-in-flight", True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED + "Error getting Search Indexer Requests In Flight: ", e)
        print(Style.RESET_ALL)
    print("=============================================")

def searchIndexerRequestSize(pc, start_time, end_time, step):
    print("95th Percentile Search Indexer Request Size")

    try:
        # histogram_quantile(0.95, sum(search_indexer_request_size_bucket) by (le)) or vector(0) instant value
        search_indexer_request_size = pc.custom_query('histogram_quantile(0.95, sum(rate(search_indexer_request_size_bucket[30m])) by (le)) or vector(0)')
        search_indexer_request_size_df = MetricSnapshotDataFrame(search_indexer_request_size)
        search_indexer_request_size_df.rename(columns={"value": "SearchIndexerRequestSize95Pctle"}, inplace=True)
        print(search_indexer_request_size_df[["SearchIndexerRequestSize95Pctle"]].to_markdown())

        # histogram_quantile(0.95, sum(search_indexer_request_size_bucket) by (le)) or vector(0) timeseries
        search_indexer_request_size_trend = pc.custom_query_range(
            query="histogram_quantile(0.95, sum(search_indexer_request_size_bucket) by (le)) or vector(0)",
            start_time=start_time,
            end_time=end_time,
            step=step,
        )
        search_indexer_request_size_trend_df = MetricRangeDataFrame(search_indexer_request_size_trend)
        search_indexer_request_size_trend_df["value"] = search_indexer_request_size_trend_df["value"].astype(float)
        search_indexer_request_size_trend_df.index = pandas.to_datetime(search_indexer_request_size_trend_df.index, unit="s")
        search_indexer_request_size_trend_df.rename(columns={"value": "SearchIndexerRequestSize95Pctle"}, inplace=True)
        search_indexer_request_size_trend_df.plot(title="Search Indexer Request Size 95 Percentile", figsize=(30, 15))
        plt.savefig('../../output/search-indexer-request-size-95-percentile.png')
        saveCSV(search_indexer_request_size_trend_df, "search-indexer-request-size-95-percentile", True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED + "Error getting 95th Percentile Search Indexer Request Size: ", e)
        print(Style.RESET_ALL)
    print("=============================================")
