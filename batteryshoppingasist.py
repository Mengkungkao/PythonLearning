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
