# DNS System - Advanced Hybrid HLD
# Run in Google Colab

!pip install -q graphviz

from graphviz import Digraph

dot = Digraph("DNS_Advanced_HLD", format="png")

# =========================
# GLOBAL STYLE
# =========================
dot.attr(
    rankdir="LR",
    fontname="Helvetica",
    fontsize="13",
    bgcolor="#F7F9FC",
    labelloc="t",
    label="Domain Name System (DNS) – High Level Design (HLD)"
)

dot.attr("node", style="filled", fontname="Helvetica", fontsize="11")
dot.attr("edge", fontname="Helvetica", fontsize="10", color="#555555")

# =========================
# CLIENT & EDGE LAYER
# =========================
with dot.subgraph(name="cluster_client") as c:
    c.attr(label="Client Layer", style="rounded", color="#90CAF9")
    c.node("Client", "Client\n(Browser / OS Resolver)", shape="oval", fillcolor="#E3F2FD")

# =========================
# ENTRY & DISTRIBUTION
# =========================
with dot.subgraph(name="cluster_entry") as c:
    c.attr(label="DNS Entry & Traffic Distribution", style="rounded", color="#81D4FA")
    c.node("Anycast", "Anycast Routing", fillcolor="#E1F5FE")
    c.node("LB", "DNS Load Balancer", shape="circle", fillcolor="#B3E5FC")

# =========================
# RESOLVER LAYER
# =========================
with dot.subgraph(name="cluster_resolver") as c:
    c.attr(label="Recursive Resolver Layer", style="rounded", color="#A5D6A7")
    c.node("Resolver", "Recursive DNS Resolver\n(Stateless Instances)", fillcolor="#E8F5E9")
    c.node("Cache", "DNS Cache\n(TTL-based)", shape="box", fillcolor="#DCEDC8")

# =========================
# DNS HIERARCHY
# =========================
with dot.subgraph(name="cluster_hierarchy") as c:
    c.attr(label="DNS Hierarchy", style="rounded", color="#FFCC80")
    c.node("Root", "Root Name Servers", fillcolor="#FFF3E0")
    c.node("TLD", "TLD Name Servers", fillcolor="#FFE0B2")
    c.node("Auth", "Authoritative Name Servers", fillcolor="#FFD180")

# =========================
# DATA & MANAGEMENT
# =========================
with dot.subgraph(name="cluster_data") as c:
    c.attr(label="Zone Data & Control Plane", style="rounded", color="#FFF59D")
    c.node("ZoneDB", "Zone File Storage", shape="cylinder", fillcolor="#FFFDE7")
    c.node("API", "DNS Management API", fillcolor="#FFF9C4")

# =========================
# OBSERVABILITY & SECURITY
# =========================
with dot.subgraph(name="cluster_obs") as c:
    c.attr(label="Security & Observability", style="rounded", color="#CE93D8")
    c.node("DNSSEC", "DNSSEC Validation", fillcolor="#F3E5F5")
    c.node("Monitor", "Monitoring & Logging", fillcolor="#EDE7F6")

# =========================
# HORIZONTAL QUERY FLOW
# =========================
dot.edge("Client", "Anycast", label="DNS Query")
dot.edge("Anycast", "LB")
dot.edge("LB", "Resolver")

dot.edge("Resolver", "Cache", label="Lookup")
dot.edge("Cache", "Resolver", label="Hit")

dot.edge("Resolver", "Root", label="Cache Miss")
dot.edge("Root", "TLD")
dot.edge("TLD", "Auth")

dot.edge("Auth", "Resolver", label="DNS Answer")

# =========================
# VERTICAL DATA & CONTROL FLOWS
# =========================
dot.edge("Auth", "ZoneDB", style="dashed")
dot.edge("API", "ZoneDB", label="Manage Zones", style="dashed")

dot.edge("Resolver", "DNSSEC", label="Validate")
dot.edge("DNSSEC", "Resolver")

dot.edge("Resolver", "Monitor")
dot.edge("Auth", "Monitor")
dot.edge("LB", "Monitor")

# =========================
# RENDER
# =========================
dot