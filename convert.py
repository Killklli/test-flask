# For each py file in this directory and all subdirectories, this script will run a subprocess call to mypyc
import glob
import subprocess
from multiprocessing import Pool

def process_file(file):
    try:
        subprocess.call(["mypyc", file])
    except Exception:
        pass

if __name__ == '__main__':
    pool = Pool()                         # Create a multiprocessing Pool
    pool.map(process_file, glob.glob("randomizer/**/*.py", recursive=True))  
    pool.close()                          # Close the pool and wait for the work to finish
    pool.join()                           # Combine the results of the workers