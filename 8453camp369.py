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
from typing import List, Dict
import runpy
import traceback
import getpass  # To securely get user input

# Import bot constructor class(es) here
from B07 import B07
from B07_D474 import D474
from B07_Y4ML import Y4ML
from B07_S3CR375 import S3CR375

# # Constants for `Wake Up` game.
# ZIP = "219"
# ZAP = "249"
# ZOP = "209"

class BotDoesNotExistInDictionaryError(Exception):
    pass

class Signal369: #bot_manager
    """
    This class represents a bot manager, providing functionality for managing multiple bot instances. 

    The class handles tasks such as starting, stopping, and restarting bots, as well as retrieving and managing bot keys and tokens. 

    It also includes functionality for handling and waiting for asynchronous tasks related to the bots, getting active bots, and loading bot configurations.
    """

    def __init__(self, data):
        """
        Initializes a Signal369 instance, which sets up a dictionary to store bot instances and their respective 
        tasks, initializes the data manager, and loads the required keys and tokens.

        Args:
            data (D474): represents a Data Manager, providing logging functionalities + message passing.

        Returns:
            None
        """
    def __init__(self, data):
        self.bots = {}
        self.bot_tasks = {}
        self.data = data
        self.secrets = self.init_secrets_manager(self.data)
        self.yaml = Y4ML(data)
        # Checking and loading keys and tokens.
        if os.path.isfile('___keys___.yaml.enc') and os.path.isfile('__tokens__.yaml.enc'):
            self.load_keys()
            self.load_tokens()
        else:
            self.first_time_setup()

    def first_time_setup(self):
        """
        First time setup for generating and saving encryption key and encrypted config files.
        """
        self.secrets.generate_key()
        self.secrets.save_key(self.secrets.key_file)
        keys = self.yaml.load_yaml_file("___keys___.yaml")
        tokens = self.yaml.load_yaml_file("__tokens__.yaml")
        self.secrets.save_encrypted_yaml(keys, '___keys___.yaml.enc')
        self.secrets.save_encrypted_yaml(tokens, '__tokens__.yaml.enc')
        self.keys = keys
        self.tokens = tokens
        self.data.set_flash('debug', 'First time setup completed')

    def init_secrets_manager(self, data):
        """
        Initializes the SecretsManager with a private key obtained from the user and returns the DataManager instance.

        Args:   
            None

        Returns:
            yaml_manager (Y4ML): An instance of the YamlManager.
        """
        # Prompt the user for a private key to use with SecretsManager
        private_key = getpass.getpass(prompt='Enter the private key for SecretsManager: ')
        
        # Instantiate SecretsManager and YAMLManager with SecretsManager
        secrets_manager = S3CR375(data, private_key)  # Creates new instance of SecretsManager from DataManager
        
        return secrets_manager

    def load_keys(self):
        """
        Loads keys from a YAML file named "___keys___.yaml" using the data manager instance.

        Args:   None
        Returns:    None
        """
        # Load keys from the ___keys___.yaml file
        self.data.set_flash('debug', 'Loading keys...')
        self.keys = self.secrets.load_encrypted_yaml("___keys___.yaml.enc")
        self.data.set_flash('debug', f'Keys loaded: {self.keys}')

    def load_tokens(self):
        """
        Loads tokens from a YAML file named "__tokens__.yaml" using the data manager instance.

        Args:   None
        Returns:    None
        """
        # Load tokens from the __tokens__.yaml file
        self.data.set_flash('debug', 'Loading tokens...')
        self.tokens = self.secrets.load_encrypted_yaml("__tokens__.yaml.enc")
        self.data.set_flash('debug', f'Tokens loaded: {self.tokens}')

    # Return a list of bots that have an init file and a Discord token.
    def get_available_bots(self) -> List[str]:
        """
        Returns a list of bot names that have an encrypted initialization file and a Discord token.

        Args:
            None

        Returns:
            available_bots (List[str]): A list of names of available bots.
        """
        available_bots = []
        # Use keys and tokens dictionary instead of reading yaml files.
        for bot_name in self.tokens.keys():
            if bot_name.endswith("_discord_token"):
                bot_name_stripped = bot_name.replace('_discord_token', '')
                if f"{bot_name_stripped}_telegram_api_hash" in self.keys and f"{bot_name_stripped}_aws_secret_access_key" in self.keys:
                    available_bots.append(bot_name_stripped)
        self.data.set_flash('Debug', 'Available bots: ' + ', '.join(available_bots))
        return available_bots

    async def start_bot(self, bot_name: str):
        """Starts a specified bot by performing the following tasks:

        1. Checking bot instance: 
            Checks if the bot has already been started. If so, it issues a warning and returns.
        
        2. Configuration retrieval: 
            Merges the configuration files to get the most updated configuration for the bot.

        3. Key retrieval: 
            Retrieves all necessary keys from the SecretsManager.
        
        4. Bot instantiation: 
            Instantiates a new B07 object using the retrieved keys and configuration data.

        5. Task creation: 
            Starts the bot as an asyncio task and adds it to the task dictionary.

        6. Bot addition to dictionary: 
            Adds the bot object to the dictionary of bot objects for reference.

        Args:
            bot_name (str): The name of the bot to start.

        Returns:
            error_message (str): In case of an error, returns an error message. Otherwise, returns None upon successful bot startup.
        """
        if bot_name in self.bots:
            warning_message = f"Bot `{bot_name}` has already been started. Please stop it before attempting to start a new instance."
            self.data.set_flash('warning', warning_message)
            return 

        # Retrieve bot configuration and token
        config_files = ["_init__global.yaml", f"_init_{bot_name}.yaml"]
        merged_config = self.yaml.merge_yaml_files(config_files)
        bot_init_data = merged_config

        discord_token = None
        aws_secret_access_key = None
        aws_access_key_id = None
        openai_key = None
        telegram_api_id = None
        telegram_api_hash = None

        # Retrieve keys
        try:
            discord_token = self.tokens[f"{bot_name}_discord_token"]
            aws_secret_access_key = self.keys[f"{bot_name}_aws_secret_access_key"]
            aws_access_key_id = bot_init_data.get("aws_access_key_id")
            openai_key = self.keys["openai_api_key"]
            telegram_api_id = bot_init_data.get("telegram_api_id")
            telegram_api_hash = self.keys[f"{bot_name}_telegram_api_hash"]

            self.data.set_flash('debug', f"Keys Dictionary: {self.keys}")
            self.data.set_flash('debug', f"aws_secret_access_key for {bot_name}: {aws_secret_access_key}")
            self.data.set_flash('debug', f"aws_access_key_id for {bot_name}: {aws_access_key_id}")
        except AttributeError as e:
            error_message = f"An attribute is missing for {bot_name}. Please check the bot's configuration, and the keys and tokens yaml files. {str(e)}"
            self.data.set_flash('error', error_message)
            return error_message
        except KeyError as e:
            error_message = f"A key property is missing for {bot_name}. Please check the bot's configuration, and the keys and tokens yaml files. {str(e)}"
            self.data.set_flash('error', error_message)
            return error_message

        if discord_token is None:
            warning_message = f"The discord_token is set to None for {bot_name}. Please check the ___tokens__.yaml file."
            self.data.set_flash('warning', warning_message)
        else:
            self.data.set_flash('debug', f"Retrieved discord_token for {bot_name}.")

        if aws_secret_access_key is None or aws_access_key_id is None:
            warning_message = f"The aws_secret_access_key or aws_access_key_id is set to None for {bot_name}. Please check the ___keys__.yaml file."
            self.data.set_flash('warning', warning_message)
        else:
            self.data.set_flash('debug', f"Retrieved AWS keys for {bot_name}.")

        if openai_key is None:
            warning_message = f"The openai_api_key is set to None for {bot_name}. Please check the ___keys__.yaml file."
            self.data.set_flash('warning', warning_message)
        else:
            self.data.set_flash('debug', f"Retrieved openai_api_key for {bot_name}.")

        if telegram_api_id is None or telegram_api_hash is None:
            warning_message = f"The Telegram api_id or api_hash is set to None for {bot_name}. Please check the _init_{bot_name}.yaml and the ___keys__.yaml files."
            self.data.set_flash('warning', warning_message)
        else:
            self.data.set_flash('debug', f"Retrieved Telegram api_id and api_hash for  {bot_name}.")

        # Create and store the bot instance
        try:
            bot = B07(self.secrets, self.data, bot_name, bot_init_data, openai_key, discord_token, telegram_api_id, telegram_api_hash, aws_secret_access_key, aws_access_key_id)

            # Create bot task and handle done task
            task = asyncio.create_task(bot.start_bit_manager())
            self.bot_tasks[bot_name] = task
            task.add_done_callback(self.handle_bot_task_done)

            # Add the bot to the dictionary after it starts successfully
            self.bots[bot_name] = bot

            # Check if the bot_name exists in the dictionary
            if bot_name not in self.bots:
                raise BotDoesNotExistInDictionaryError(f"Bot {bot_name} does not exist in dictionary!")

        except BotDoesNotExistInDictionaryError as e:
            self.data.set_flash('critical', str(e))
            raise e  # Or handle the error accordingly, depending on the use case

        except Exception as e:
            traceback.print_exc() 
            error_message = f"Error starting bot {bot_name}: {str(e)}"
            self.data.set_flash('error', error_message)
            return error_message

        else:
            self.data.set_flash('info', f'{bot_name} started successfully')

    def handle_bot_task_done(self, task: asyncio.Task):
        """
        Handles the completion of a bot task by logging the completion or error messages, depending on whether the task 
        was completed successfully or resulted in an exception.

        Args:
            task (asyncio.Task): The completed task.

        Returns:
            None
        """
        if task.cancelled():
            self.data.set_flash('info', f"Task was cancelled: {task}")
        else:
            exc = task.exception()
            if exc:
                self.data.set_flash('error', f"Error starting bot task: {exc}")

    async def stop_bot(self, bot_name: str):
        """
        Stops the specified bot by calling the bot's close method and removes it from the bot and tasks dictionaries.

        Args:
            bot_name (str): The name of the bot to stop.

        Returns:
            None
        """
        bot = self.bots[bot_name]
        await bot.close()
        del self.bots[bot_name]
        del self.bot_tasks[bot_name]
        self.data.set_flash('info', f'Bot `{bot_name}` Stopped')

    async def restart_bot(self, bot_name: str):
        """
        Restarts the specified bot by first stopping it and then starting it again.

        Args:
            bot_name (str): The name of the bot to restart.

        Returns:
            None
        """
        await self.stop_bot(bot_name)
        self.data.set_flash('debug', f'Bot `{bot_name}` Stopped')
        await self.start_bot(bot_name)
        self.data.set_flash('info', f'Bot `{bot_name}` Restarted')

    async def wait_for_bots(self):
        """
        Waits for all bot tasks to complete using asyncio.gather. This function is used to prevent the main application
        from exiting until all bots have completed their tasks.

        Args:   None
        Returns:    None
        """
        tasks = list(self.bot_tasks.values())
        if tasks:
            self.data.set_flash('debug', 'wait_for_bots')
            await asyncio.gather(*tasks)
    
    def get_active_bots(self) -> List[str]:
        """
        Returns a list of the names of currently active bots, i.e., those whose tasks are not yet done.

        Args:
            None

        Returns:
            active_bots (List[str]): A list of names of currently active bots.
        """
        active_bots = [bot_name for bot_name, task in self.bot_tasks.items() if not task.done()]
        self.data.set_flash('debug', 'Got active bots.')
        return active_bots

    def configure_bot(self, bot_name: str):
        """
        Configures the specified bot. The specific configuration details are not provided.

        Args:
            bot_name (str): The name of the bot to configure.

        Returns:
            None
        """
        try:
            # Implement configuration logic here
            self.data.set_flash('info', f'Bot `{bot_name}` Configured')
        except Exception as e:
            import traceback
            traceback.print_exc() 
            self.data.set_flash('critical', f'Error configuring bot {bot_name}: {str(e)}')

    def configure_rpc_portmap(self):
        """
        Configures the RPC portmap. The specific configuration details are not provided.

        Args:   None
        Returns:    None
        """
        # Implement RPC portmap configuration logic here
        self.data.set_flash('debug', f'`Global` configure_rpc_portmap')

