import subprocess

# Exécution
for i in range(0, 9):
	command = ["python3", "./scripts python/norm_data.py", str(i)]
	result = subprocess.run(command)

