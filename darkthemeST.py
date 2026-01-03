!pip install -q graphviz

from graphviz import Digraph

dot = Digraph(
    name="Stranger_Things_Advanced_LLD",
    format="png"
)

# ===============================
# GLOBAL STYLES
# ===============================
dot.attr(
    rankdir="TB",
    fontsize="10",
    bgcolor="black",
    fontcolor="white"
)

dot.attr(
    "node",
    fontcolor="white"
)

dot.attr(
    "edge",
    color="lightgray",
    fontcolor="white",
    penwidth="2",
    arrowsize="1.2"
)

# =================================================
# WORLDS
# =================================================
with dot.subgraph(name="cluster_worlds") as c:
    c.attr(label="World Layer", color="red", fontcolor="red")

    c.node("Hawkins", "Hawkins (Normal World)", shape="box", style="filled", fillcolor="#1a1a1a")
    c.node("UpsideDown", "Upside Down (Parallel World)", shape="box", style="filled", fillcolor="#2b0000")

# =================================================
# GOVERNMENT & LAB
# =================================================
with dot.subgraph(name="cluster_lab") as c:
    c.attr(label="Government & Control Systems", color="purple", fontcolor="purple")

    c.node("HawkinsLab", "Hawkins Lab\n(Experiment Engine)", shape="box", style="filled", fillcolor="#2a002a")
    c.node("DrBrenner", "Dr. Brenner\n(System Architect)", shape="oval", style="filled", fillcolor="#330033")
    c.node("Agents", "Government Agents\n(Suppression Units)", shape="box", style="filled", fillcolor="#220022")

# =================================================
# SUPERNATURAL THREATS
# =================================================
with dot.subgraph(name="cluster_threats") as c:
    c.attr(label="Threat System", color="orange", fontcolor="orange")

    c.node("MindFlayer", "Mind Flayer\n(Control Layer)", shape="box", style="filled", fillcolor="#402200")
    c.node("Vecna", "Vecna\n(Command Executor)", shape="box", style="filled", fillcolor="#402200")
    c.node("Demogorgon", "Demogorgon\n(Attack Node)", shape="box", style="filled", fillcolor="#402200")

# =================================================
# KIDS
# =================================================
with dot.subgraph(name="cluster_kids") as c:
    c.attr(label="Kids (Decision Cluster)", color="cyan", fontcolor="cyan")

    c.node("Eleven", "Eleven\n(Psychic Interface)", shape="oval", style="filled", fillcolor="#003333")
    c.node("Mike", "Mike\n(Leader)", shape="oval", style="filled", fillcolor="#003333")
    c.node("Dustin", "Dustin\n(Logic)", shape="oval", style="filled", fillcolor="#003333")
    c.node("Lucas", "Lucas\n(Defense)", shape="oval", style="filled", fillcolor="#003333")
    c.node("Will", "Will\n(Signal Receiver)", shape="oval", style="filled", fillcolor="#003333")
    c.node("Max", "Max\n(Risk Target)", shape="oval", style="filled", fillcolor="#003333")

# =================================================
# ADULTS
# =================================================
with dot.subgraph(name="cluster_adults") as c:
    c.attr(label="Adult Layer", color="green", fontcolor="green")

    c.node("Hopper", "Hopper\n(Enforcement)", shape="oval", style="filled", fillcolor="#003300")
    c.node("Joyce", "Joyce\n(Decoder)", shape="oval", style="filled", fillcolor="#003300")
    c.node("Murray", "Murray\n(Analyst)", shape="oval", style="filled", fillcolor="#003300")

# =================================================
# COMMUNICATION
# =================================================
with dot.subgraph(name="cluster_comm") as c:
    c.attr(label="Communication", color="white", fontcolor="white")

    c.node("Radio", "Walkie-Talkies", shape="diamond", style="filled", fillcolor="#333333")
    c.node("Lights", "Lights / Signals", shape="diamond", style="filled", fillcolor="#333333")
    c.node("Music", "Music (Interrupt)", shape="diamond", style="filled", fillcolor="#333333")

# =================================================
# RELATIONSHIPS (VISIBLE ARROWS)
# =================================================
dot.edge("HawkinsLab", "Eleven", label="Experiments")
dot.edge("HawkinsLab", "UpsideDown", label="Portal Creation")
dot.edge("UpsideDown", "MindFlayer", label="Hosts")
dot.edge("MindFlayer", "Vecna", label="Commands")
dot.edge("Vecna", "Demogorgon", label="Controls")
dot.edge("Demogorgon", "Hawkins", label="Attacks")

dot.edge("Eleven", "UpsideDown", label="Psychic Access")
dot.edge("Eleven", "Mike", label="Trust")
dot.edge("Will", "UpsideDown", label="Linked")
dot.edge("Will", "Lights", label="Signals")

dot.edge("Lights", "Joyce", label="Decoded By")
dot.edge("Joyce", "Hopper", label="Alerts")

dot.edge("Radio", "Kids", label="Coordination")
dot.edge("Kids", "Radio")
dot.edge("Music", "Max", label="Protection")
dot.edge("Vecna", "Max", label="Targets")

dot.edge("Hopper", "Agents", label="Conflict")
dot.edge("Agents", "HawkinsLab", label="Cover-up")

# Render
dot