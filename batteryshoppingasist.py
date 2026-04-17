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

def save_batteries(batteries, filename=FILE_NAME):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "name",
            "capacity",
            "voltage",
            "discharge",
            "charge",
            "safety",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for battery in batteries:
            writer.writerow(asdict(battery))



def compare_batteries(batteries):
    if len(batteries) < 2:
        print("\nNeed at least 2 batteries to compare.")
        return

    show_batteries(batteries)

    try:
        first = int(input("\nEnter first battery number to compare: ")) - 1
        second = int(input("Enter second battery number to compare: ")) - 1

        if first < 0 or second < 0 or first >= len(batteries) or second >= len(batteries):
            print("Invalid selection.")
            return

        b1 = batteries[first]
        b2 = batteries[second]

        print("\nBattery Comparison")
        print("-" * 60)
        print(f"{'Property':<20}{b1.name:<18}{b2.name:<18}")
        print("-" * 60)
        print(f"{'Capacity (mAh)':<20}{b1.capacity:<18.1f}{b2.capacity:<18.1f}")
        print(f"{'Nominal V':<20}{b1.voltage:<18.2f}{b2.voltage:<18.2f}")
        print(f"{'Discharge A':<20}{b1.discharge:<18.2f}{b2.discharge:<18.2f}")
        print(f"{'Charge A':<20}{b1.charge:<18.2f}{b2.charge:<18.2f}")
        print(f"{'Safety':<20}{b1.safety:<18}{b2.safety:<18}")
        print(f"{'Energy (Wh)':<20}{b1.energy():<18.2f}{b2.energy():<18.2f}")

    except ValueError:
        print("Please enter valid numbers.")
def best_by_safety(batteries):
    if not batteries:
        print("\nNo battery data found.")
        return

    best = max(batteries, key=lambda b: b.safety)
    print("\nBest Battery by Safety:")
    print(
        f"{best.name} | Safety: {best.safety} | "
        f"Capacity: {best.capacity} mAh | Voltage: {best.voltage} V"
    )

def edit_battery(batteries):
    if not batteries:
        print("\nNo battery data found.")
        return

    show_batteries(batteries)

    try:
        index = int(input("\nEnter battery number to edit: ")) - 1

        if index < 0 or index >= len(batteries):
            print("Invalid battery number.")
            return

        battery = batteries[index]

        print("\nPress Enter to keep old value.")

        new_name = input(f"Battery name [{battery.name}]: ").strip()
        new_capacity = input(f"Capacity (mAh) [{battery.capacity}]: ").strip()
        new_voltage = input(f"Nominal voltage (V) [{battery.voltage}]: ").strip()
        new_discharge = input(f"Discharge current (A) [{battery.discharge}]: ").strip()
        new_charge = input(f"Charge current (A) [{battery.charge}]: ").strip()
        new_safety = input(f"Safety rating (1 to 10) [{battery.safety}]: ").strip()

        if new_name:
            battery.name = new_name
        if new_capacity:
            battery.capacity = float(new_capacity)
        if new_voltage:
            battery.voltage = float(new_voltage)
        if new_discharge:
            battery.discharge = float(new_discharge)
        if new_charge:
            battery.charge = float(new_charge)
        if new_safety:
            battery.safety_1_to_10 = float(new_safety)

        print("Battery updated successfully.")

    except ValueError:
        print("Invalid input. Please enter correct numeric values.")




def main():
    batteries = load_batteries()
    while True:
        print("\nBattery Comparison System")
        print("1. Add new battery")
        print("2. Show all batteries")
        print("3. Compare two batteries")
        print("4. Show best battery by safety")
        print("5. Save data")
        print("6. Reload saved battery data")
        print("7. Edit one battery")
        print("8. Exit")
    
        choice = input("Choose an option: ").strip()
    
        if choice == "1":
            try:
                battery_obj = add_battery()
                batteries.append(battery_obj)
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
            print(f"Data saved to '{FILE_NAME}'.")

        elif choice == "6":
            confirm = input("Reload from file? Unsaved changes will be lost. (y/n): ").strip().lower()
            if confirm == "y":
                batteries = load_batteries()
                print(f"Reloaded {len(batteries)} battery record(s) from {FILE_NAME}.")
            else:
                print("Reload cancelled.")

        elif choice == "7":
            edit_battery(batteries)

        elif choice == "8":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
