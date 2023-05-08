#B453camp369.py
# Copyright (c) 2023 C15N32™
# This code is licensed under the 6o Function Yourself (6FY) License, or
# MIT License, WTFPL License, or GFYS License, if 6FY is not recognized.
# Please refer to the LICENSE file in the project root for the full text.
# 
# pip install -r requirements.txt
import os
import sys
import asyncio
from typing import List
import yaml
import openai
import runpy

# Import bot constructor class(es) here
from B07_B17 import B17
#  (e.g. B17 is the Discord bit of the bot's abilities)
from B17_D474 import D474FL45H

def merge_yaml_files(file_paths):
    merged_data = {}
    for file_path in file_paths:
        with open(file_path, "r", encoding='utf-8') as f:
            data = yaml.safe_load(f)
            for key, value in data.items():
                if key not in merged_data:
                    merged_data[key] = value
                else:
                    if value is None:  # If the value is None, do nothing.
                        pass
                    elif isinstance(value, list):
                        if merged_data[key] is None:
                            merged_data[key] = value
                        else:
                            merged_data[key] += value
                    elif isinstance(value, dict):
                        if merged_data[key] is None:
                            merged_data[key] = value
                        else:
                            merged_data[key].update(value)
                    else:  # If the value is not None, list, or dict, replace the existing value.
                        merged_data[key] = value
    return merged_data

class Signal369:    # Bot Manager
    def __init__(self):
        self.bots = {}  # Stores bot instances
        self.bot_tasks = {}  # Stores asyncio tasks for each bot

        # Load tokens from the ___tokens___.yaml file
        with open("___tokens___.yaml", "r") as f:
            self.tokens = yaml.safe_load(f)

    def get_available_bots(self) -> List[str]:
        yaml_files = [f for f in os.listdir() if f.startswith("_init_") and f.endswith(".yaml")]
        bot_names = [os.path.splitext(f)[0][6:] for f in yaml_files]

        with open("___tokens___.yaml", "r") as f:
            tokens_data = yaml.safe_load(f)

        available_bots = [bot_name for bot_name in bot_names if f"{bot_name}_discord" in tokens_data]

        return available_bots

    async def start_bot(self, bot_name: str):
        # Retrieve bot configuration and token
        config_files = ["_init__global.yaml", f"_init_{bot_name}.yaml"]
        merged_config = merge_yaml_files(config_files)
        bot_init_data = merged_config
        try:
            discord_token = self.tokens[f"{bot_name}_discord"]
        except KeyError as e:
            return f"Error: Unable to find the token for {bot_name}. Please check the ___tokens___.yaml file."
        except AttributeError as e:
            return f"Error: 'Signal369' object has no attribute 'tokens'. Please check the class definition."
        finally:
            print(f"Attempting to retrieve token for {bot_name}.")

        # Create and store the bot instance
        bot = B17(openai.api_key, discord_token, bot_init_data)
        self.bots[bot_name] = bot

        # Start the bot as an asyncio task
        try:
            task = asyncio.create_task(bot.start(discord_token))
            self.bot_tasks[bot_name] = task
        except Exception as e:
            return f"Error starting bot {bot_name}: {e}"

    async def stop_bot(self, bot_name: str):
        bot = self.bots[bot_name]
        await bot.close()
        del self.bots[bot_name]
        del self.bot_tasks[bot_name]

    async def restart_bot(self, bot_name: str):
        await self.stop_bot(bot_name)
        await self.start_bot(bot_name)
    
    async def wait_for_bots(self):
        tasks = list(self.bot_tasks.values())
        if tasks:
            await asyncio.gather(*tasks)

    def get_running_bots(self) -> List[str]:
        return list(self.bots.keys())

    def configure_bot(self, bot_name: str):
        # Implement your bot configuration logic here
        pass

    def configure_rpc_portmap(self):
        # Implement your RPC portmap configuration logic here
        pass

