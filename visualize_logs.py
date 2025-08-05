import json
import pandas as pd
import plotly.express as px

def load_parsed_log(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def visualize_events(events):
    df_data = []

    for event in events:
        try:
            timestamp = int(event["timestamp"].replace("ns", "").strip())
        except:
            continue  # skip malformed timestamps

        df_data.append({
            "Time_ns": timestamp,
            "Event Type": event.get("level", "UNKNOWN"),
            "Module": event.get("module", "unknown"),
            "Message": event.get("message", ""),
            "File": event.get("file", ""),
            "Line": event.get("line", ""),
        })

    df = pd.DataFrame(df_data)

    # Sort by time
    df = df.sort_values(by="Time_ns")

    # Create scatter plot with vertical layout
    fig = px.scatter(
        df,
        x="Time_ns",
        y="Module",
        color="Event Type",
        hover_data=["Message", "File", "Line"],
        title="AXI Simulation Timeline",
        labels={"Time_ns": "Simulation Time (ns)", "Module": "Source Module"}
    )

    fig.update_traces(marker=dict(size=12))
    fig.update_layout(
        yaxis=dict(title="Module"),
        xaxis=dict(title="Simulation Time (ns)")
    )

    fig.show()

if __name__ == "__main__":
    events = load_parsed_log("output/parsed_log.json")
    visualize_events(events)
    