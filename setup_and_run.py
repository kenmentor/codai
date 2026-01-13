import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    try:
        import flask
    except ImportError:
        print("Flask is not installed. Installing now...")
        install_package('Flask')
    
    print("Dependencies are satisfied.")
    
    # Running the Flask application
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    main()
