#8453camp369.py
# Copyright (c) 2023 C15N32™
# This code is licensed under the 6o Function Yourself (6FY) License, or
# MIT License, WTFPL License, or GFYS License, if 6FY is not recognized.
# Please refer to the LICENSE file in the project root for the full text.
# 
# pip install -r requirements.txt
#
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

# Constants for `Wake Up` game.
ZIP = "219"
ZAP = "249"
ZOP = "209"

def merge_yaml_files(file_paths):
    merged_data = {}
    for file_path in file_paths:
        with open(file_path, "r", encoding='utf-8') as f:
            data = yaml.safe_load(f)
            for key, value in data.items():
                if value is None:  # If the value is None, do nothing.
                    pass
                elif isinstance(value, list):
                    if key not in merged_data or merged_data[key] is None:
                        merged_data[key] = value
                    else:
                        merged_data[key] += value
                elif isinstance(value, dict):
                    if key not in merged_data or merged_data[key] is None:
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
        self.load_keys()
        self.load_tokens()

    def load_keys(self):
        # Load keys from the ___keys___.yaml file
        with open("___keys___.yaml", "r") as f:
            self.keys = yaml.safe_load(f)

    def load_tokens(self):
        # Load tokens from the ___tokens___.yaml file
        with open("___tokens___.yaml", "r") as f:
            self.tokens = yaml.safe_load(f)
        
    def get_available_bots(self) -> List[str]:
        yaml_files = [f for f in os.listdir() if f.startswith("_init_") and f.endswith(".yaml")]
        bot_names = [os.path.splitext(f)[0][6:] for f in yaml_files]

        with open("___tokens___.yaml", "r") as f:
            tokens_data = yaml.safe_load(f)

        available_bots = [bot_name for bot_name in bot_names if f"{bot_name}_discord_token" in tokens_data]

        return available_bots

    async def start_bot(self, bot_name: str, flash_data: D474FL45H):
        # Retrieve bot configuration and token
        #config_files = ["_init_{bot_name}.yaml", "_init__global.yaml"]
        #{To ensure the bot's custom values overwrite the globals, 
        # you would want to reverse the order of these config files like this: 
        # config_files = ["_init__global.yaml", "_init_{bot_name}.yaml"]}.
        config_files = ["_init__global.yaml", f"_init_{bot_name}.yaml"]
        merged_config = merge_yaml_files(config_files)
        bot_init_data = merged_config

        try:
            discord_token = self.tokens[f"{bot_name}_discord_token"]
        except KeyError as e:
            flash_data.set(f"Error: Unable to find the token for {bot_name}. Please check the ___tokens___.yaml file. {str(e)}")
            return f"Error: Unable to find the token for {bot_name}. Please check the ___tokens___.yaml file."
        except AttributeError as e:
            flash_data.set(f"Error: 'Signal369' object has no attribute 'tokens'. Please check the class definition. {str(e)}")
            return f"Error: 'Signal369' object has no attribute 'tokens'. Please check the class definition."
        finally:
            print(f"Attempting to retrieve token for {bot_name}.")

        try:
            openai_key = self.keys["openai_api_key"]
        except KeyError as e:
            flash_data.set(f"Error: Unable to find the token for {bot_name}. Please check the ___tokens___.yaml file. {str(e)}")
            return f"Error: Unable to find the OpenAI key. Please check the ___keys__.yaml file."

        # Fetch the Telegram api_id and api_hash
        try:
            telegram_api_id = bot_init_data["telegram_api_id"]
            telegram_api_hash = self.keys[f"{bot_name}_telegram_api_hash"]
        except KeyError as e:
            flash_data.set(f"Error: Unable to find the Telegram api_id or api_hash. Please check the bot's configuration and the ___keys__.yaml files. {str(e)}")
            return f"Error: Unable to find the Telegram api_id or api_hash. Please check the bot's configuration and the ___keys__.yaml files."

        # Create and store the bot instance
        bot = B17(openai_key, discord_token, telegram_api_id, telegram_api_hash, bot_init_data)
        self.bots[bot_name] = bot

        # Start the bot as an asyncio task
        try:
            task = asyncio.create_task(bot.start(discord_token))
            self.bot_tasks[bot_name] = task
            flash_data.set(f'{bot_name} started successfully')
        except Exception as e:
            flash_data.set(f"Error starting bot {bot_name}: {str(e)}")
            return f"Error starting bot {bot_name}: {str(e)}"

    async def stop_bot(self, bot_name: str):
        bot = self.bots[bot_name]
        await bot.close()
        del self.bots[bot_name]
        del self.bot_tasks[bot_name]

    async def restart_bot(self, bot_name: str, flash_data: D474FL45H):
        await self.stop_bot(bot_name)
        await self.start_bot(bot_name, flash_data)
    
    async def wait_for_bots(self):
        tasks = list(self.bot_tasks.values())
        if tasks:
            await asyncio.gather(*tasks)
    
    async def send_message(self, bot_name: str, message: str):
        bot = self.bots.get(bot_name)
        if bot is None:
            print(f"Bot {bot_name} is not running.")
            return
        try:
            await bot.send_message(message)
        except Exception as e:
            print(f"Error sending message with bot {bot_name}: {str(e)}")


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

        current_flash_data = flash_data.get_and_reset()
        if current_flash_data:
            print(f"\n{current_flash_data}")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                bot_name = display_available_bots(bot_manager, flash_data)
                if bot_name is None:
                    flash_data.set("No available bots.")
                    continue
                flash_message = await bot_manager.start_bot(bot_name, flash_data)
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
                await bot_manager.restart_bot(bot_name, flash_data)

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

        flash_message = flash_data.get_and_reset()
        if flash_message:
            print("Message: " + flash_message)

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                # Import and use the constructor class for Discord
                from B17_D15C0RD import D15C0RD
                # Add the logic to connect the Discord bot here
                break
            elif choice == "2":
                # Import and use the constructor class for Telegram
                from B17_T3L36R4M import T3L36R4M
                # Add the logic to connect the Telegram bot here
                break
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            flash_data.set(str(e))

