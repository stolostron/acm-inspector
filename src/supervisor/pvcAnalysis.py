from prometheus_api_client import *
import pandas
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt
import seaborn as sns
import os


def checkPVCUsage(pc, start_time, end_time, step, namespace, name=""):
    title = f"ACM {namespace}" + (f"/{name}" if name else "") + " PVC Usage"
    file = f"{namespace}-" + (f"{name}-" if name else "") + "pvc-usage"
    output_file = os.path.join(os.path.dirname(__file__), "../../output", file)

    print(title)
    try:

        if name:
            query_sql = f"""sum(kubelet_volume_stats_used_bytes{{job='kubelet', metrics_path='/metrics', namespace='{namespace}', persistentvolumeclaim=~'{name}'}}) by (persistentvolumeclaim) / (1024*1024)"""
            title = title + " MB"
        else:
            query_sql = f"""sum(kubelet_volume_stats_used_bytes{{job='kubelet', metrics_path='/metrics', namespace='{namespace}'}}) / (1024*1024*1024)"""
            title = title + " GB"

        pvc_trend = pc.custom_query_range(
            query=query_sql,
            start_time=start_time,
            end_time=end_time,
            step=step,
        )

        pvc_trend_df = MetricRangeDataFrame(pvc_trend)
        pvc_trend_df["value"] = pvc_trend_df["value"].astype(float)
        pvc_trend_df.index = pandas.to_datetime(pvc_trend_df.index, unit="s")
        pvc_trend_df.rename(columns={"value": "Storage"}, inplace=True)

        print(pvc_trend_df.head(3))
        # pvc_trend_df.plot(title=title, figsize=(18, 10))

        plt.figure(figsize=(18, 10))

        if name:
            sns.lineplot(
                x="timestamp",
                y="Storage",
                data=pvc_trend_df,
                hue="persistentvolumeclaim",
            )
        else:
            sns.lineplot(
                x="timestamp",
                y="Storage",
                data=pvc_trend_df,
            )
        plt.title(title)
        plt.savefig(output_file + ".png")
        pvc_trend_df.to_csv(output_file + ".csv", index=True, header=True)
        plt.close("all")

    except Exception as e:
        print(Fore.RED + "Error in getting PVC for cluster: ", e)
        print(Style.RESET_ALL)

    print("---------------------------------------------------------------------------")
