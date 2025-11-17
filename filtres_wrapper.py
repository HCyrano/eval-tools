import subprocess

# Exécution
for i in range(9, 60):
	command = ["python3", "filtre_100.py", str(i)]
	result = subprocess.run(command)

