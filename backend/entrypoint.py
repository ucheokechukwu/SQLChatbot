import subprocess
launch_command = "uvicorn backend.main:app --host 0.0.0.0 --port 8001"
process = subprocess.Popen(launch_command.split(), stdout=subprocess.PIPE)