async def tools_menu(bot_manager):
    while True:
        clear_console()
        print("\nTools - Pirate Menu")
        print("1. Back to Main Menu")
        print("2. Horse Stable")
        print("3. Flash World")
        print("4. Test AWS for Active bots")
        print("5. Move files to S3.") 

        print(bot_manager.data.get_flash_and_reset())

        choice = input("Enter your choice: ")

        if choice == "1":
            break

        elif choice == "2":
            print("Running Horse Stable...")
            runpy.run_path("pirate_horse_stable.py")
            bot_manager.data.set_flash('info', "Horse Stable script completed.")
            break

        elif choice == "3":
            bot_manager.data.set_flash('info', "Hello World")
            break

        elif choice == "4":
            active_bots = bot_manager.get_active_bots()
            if active_bots:
                bot_manager.data.set_flash('info', 'Testing AWS for Active bots.')
                for i, bot_name in enumerate(active_bots, start=1):
                    bot = bot_manager.bots[bot_name]
                    bot_status = bot.get_bit_status()

                    # Check if the bot's AWS bit has been initialized
                    if not bot_status["aws_api"]:
                        result = f"{i}. Bot {bot_name} has not initialized its AWS bit."
                        bot_manager.data.set_flash('warning', result)
                    else:
                        bot_init_data = bot.bot_init_data
                        aws_bucket = bot_init_data.get("aws_bucket", "")
                        if not aws_bucket:
                            warning_message = f"AWS bucket is not configured for {bot_name}. Please check the _init_{bot_name}.yaml file."
                            bot_manager.data.set_flash('warning', warning_message)
                        else:
                            test_key = "test-file.txt"
                            test_content = "This is a test."
                            try:
                                s3_test_result = await bot.bit_manager.aws_bit.test_s3(aws_bucket, test_key, test_content)
                                if s3_test_result:
                                    result = f"{i}. Bot {bot_name} can successfully read, write, and delete using aws_bit."
                                    bot_manager.data.set_flash('info', result)
                                else:
                                    result = f"{i}. Bot {bot_name} failed the S3 read/write test."
                                    bot_manager.data.set_flash('error', result)
                            except Exception as e:
                                traceback.print_exc()
                                error_message = f"An error occurred while testing S3 for Bot {bot_name}: {str(e)}"
                                bot_manager.data.set_flash('error', error_message)

                # Display flash data whether or not an AWS test was attempted
                print(bot_manager.data.get_flash_and_reset())
            input("Press any key to return to the main menu...")

        elif choice == "5":
            active_bots = bot_manager.get_active_bots()
            if active_bots:
                bot_manager.data.set_flash('info', 'Moving files to S3 for Active bots.')
                for i, bot_name in enumerate(active_bots, start=1):
                    bot = bot_manager.bots[bot_name]
                    await bot.move_files_to_s3()
                    bot_manager.data.set_flash('info', f"{i}. Bot {bot_name} moved files to S3.")
        else:
            bot_manager.data.set_flash('warning', 'Invalid choice. Please try again.')