async def service_bot(bot_manager: Signal369, flash_data: D474FL45H):
    while True:
        print("\nService Menu")
        print("1. Start a bot")
        print("2. Shutdown a bot")
        print("3. Restart a bot")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                bot_name = display_available_bots(bot_manager)
                flash_message = await bot_manager.start_bot(bot_name)
                if flash_message:
                    flash_data.set(flash_message)

            elif choice == "2":
                if not bot_manager.bots:
                    flash_data.set("No bots are currently running.")
                    break

                print("\nRunning bots:")
                for i, bot_name in enumerate(bot_manager.bots.keys(), start=1):
                    print(f"{i}. {bot_name}")

                bot_choice = int(input("Enter the number of the bot you want to stop: "))
                bot_name = list(bot_manager.bots.keys())[bot_choice - 1]
                await bot_manager.stop_bot(bot_name)

            elif choice == "3":
                if not bot_manager.bots:
                    flash_data.set("No bots are currently running.")
                    break

                print("\nRunning bots:")
                for i, bot_name in enumerate(bot_manager.bots.keys(), start=1):
                    print(f"{i}. {bot_name}")

                bot_choice = int(input("Enter the number of the bot you want to restart: "))
                bot_name = list(bot_manager.bots.keys())[bot_choice - 1]
                await bot_manager.restart_bot(bot_name)

            elif choice == "4":
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            flash_data.set(str(e))

async def connect_bot(bot_manager: Signal369, flash_data: D474FL45H):
    while True:
        print("\nConnect Bot Menu")
        print("1. Discord")
        print("2. Telegram")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                # Import and use the constructor class for Discord
                from B17_D15C0RD import D15C0RD
                # Add the logic to connect the Discord bot here
                break
            elif choice == "2":
                # Import and use the constructor class for Telegram
                from B17_73L36R4M import T3L36R4M
                # Add the logic to connect the Telegram bot here
                break
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            flash_data.set(str(e))

def display_available_bots(bot_manager):
    available_bots = bot_manager.get_available_bots()
    print("\nAvailable bots:")
    for i, bot_name in enumerate(available_bots, start=1):
        print(f"{i}. {bot_name}")

    bot_choice = int(input("Enter the number of the bot: "))
    bot_name = available_bots[bot_choice - 1]
    return bot_name

async def main():
    bot_manager = Signal369()
    flash_data = D474FL45H()

    async def tools_menu():
        while True:
            print("\nTools - Pirate Menu")
            print("1. Horse Stable")
            print("2. Flash World")
            print("3. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                print("Running Horse Stable...")
                runpy.run_path("pirate_horse_stable.py")
                flash_data.set("Horse Stable script completed.")
                break
            elif choice == "2":
                flash_data.set("Hello World")
                break
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        flash_message = flash_data.get_and_reset()

        print("\nBot Troop 369 - Main Menu")
        print("1. Configure a bot")
        print("2. Service a bot")
        print("3. Display running bots")
        print("4. Connect a bot")
        print("5. Configure Globals (e.g. RPC Portmap for all bots)")
        print("7. Tools")
        print("9. Exit")

        if flash_message:
            print("Message: " + flash_message)

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                bot_name = display_available_bots(bot_manager)
                bot_manager.configure_bot(bot_name)

            elif choice == "2":
                await service_bot(bot_manager, flash_data)

            elif choice == "3":
                running_bots = bot_manager.get_running_bots()
                if running_bots:
                    print("\nRunning bots:")
                    for i, bot_name in enumerate(running_bots, start=1):
                        print(f"{i}. {bot_name}")
                    input("Press any key to return to the main menu...")
                else:
                    flash_data.set("No bots are currently running.")
 
            elif choice == "4":
                await connect_bot(bot_manager, flash_data)

            elif choice == "5":
                bot_manager.configure_rpc_portmap()

            elif choice == "6":
                pass

            elif choice == "7":
                await tools_menu()

            elif choice == "8":
                pass

            elif choice == "9":
                sys.exit()

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            flash_data = str(e)

if __name__ == "__main__":
    asyncio.run(main())
