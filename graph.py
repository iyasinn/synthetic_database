import pandas as pd
from pyvis.network import Network
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def generate_graph():

    # Read in data
    node_data = supabase.table("modules").select("*").execute()
    df = pd.DataFrame(node_data.data)
    df.to_csv("modules.csv", index=False)

    data = supabase.table("linkages").select("*").execute()
    df = pd.DataFrame(data.data)
    df.to_csv("linkages.csv", index=False)

    # print("Data saved to 'linkages.csv'.")

    # Load data from CSV
    data = pd.read_csv("linkages.csv")
    node_data = pd.read_csv("modules.csv")

    # Ensure identifiers are strings to avoid type issues
    data["parent"] = data["parent"].astype(str)
    data["child"] = data["child"].astype(str)

    # Initialize Pyvis network
    net = Network(
        notebook=True, bgcolor="#222222", font_color="white", height="750px", width="100%", directed=True
    )

    # Sample the data
    sample = data.sample(len(data), random_state=1)
    # Add nodes and edges
    nodes = node_data["module_id"]
    net.add_nodes(nodes)  # Ensure all nodes are added before adding edges

    for node in net.nodes:
        module_id = node["id"]
        node["label"] = f"{module_id}: " + (
            supabase.table("modules")
            .select("*")
            .eq("module_id", module_id)
            .execute()
            .data[0]["name"]
        )

    for idx, row in sample.iterrows():
        # print(idx, int(row["parent"]), int(row["child"]))
        net.add_edge(int(row["parent"]), int(row["child"]))

    # Show the network
    net.show("graph.html")
