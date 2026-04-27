import concurrent.futures
import subprocess
import os


def run_script():
    script_path = os.path.join(
        os.path.dirname(__file__), "ddos_attack.py"
    )  # Automatisch pad bepalen
    subprocess.run(["python", script_path], input="ja\n", text=True)


if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(max_workers=40) as executor:
        futures = [executor.submit(run_script) for _ in range(40)]

        # Wacht tot alle taken zijn voltooid
        concurrent.futures.wait(futures)
