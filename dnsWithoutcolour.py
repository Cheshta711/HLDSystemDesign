# Advanced DNS HLD Architecture
# Run in Google Colab

!pip install -q graphviz

from graphviz import Digraph

dot = Digraph("DNS_HLD_Advanced", format="png")
dot.attr(rankdir="LR", fontsize="12", bgcolor="white")

# =====================
# CLIENT LAYER
# =====================
with dot.subgraph(name="cluster_client") as c:
    c.attr(label="Client Layer", style="dashed")
    c.node("Client", "Client\nBrowser / OS Resolver", shape="cloud")

# =====================
# EDGE & TRAFFIC
# =====================
with dot.subgraph(name="cluster_edge") as e:
    e.attr(label="Edge & Traffic Management", style="dashed")
    e.node("Anycast", "Anycast Routing", shape="circle")
    e.node("LB", "Global Load Balancer", shape="circle")
    e.node("RateLimit", "Rate Limiter", shape="parallelogram")

# =====================
# RESOLUTION CORE
# =====================
with dot.subgraph(name="cluster_core") as core:
    core.attr(label="Resolution Core", style="dashed")
    core.node("Resolver", "Recursive DNS Resolver\n(Stateless Pool)", shape="box")
    core.node("Cache", "Distributed DNS Cache\nTTL-based", shape="box", style="rounded")
    core.node("Decision", "Cache Valid?", shape="diamond")

# =====================
# DNS HIERARCHY
# =====================
with dot.subgraph(name="cluster_hierarchy") as h:
    h.attr(label="DNS Hierarchy", style="dashed")
    h.node("Root", "Root Name Servers", shape="rectangle")
    h.node("TLD", "TLD Name Servers", shape="rectangle")
    h.node("Auth", "Authoritative Name Servers", shape="box")

# =====================
# DATA LAYER
# =====================
with dot.subgraph(name="cluster_data") as d:
    d.attr(label="Data & State", style="dashed")
    d.node("ZoneDB", "Zone File Storage", shape="cylinder")
    d.node("Replica", "Read Replicas", shape="cylinder")

# =====================
# CROSS-CUTTING (VERTICAL)
# =====================
with dot.subgraph(name="cluster_vertical") as v:
    v.attr(label="Cross-Cutting Services", style="bold")
    v.node("AuthZ", "AuthZ / Policy Engine", shape="parallelogram")
    v.node("Lambda", "Serverless\nLogs / Validation", shape="hexagon")
    v.node("Monitor", "Monitoring & Alerting", shape="rectangle")

# =====================
# PRIMARY FLOW (HORIZONTAL)
# =====================
dot.edge("Client", "Anycast")
dot.edge("Anycast", "LB")
dot.edge("LB", "RateLimit")
dot.edge("RateLimit", "Resolver")

dot.edge("Resolver", "Cache")
dot.edge("Cache", "Decision")

dot.edge("Decision", "Resolver", label="Hit")
dot.edge("Decision", "Root", label="Miss")

dot.edge("Root", "TLD")
dot.edge("TLD", "Auth")

dot.edge("Auth", "ZoneDB")
dot.edge("ZoneDB", "Replica")
dot.edge("Auth", "Resolver")

# =====================
# VERTICAL INTERACTIONS
# =====================
dot.edge("Resolver", "Lambda", style="dotted")
dot.edge("Auth", "Lambda", style="dotted")

dot.edge("Lambda", "Monitor", style="dotted")
dot.edge("LB", "Monitor", style="dotted")
dot.edge("Resolver", "Monitor", style="dotted")

dot.edge("Client", "AuthZ", style="dotted")
dot.edge("AuthZ", "RateLimit", style="dotted")

# =====================
# DISPLAY
# =====================
dot