async def manage_available_bots(bot_manager: Signal369):
    # First, the bot is selected before entering the loop
    bot_name = select_a_bot(bot_manager, bot_manager.get_available_bots(), 'available')

    print(bot_manager.data.get_flash_and_reset())

    if bot_name is None:
        bot_manager.data.set_flash('warning', 'No bots are available.')
        return  # Return to the main menu if no available bots

    while True:
        clear_console()
        print(f"\nManage {bot_name}")
        print("1. Back to Main Menu")
        print(f"2. Configure {bot_name}")
        print(f"3. Start {bot_name}")

        print(bot_manager.data.get_flash_and_reset())

        choice = input("Enter your choice: ")

        if choice == "1":
            return  # Back to Main Menu

        elif choice == "2":
            try:
                bot_manager.configure_bot(bot_name)
            except Exception as e:
                import traceback
                traceback.print_exc()
                bot_manager.data.set_flash('critical', f'Error during bot configuration: {str(e)}')
        
        elif choice == "3":
            error_returned = await bot_manager.start_bot(bot_name)
            if error_returned:
                bot_manager.data.set_flash('debug', f'Error returned starting bot: {error_returned}')
            return  # Return to Main Menu after Start

async def manage_active_bots(bot_manager: Signal369):
    while True:
        clear_console()
        print("\nService Menu")
        print("1. Back to Main Menu")
        print("2. Bit Manager")
        print("3. Restart a bot")
        print("4. Shutdown a bot")

        print(bot_manager.data.get_flash_and_reset())

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                break

            elif choice == "2":
                await connect_bit(bot_manager)

            elif choice == "3":
                    for i, bot_name in enumerate(bot_manager.bots.keys(), start=1):
                        print(f"{i}. {bot_name}")

                    bot_choice = int(input("Enter the number of the bot you want to restart: "))
                    bot_name = list(bot_manager.bots.keys())[bot_choice - 1]
                    await bot_manager.restart_bot(bot_name)

            elif choice == "4":
                if not bot_manager.bots:
                    bot_manager.data.set_flash('info', 'No bots are currently Active.')
                else:
                    print("\nActive bots:")
                    for i, bot_name in enumerate(bot_manager.bots.keys(), start=1):
                        print(f"{i}. {bot_name}")

                    try:
                        bot_choice = int(input("Enter the number of the bot you want to stop: "))
                        if bot_choice < 1 or bot_choice > len(bot_manager.bots):
                            raise ValueError('Invalid choice. Please try again.')

                        bot_name = list(bot_manager.bots.keys())[bot_choice - 1]
                        await bot_manager.stop_bot(bot_name)
                    except (ValueError, IndexError) as e:
                        bot_manager.data.set_flash('warning', str(e))

        except Exception as e:
            import traceback
            traceback.print_exc() 
            bot_manager.data.set_flash('critical', f'Error during servicing a bot: {str(e)}')

