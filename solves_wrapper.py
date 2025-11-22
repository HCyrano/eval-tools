import subprocess

# Exécution
for i in range(9):
	command = ["python3", "solve.py", str(i)]
	result = subprocess.run(command)


