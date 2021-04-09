from diagrams import Cluster, Diagram, Edge
from diagrams.programming.language import Python
from diagrams.custom import Custom
from urllib.request import urlretrieve

graph_attr = {"fontsize": "45"}

with Diagram("Technical Architecture", show=False, graph_attr=graph_attr):
    unity_url = (
        "https://cdn.freebiesupply.com/logos/large/2x/unity-69-logo-png-transparent.png"
    )
    unity_icon = "unity-69-logo-png-transparent.png"
    urlretrieve(unity_url, unity_icon)
    nextmind_app = Custom("NextMind App", unity_icon)
    with Cluster("Azure"):
        cloud_agent = Python("GRPC Forwarder")
    with Cluster("ROCOS"):
        grpc_url = "https://www.grpc.io/img/logos/grpc-logo.png"
        grpc_icon = "grpc-logo.png"
        urlretrieve(grpc_url, grpc_icon)

        grpc = Custom("Rocos", grpc_icon)
    nextmind_app >> Edge(color="darkgreen") << cloud_agent
    cloud_agent >> Edge(color="darkgreen") << grpc