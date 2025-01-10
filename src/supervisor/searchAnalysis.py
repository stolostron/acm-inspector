from prometheus_api_client import *
import pandas
from utility import *
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt


def checkSearchMetrics(start_time, end_time, step):
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Checking Search Metrics across the cluster")
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
    print("Search Metrics Check - ", "PLEASE CHECK to see if the results are concerning!! ")
    print("************************************************************************************************")
    print(Style.RESET_ALL)

    return True


def metricSnapshot(pc, query, col_name):
    result = pc.custom_query(query)
    result_df = MetricSnapshotDataFrame(result)
    result_df.rename(columns={"value": col_name}, inplace=True)
    print(result_df[[col_name]].to_markdown())


def metricRange(pc, query, col_name, plot_title, file_name, start_time, end_time, step):
    request_trend = pc.custom_query_range(
        query=query,
        start_time=start_time,
        end_time=end_time,
        step=step,
    )
    request_trend_df = MetricRangeDataFrame(request_trend)
    request_trend_df["value"] = request_trend_df["value"].astype(float)
    request_trend_df.index = pandas.to_datetime(request_trend_df.index, unit="s")
    request_trend_df.rename(columns={"value": col_name}, inplace=True)
    request_trend_df.plot(title=plot_title, figsize=(30, 15))
    plt.savefig("../../" + file_name + ".png")
    saveCSV(request_trend_df, file_name, True)
    plt.close("all")


def searchAPIRequestDuration(pc, start_time, end_time, step):
    print("95th Percentile Search API Request Duration")

    try:
        metricSnapshot(pc,
                       "histogram_quantile(0.95, sum(rate(search_api_request_duration_bucket[30m])) by (le)) or vector(0)",
                       "SearchAPIRequestDuration95Pctle")
        metricRange(pc,
                    "histogram_quantile(0.95, sum(rate(search_api_request_duration_bucket[30m])) by (le)) or vector(0)",
                    "SearchAPIRequestDuration95Pctle",
                    "Search API Request Duration 95 Percentile",
                    "search-api-request-duration-95-percentile",
                    start_time,
                    end_time,
                    step)
    except Exception as e:
        print(Fore.RED + "Error getting 95th Percentile Search API Request Duration: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchAPIRequestCount(pc, start_time, end_time, step):
    print("Search API Request Count")

    try:
        metricSnapshot(pc,
                       "sum(rate(search_api_request_duration_count[30m])) or vector(0)",
                       "SearchAPIRequestCount")
        metricRange(pc,
                    "sum(rate(search_api_request_duration_count[30m])) or vector(0)",
                    "SearchAPIRequestCount",
                    "Search API Request Count",
                    "search-api-request-count",
                    start_time,
                    end_time,
                    step)
    except Exception as e:
        print(Fore.RED + "Error getting Search API Request Count: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchAPIDBConnectionFailed(pc, start_time, end_time, step):
    print("Search API DB Connection Failed")

    try:
        metricSnapshot(pc,
                       "sum(rate(search_api_db_connection_failed[30m])) or vector(0)",
                       "SearchAPIDBConnectionFailed")
        metricRange(pc,
                    "sum(rate(search_api_db_connection_failed[30m])) or vector(0)",
                    "SearchAPIDBConnectionFailed",
                    "Search API DB Connection Failed",
                    "search-api-db-connection-failed",
                    start_time,
                    end_time,
                    step)
    except Exception as e:
        print(Fore.RED + "Error getting Search API DB Connection Failed: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchAPIDBQueryDuration(pc, start_time, end_time, step):
    print("95th Percentile Search API DB Query Duration")

    try:
        metricSnapshot(pc,
                       "histogram_quantile(0.95, sum(rate(search_api_db_query_duration_bucket[30m])) by (le)) or vector(0)",
                       "SearchAPIDBQueryDuration95Pctle")
        metricRange(pc,
                    "histogram_quantile(0.95, sum(rate(search_api_db_query_duration_bucket[30m])) by (le)) or vector(0)",
                    "SearchAPIDBQueryDuration95Pctle",
                    "Search API DB Query Duration 95 Percentile",
                    "search-api-db-query-duration-95-percentile",
                    start_time,
                    end_time,
                    step)
    except Exception as e:
        print(Fore.RED + "Error getting 95th Percentile Search API DB Query Duration: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchIndexerRequestCount(pc, start_time, end_time, step):
    print("Search Indexer Request Count")

    try:
        metricSnapshot(pc,
                       "sum(rate(search_indexer_request_count[30m])) or vector(0)",
                       "SearchIndexerRequestCount")
        metricRange(pc,
                    "sum(rate(search_indexer_request_count[30m])) or vector(0)",
                    "SearchIndexerRequestCount",
                    "Search Indexer Request Count",
                    "search-indexer-request-count",
                    start_time,
                    end_time,
                    step)
    except Exception as e:
        print(Fore.RED + "Error getting Search Indexer Request Count: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchIndexerRequestDuration(pc, start_time, end_time, step):
    print("95th Percentile Search Indexer Request Duration")

    try:
        metricSnapshot(pc,
                       "histogram_quantile(0.95, sum(rate(search_indexer_request_duration_bucket[30m])) by (le)) or vector(0)",
                       "SearchIndexerRequestDuration95Pctle")
        metricRange(pc,
                    "histogram_quantile(0.95, sum(rate(search_api_db_query_duration_bucket[30m])) by (le)) or vector(0)",
                    "SearchIndexerRequestDuration95Pctle",
                    "Search Indexer Request Duration 95 Percentile",
                    "search-indexer-request-duration-95-percentile",
                    start_time,
                    end_time,
                    step)
    except Exception as e:
        print(Fore.RED + "Error getting 95th Percentile Search Indexer Request Duration: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchIndexerRequestsInFlight(pc, start_time, end_time, step):
    print("Search Indexer Requests In Flight")

    try:
        metricSnapshot(pc,
                       "sum(rate(search_indexer_requests_in_flight[30m])) or vector(0)",
                       "SearchIndexerRequestsInFlight")
        metricRange(pc,
                    "sum(rate(search_indexer_requests_in_flight[30m])) or vector(0)",
                    "SearchIndexerRequestsInFlight",
                    "Search Indexer Requests In Flight",
                    "search-indexer-requests-in-flight",
                    start_time,
                    end_time,
                    step)
    except Exception as e:
        print(Fore.RED + "Error getting Search Indexer Requests In Flight: ", e)
        print(Style.RESET_ALL)
    print("=============================================")


def searchIndexerRequestSize(pc, start_time, end_time, step):
    print("95th Percentile Search Indexer Request Size")

    try:
        metricSnapshot(pc,
                       "histogram_quantile(0.95, sum(rate(search_indexer_request_size_bucket[30m])) by (le)) or vector(0)",
                       "SearchIndexerRequestSize95Pctle")
        metricRange(pc,
                    "histogram_quantile(0.95, sum(rate(search_indexer_request_size_bucket[30m])) by (le)) or vector(0)",
                    "SearchIndexerRequestSize95Pctle",
                    "Search Indexer Request Size 95 Percentile",
                    "search-indexer-request-size-95-percentile",
                    start_time,
                    end_time,
                    step)
    except Exception as e:
        print(Fore.RED + "Error getting 95th Percentile Search Indexer Request Size: ", e)
        print(Style.RESET_ALL)
    print("=============================================")
