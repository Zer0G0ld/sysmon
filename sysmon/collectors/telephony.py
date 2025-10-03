from ..utils import run_json

def read():
    j = run_json(["termux-telephony-status"])
    return {
        "sim_state": j.get("simState"),
        "network": j.get("networkOperatorName")
    }