def display_available_bots(bot_manager, flash_data: D474FL45H):
    available_bots = bot_manager.get_available_bots()
    if not available_bots:
        print("No available bots.")
        flash_data.set("No available bots.")
        return None
    print("\nAvailable bots:")
    for i, bot_name in enumerate(available_bots, start=1):
        print(f"{i}. {bot_name}")

    bot_choice = -1
    while bot_choice < 1 or bot_choice > len(available_bots):
        try:
            bot_choice = int(input("Enter the number of the bot: "))
            if bot_choice < 1 or bot_choice > len(available_bots):
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
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

            flash_message = flash_data.get_and_reset()
            if flash_message:
                print("Message: " + flash_message)

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
        #os.system('cls' if os.name == 'nt' else 'clear')

        print("\nBot Troop 369 - Main Menu")
        print("1. Configure a bot")
        print("2. Service a bot")
        print("3. Display running bots")
        print("4. Connect a bot")
        print("5. Configure Globals (e.g. RPC Portmap for all bots)")
        print("6. Play Zip-Zap-Zop")
        print("7. Tools")
        print("9. Exit")

        flash_message = flash_data.get_and_reset()
        if flash_message:
            print("Message: " + flash_message)

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                bot_name = display_available_bots(bot_manager, flash_data)
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
                current_flash_data = flash_data.get_and_reset()
                print(f"Current flash_data: {current_flash_data}")  # Debug print
                bot_name = "your_bot_name"  # Replace with your actual bot name
                if current_flash_data == ZIP:
                    print("Sending ZAP message")  # Debug print
                    await bot_manager.send_message(bot_name, ZAP)
                elif current_flash_data == ZAP:
                    print("Sending ZOP message")  # Debug print
                    await bot_manager.send_message(bot_name, ZOP)
                else:
                    flash_data.set("You Lost")

            elif choice == "7":
                await tools_menu()

            elif choice == "8":
                pass

            elif choice == "9":
                sys.exit()

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            flash_data.set(str(e))

if __name__ == "__main__":
    asyncio.run(main())
