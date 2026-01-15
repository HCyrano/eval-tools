import subprocess

# Exécution
for i in range(0, 60):
	command = ["python3", "./scripts python/solve.py", str(i)]
	result = subprocess.run(command)