async def connect_bit(bot_manager):
    bot_name = select_a_bot(bot_manager, bot_manager.get_active_bots(), 'active')

    if bot_name is not None:
        bot = bot_manager.bots[bot_name]  # Assuming bots are stored in a dictionary in bot_manager

        while True:
            clear_console()
            print("\nBit Connector Menu for: " + bot_name)
            print("1. Back to Main Menu")
            print("2. Start Discord")
            print("3. Start Telegram")
            print("4. Start AWS")
            print("5. Start OpenAi")

            print(bot_manager.data.get_flash_and_reset())

            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    break
                elif choice == "2":
                    # Initialize the Discord bit
                    bot.bit_manager.init_bit('discord_api')
                    bot.data.set_flash('debug', 'Instantiating Discord Bit')
                elif choice == "3":
                    # Initialize the Telegram bit
                    bot.bit_manager.init_bit('telegram_api')
                    bot.data.set_flash('debug', 'Instantiating Telegram Bit')
                elif choice == "4":
                    # Initialize the AWS bit
                    bot.bit_manager.init_bit('aws_api')
                    bot.data.set_flash('debug', 'Instantiating AWS Bit')
                elif choice == "5":
                    # Initialize the OpenAi bit
                    bot.bit_manager.init_bit('openai_api')
                    bot.data.set_flash('debug', 'Instantiating OpenAi Bit')
                else:
                    warning_message = 'Invalid choice. Please try again.'
                    bot.data.set_flash('warning', warning_message)
            except Exception as e:
                import traceback
                traceback.print_exc() 
                bot.data.set_flash('critical', f'Error during connecting bit: {str(e)}')

