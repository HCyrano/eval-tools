import subprocess

# Exécution
for i in range(60):
	command = ["python3", "solve.py", str(i)]
	result = subprocess.run(command)


