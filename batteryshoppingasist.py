import csv
import os
from dataclasses import dataclass, asdict
FILE_NAME = "battery_data.csv"
@dataclass
class Battery:
    name: str
    capacity: float
    voltage: float
    discharge: float
    charge: float
    safety: float
    def energy(self) -> float:
        return self.capacity* self.voltage
def load_batteries(filename = FILE_NAME):
    batteries=[]
    if not os.path.exists(filename):
        return batteries
    with open(filename,mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try: 
                battery = Battery(
                    name = row["name"], #name need to be the same as class variable otherwise unreadable
                    capacity= float(row["capacity"]),
                    voltage= float(row["voltage"]),
                    discharge =float(row["discharge"]),
                    charge = float(row["charge"]),
                    safety = float(row["safety"]),
                )
                batteries.append(battery)
            except(ValueError, KeyError):
                print(f"Skipped invalid row: {row}")
        return batteries

def add_battery():
    print("\nEnter batteries information")
    name = input("Model name: ")
    capacity = float(input("Capacity[Ah] "))
    voltage = float(input("Norminal Voltage[V]"))
    discharge= float(input("Maximum Discharge Current{C}"))
    charge =float(input("Maximum Charge Current[C]"))
    safety = float(input("Safety Factor Rating 1 to 10 "))
    return Battery(name,capacity,voltage,discharge,charge,safety)
def show_batteries(batteries):
    if not batteries:
        print("\nNot yet input any battery")
        return
    print("\nBatteries models:")
    print("--------------------------------------------------------------------------------------------------")
    print(
        f"{'No.':<5}{'Name':<20}{'Capacity(mAh)':<15}{'Voltage(V)':<12}"
        f"{'Discharge(A)':<15}{'Charge(A)':<12}{'Energy(Wh)':<12}{'Safety':<10}"
    )
    print("--------------------------------------------------------------------------------------------------")
    for i,b in enumerate(batteries,start=1):
        print(
            f"{i:<5}{b.name:<20}{b.capacity:<15.1f}{b.voltage:<12.2f}"
            f"{b.discharge:<15.2f}{b.charge:<12.2f}{b.energy():<12.2f}{b.safety:<10}"
        )

def main():
batteries = load_batteries()
while True:
    print("\nBattery Comparison System")
    print("1. Add new battery")
    print("2. Show all batteries")
    print("3. Compare two batteries")
    print("4. Show best battery by safety")
    print("5. Edit")
    print("6. Save")
    print("7. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        try:
            battery = add_battery()
            batteries.append(battery)
            print("Battery added successfully.")
        except ValueError:
            print("Invalid input. Please enter correct numeric values.")

    elif choice == "2":
        show_batteries(batteries)

    elif choice == "3":
        compare_batteries(batteries)

    elif choice == "4":
        best_by_safety(batteries)

    elif choice == "5":
        save_batteries(batteries)
        print(f"Data saved to '{FILE_NAME}'. Goodbye.")
    elif choice == "6":
        save_batteries(batteries)
        print(f"Data saved to '{FILE_NAME}' successfully.")
    elif choice == "7":
        break  
    else:
        print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
