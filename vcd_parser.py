from vcdvcd import VCDVCD
import os

# ---- CONFIG ----
vcd_file = "sample_axi.vcd"   # Replace with your actual VCD filename
watch_signals = ["AWVALID", "AWREADY", "BVALID", "ARVALID", "ARREADY", "RVALID"]

# ---- PARSE VCD ----
def parse_vcd(file_path, signals):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None

    vcd = VCDVCD(file_path, signals=signals, store_tvs=True)
    signal_data = {}

    for signal in signals:
        for full_signal in vcd.data:
            if signal in full_signal:
                signal_data[signal] = vcd[full_signal]['tv']
                break

    return signal_data

# ---- RULE CHECKING ----
def check_rule_r1(signal_data):
    print("\n🔍 Rule R1: Write issued (AWVALID & AWREADY) but no BVALID\n")
    write_issued = []
    bvalid_times = {t for t, v in signal_data.get("BVALID", []) if v == '1'}

    for t, val in signal_data.get("AWVALID", []):
        if val == '1':
            # Check if AWREADY also 1 at same time
            awready_at_t = next((v for ts, v in signal_data.get("AWREADY", []) if ts == t), None)
            if awready_at_t == '1':
                if not any(bt > t and bt < t + 500 for bt in bvalid_times):
                    print(f"❗ No BVALID after AWVALID+AWREADY at time {t}ns")

def check_rule_r2(signal_data):
    print("\n🔍 Rule R2: ARVALID held high but ARREADY low (read stall)\n")
    last_valid_time = None
    stall_start = None

    for t, val in signal_data.get("ARVALID", []):
        if val == '1':
            arready_at_t = next((v for ts, v in signal_data.get("ARREADY", []) if ts == t), None)
            if arready_at_t == '0':
                if stall_start is None:
                    stall_start = t
            else:
                if stall_start is not None and (t - stall_start > 100):
                    print(f"❗ Read stall detected from {stall_start}ns to {t}ns")
                stall_start = None

# ---- MAIN ----
if __name__ == "__main__":
    signals = parse_vcd(vcd_file, watch_signals)
    if signals:
        check_rule_r1(signals)
        check_rule_r2(signals)
