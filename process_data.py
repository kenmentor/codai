# Script to loop through data in data.py file

def main():
    try:
        from data import data
        if not isinstance(data, list):
            raise ValueError("Data should be a list.")

        for item in data:
            print(item)

    except ImportError:
        print("The data.py file or the 'data' variable was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()