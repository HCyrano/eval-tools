import subprocess

# Exécution
for i in range(9, 60):
	command = ["python3", "norm_data.py", str(i)]
	result = subprocess.run(command)