def select_a_bot(bot_manager, bot_list: List[str], bot_type: str):
    if not bot_list:
        bot_manager.data.set_flash('info', f'No {bot_type} bots.')
        return None

    clear_console()
    print(f"\n{bot_type.capitalize()} bots:")
    for i, bot_name in enumerate(bot_list, start=1):
        print(f"{i}. {bot_name}")

    while True:
        try:
            bot_choice = int(input(f"Enter the number of the bot you want to select from the {bot_type} bots: "))
            if bot_choice < 1 or bot_choice > len(bot_list):
                raise ValueError('Invalid choice. Please try again.')
            bot_name = bot_list[bot_choice - 1]
            return bot_name
        except (ValueError, IndexError) as e:
            bot_manager.data.set_flash('warning', str(e))

def clear_console():
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

async def main_menu(bot_manager):
    clear_console()
    print("\nBot Troop 369 - Main Menu")
    print("1. Manage Available Bots")
    print("2. Manage Active Bots")
    print("3. Display Active bots")
    print("4. ")
    print("5. Configure Globals (e.g. RPC Portmap for all bots)")
    print("6. Play Zip-Zap-Zop")
    print("7. Tools")
    print("9. Exit")

    print(bot_manager.data.get_flash_and_reset())

    choice = input("Enter your choice: ")

    try:
        if choice == "1":
            try:
                await manage_available_bots(bot_manager)
            except Exception as e:
                import traceback
                traceback.print_exc() 
                bot_manager.data.set_flash('critical', f'{str(e)}')

        elif choice == "2":
            try:
                await manage_active_bots(bot_manager)
            except Exception as e:
                import traceback
                traceback.print_exc() 
                bot_manager.data.set_flash('critical', f'{str(e)}')

        elif choice == "3":
            active_bots = bot_manager.get_active_bots()
            if active_bots:
                clear_console()
                print("Active bots:")
                for i, bot_name in enumerate(active_bots, start=1):
                    # Accessing the bot instance
                    bot = bot_manager.bots[bot_name]
                    # Use logging level as color, default to 'info' if color not found
                    bot_color = bot_manager.data.level_colors.get(bot.bot_init_data.get("color", "info"), "\033[37m")
                    # reset color after printing
                    print(f"{bot_color}{i}. {bot_name} [{bot.leet_name}] - Bit switches: {bot._bit_switches()}\033[0m")
                input("Press any key to return to the main menu...")
            else:
                bot_manager.data.set_flash('info', 'No bots are currently Active.')

        elif choice == "4":
            try:
                pass
            except Exception as e:
                import traceback
                traceback.print_exc() 
                bot_manager.data.set_flash('critical', f'{str(e)}')

        elif choice == "5":
            try:
                bot_manager.configure_rpc_portmap()
            except Exception as e:
                import traceback
                traceback.print_exc() 
                bot_manager.data.set_flash('critical', f'{str(e)}')

        elif choice == "6":
            pass
            # if current_flashdata == ZIP:
            #     bot_manager.data.set_flash('info', f'Sending ZAP message: {ZAP}')
            #     await bot_manager.send_message(bot_name, ZAP)
            # elif current_flashdata == ZAP:
            #     bot_manager.data.set_flash('info', f'Sending ZOP message: {ZOP}')
            #     await bot_manager.send_message(bot_name, ZOP)
            # else:
            #     bot_manager.data.set_flash("You Lost")
            #     print(bot_manager.data.get_flash_and_reset())

        elif choice == "7":
            try:
                await tools_menu(bot_manager)
            except Exception as e:
                import traceback
                traceback.print_exc() 
                bot_manager.data.set_flash('critical', f'{str(e)}')

        elif choice == "8":
            pass

        elif choice == "9":
            bot_manager.data.set_flash('info', "Exit selected from Main Menu")
            raise KeyboardInterrupt

        else:
                warning_message = 'Invalid choice. Please try again.'
                bot_manager.data.set_flash('warning', warning_message)

    except Exception as e:
        import traceback
        traceback.print_exc() 
        bot_manager.data.set_flash('critical', f'Error during main menu operation: {str(e)}')

async def main():
    # Create an instance of D474
    data = D474()
    # Pass the instance to Signal369
    bot_manager = Signal369(data)
  
    try:
        while True:
            # os.system('cls' if os.name == 'nt' else 'clear')
            await main_menu(bot_manager)
    except KeyboardInterrupt:
        # Cancel all running tasks on KeyboardInterrupt
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())

# :C6N5:
# C.G. Name Space
# :6FY: