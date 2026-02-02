import subprocess

# Exécution
for i in range(9, 60):
        #n_occs_min = max(10, min(50, 60 - i))
        n_occs_min = 50
        command = ["python3", "./scripts_python/norm_data.py", str(i), str(n_occs_min)]
        result = subprocess.run(command)

