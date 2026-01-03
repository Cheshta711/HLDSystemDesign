# DNS System - Detailed LLD
# Run in Google Colab

!pip install -q graphviz

from graphviz import Digraph

dot = Digraph("DNS_LLD", format="png")

# =========================
# GLOBAL STYLE
# =========================
dot.attr(
    rankdir="LR",
    bgcolor="#FAFAFA",
    fontname="Helvetica",
    labelloc="t",
    label="Domain Name System (DNS) – Low Level Design (LLD)"
)

dot.attr("node", style="filled,rounded", fontname="Helvetica", fontsize="10")
dot.attr("edge", fontname="Helvetica", fontsize="9", color="#424242")

# =========================
# CLIENT SIDE
# =========================
with dot.subgraph(name="cluster_client") as c:
    c.attr(label="Client Resolver", color="#90CAF9")
    c.node("Stub", "Stub Resolver\n(OS / Browser)", fillcolor="#E3F2FD")

# =========================
# ENTRY LAYER
# =========================
with dot.subgraph(name="cluster_entry") as c:
    c.attr(label="Traffic Entry", color="#81D4FA")
    c.node("Anycast", "Anycast Router", fillcolor="#E1F5FE")
    c.node("LB", "DNS Load Balancer", fillcolor="#B3E5FC")

# =========================
# RECURSIVE RESOLVER (CORE)
# =========================
with dot.subgraph(name="cluster_resolver") as c:
    c.attr(label="Recursive Resolver (Internal Modules)", color="#A5D6A7")

    c.node("QueryParser", "Query Parser", fillcolor="#E8F5E9")
    c.node("Policy", "Policy Engine\n(Rate Limit, ACL)", fillcolor="#DCEDC8")
    c.node("CacheMgr", "Cache Manager", fillcolor="#C5E1A5")
    c.node("TTL", "TTL Handler", fillcolor="#AED581")
    c.node("Recursor", "Iterative Resolver\n(State Machine)", fillcolor="#9CCC65")
    c.node("ResponseBuilder", "Response Builder", fillcolor="#DCE775")

# =========================
# CACHE STRUCTURE
# =========================
with dot.subgraph(name="cluster_cache") as c:
    c.attr(label="Cache Storage", color="#FFF59D")
    c.node("RRCache", "Resource Record Cache", shape="cylinder", fillcolor="#FFFDE7")
    c.node("Evict", "LRU / LFU Eviction", fillcolor="#FFF9C4")

# =========================
# DNS HIERARCHY
# =========================
with dot.subgraph(name="cluster_dns") as c:
    c.attr(label="DNS Hierarchy", color="#FFCC80")
    c.node("Root", "Root Server", fillcolor="#FFF3E0")
    c.node("TLD", "TLD Server", fillcolor="#FFE0B2")
    c.node("Auth", "Authoritative Server", fillcolor="#FFD180")

# =========================
# SECURITY & OBSERVABILITY
# =========================
with dot.subgraph(name="cluster_security") as c:
    c.attr(label="Security & Observability", color="#CE93D8")
    c.node("DNSSEC", "DNSSEC Validator", fillcolor="#F3E5F5")
    c.node("Logger", "Query Logger", fillcolor="#EDE7F6")
    c.node("Metrics", "Metrics Collector", fillcolor="#E1BEE7")

# =========================
# HORIZONTAL FLOW
# =========================
dot.edge("Stub", "Anycast", label="DNS Query")
dot.edge("Anycast", "LB")
dot.edge("LB", "QueryParser")

dot.edge("QueryParser", "Policy")
dot.edge("Policy", "CacheMgr")

dot.edge("CacheMgr", "RRCache", label="Read")
dot.edge("RRCache", "CacheMgr", label="Hit")

dot.edge("CacheMgr", "Recursor", label="Miss")
dot.edge("Recursor", "Root")
dot.edge("Root", "TLD")
dot.edge("TLD", "Auth")

dot.edge("Auth", "Recursor")
dot.edge("Recursor", "TTL")
dot.edge("TTL", "CacheMgr")

dot.edge("CacheMgr", "ResponseBuilder")
dot.edge("ResponseBuilder", "Stub", label="DNS Response")

# =========================
# VERTICAL INTERNAL FLOWS
# =========================
dot.edge("CacheMgr", "Evict", style="dashed")
dot.edge("Recursor", "DNSSEC", label="Validate", style="dashed")

dot.edge("QueryParser", "Logger", style="dashed")
dot.edge("Recursor", "Metrics", style="dashed")
dot.edge("LB", "Metrics", style="dashed")

# =========================
# RENDER
# =========================
dot 
