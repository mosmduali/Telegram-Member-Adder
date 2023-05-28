"""
27.05.2023 - ∞
"""
import time, os, sys, json
import random

from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import (PeerFloodError, UserNotMutualContactError,
                                          UserPrivacyRestrictedError, UserChannelsTooMuchError,
                                          UserBotError, InputUserDeactivatedError, ChatAdminRequiredError,FloodWaitError)





# Colors
red = "\u001b[31;1m"
green = "\u001b[32m"
yellow = "\u001b[33;1m"
blue = "\u001b[34m"
magenta = "\u001b[35m"
cyan = "\u001b[36m"
reset = "\u001b[0m"

clear_console = lambda: os.system('cls')
clear_console()

#
api_id = ""
api_hash = ""
phone_number = ""
#

if os.path.isfile('MyApiHash.json'):
    with open("MyApiHash.json", 'r') as read:
        my_data = json.load(read)
    api_id = my_data["api_id"]
    api_hash = my_data["api_hash"]
    phone_number = my_data["phone_number"]


else:
    api_id = input("Please Enter api_id: ").strip()
    api_hash = input("Please Enter api_hash: ").strip()
    phone_number = input("Please enter your phone number (with country code): ")
    with open("MyApiHash.json", 'w') as a:
        json.dump({"phone_number": phone_number, "api_id": api_id, "api_hash": api_hash}, a)

client = TelegramClient("{0}".format(phone_number), api_id, api_hash)
client.start(phone=phone_number)


def spamControl():
    spamBotMessage = "Good news, no limits are currently applied to your account. You’re free as a bird!"
    bot = 'SpamBot'
    command = '/start'
    client.send_message(bot, command)

    @client.on(events.NewMessage(chats='SpamBot'))
    async def handle_new_message(event):
        command = event.message
        if(command.text == spamBotMessage):
            pass
        else:
            get_my_number()
            print(red+"[!] "+command.text)
            input(green+"So I can't continue... (Press ENTER to exit): "+reset)
            sys.exit()

spamControl()

def banner():
    banner = f"""| {red}github.com/{green}muhammedosmanduali{reset}
| {red}linkedin.com/in/{green}muhammedosmanduali{reset}
| {red}instagram.com/{green}mosmanduali{reset}
| {red}t.me/{green}DualiWithUs{reset}
    """
    print(banner)

def get_my_number():
    banner()
    print("{0}Your Number: {1} {2}\n\n".format(yellow, green, phone_number))


def delete_user(userId):
    with open("Users.json", 'r') as read:
        user_data = json.load(read)

    update_new_data = [item for item in user_data if item["user_id"] != userId]

    with open("Users.json", 'w') as write:
        json.dump(update_new_data, write)


async def main():
    clear_console()
    async def getmem():
        clear_console()
        get_my_number()
        try:
            print("{0}[+] Select a Group or Channel to add users.".format(yellow))
            empty = 0
            for i in channel:
                print("{0}[{1}] {2}".format(green, str(empty), i.title))
                empty += 1
            option = input("{0}Enter a number: {1}".format(yellow, reset))
            if str(option).isdigit():
                if int(option) > len(channel) - 1 or int(option) < 0:
                    input("{0}[!] Select one of the listed Groups or Channels. (Press ENTER to skip): {1}".format(red, reset))
                    await getmem()
                else:
                    option = int(option)
                    pass
            else:
                input("{0}[!] Invalid character entered. (Press ENTER to skip): {1}".format(red, reset))
                await getmem()

            my_participants = await client.get_participants(channel[option])
            target_group_entity = InputPeerChannel(channel[option].id, channel[option].access_hash)
            my_participants_id = []
            for my_participant in my_participants:
                my_participants_id.append(my_participant.id)
        except ChatAdminRequiredError:
            input(
                "{0}[!] You don't have admin privileges for the Group or Channel '{1}'! (Press ENTER to skip): {2}".format(
                    red, channel[option].title, reset))
            await getmem()

        count = 1
        peer_flood_status = 0
        user_insertion_limit = 0
        check = 0
        with open("Users.json", 'r') as read:
            users = json.load(read)
        for user in users:
            if user_insertion_limit == 40 and check == 0:
                print("\nWait...")
                time.sleep(2)
                clear_console()
                get_my_number()
                option = input(
                    "{0}[!] 40th user limit reached! Having more users may lead to restrictions or closure of the account.\n{1}Do you want to continue? Y(yes)/N(no): {2}".format(
                        red, green, reset))
                if option == 'Y' or option == 'y':
                    clear_console()
                    get_my_number()
                    check = 1
                    continue
                elif option == 'N' or option == 'n':
                    print("{0}[!] Exiting the program...".format(red))
                    time.sleep(3)
                    await client.disconnect()
                    break
                else:
                    print("{0}[!] Please enter a valid command! (Press ENTER to skip): {1}".format(red, reset))
                    continue
            check = 0
            if count % 50 == 0:
                clear_console()
                get_my_number()
                print("{0}[!] Please wait for 1 minute...".format(yellow))
                time.sleep(60)
            elif count >= 300:
                await client.disconnect()
                break
            elif peer_flood_status >= 8:
                clear_console()
                get_my_number()
                print(
                    "{0}[!] The account is experiencing a FLOOD error!\n{1}FLOOD error typically occurs in the following situations:\n\t1. If an account sends too many messages or requests within a certain period of time.\n\t2. If an account invites too many users within a certain period of time.\n\t3. If an account joins too many groups or channels within a certain period of time.\n{2}For the safety of your account, the program will be closed in 60 seconds.{3}".format(
                        red, green, red, reset))
                time.sleep(60)
                await client.disconnect()
                break
            count += 1
            time.sleep(1)
            if user["user_id"] in my_participants_id:
                print("{0}User already exists. {1} Skipped.".format(red, user["user_id"]))
                delete_user(user["user_id"])
                continue
            else:
                try:
                    user_to_add = InputPeerUser(user["user_id"], user["access_hash"])
                    add = await client(InviteToChannelRequest(target_group_entity, [user_to_add]))
                    print("{0}{1}. User added. UserID: {2}".format(green, user_insertion_limit + 1, str(user["user_id"])))
                    delete_user(user["user_id"])
                    user_insertion_limit += 1
                except PeerFloodError:
                    print("{0}[!] Flood error received from Telegram.".format(red))
                    peer_flood_status += 1
                except UserPrivacyRestrictedError:
                    print("{0}The user's privacy settings do not allow me to perform this action. UserID: {1} Skipped.".format(red, str(user["user_id"])))
                    delete_user(user["user_id"])
                except InputUserDeactivatedError:
                    print("{0}The specified user does not exist on Telegram. UserID: {1} Skipped.".format(red, str(
                        user["user_id"])))
                    delete_user(user['user_id'])
                except UserBotError:
                    print("{0}The bot cannot be added. UserID: {1} Skipped.".format(red, str(user["user_id"])))
                    delete_user(user['user_id'])
                except UserChannelsTooMuchError:
                    print("{0}The user is in too many channels. UserID: {1} Skipped.".format(red, str(user["user_id"])))
                    delete_user(user['user_id'])
                except UserNotMutualContactError:
                    print("{0}You are not a mutual contact in the other person's address book. UserID: {1} Skipped.".format(red, str(user["user_id"])))
                    delete_user(user['user_id'])
                except FloodWaitError as e:
                    peer_flood_status +=8
                except Exception as e:
                    delete_user(user["user_id"])
                    continue

    get_my_number()
    chats = []
    channel = []
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))
    chats.extend(result.chats)
    for a in chats:
        try:
            if True:
                channel.append(a)
        except:
            continue
    a = 0
    print("{0}[~] Choose a group or channel to scrape.".format(yellow))
    for i in channel:
        print("{0}[{1}]".format(green, a), i.title)
        a += 1
    while True:
        option = input("{0}Enter a number to select (or press ENTER to skip): {1}".format(yellow, reset))
        if option.isdigit():
            if int(option) > len(channel) - 1 or int(option) < 0:
                input("{0}[!] Please select a valid Group or Channel to scrape. (Press ENTER to skip): {1}".format(red,
                                                                                                                   reset))
                await main()
            else:
                break
        else:
            print("{0}[!] Skipping...".format(yellow))
            time.sleep(1)
            await getmem()
            sys.exit()
            break
    option = int(option)

    try:
        print("")
        print("{0}[+] Users are being scraped...".format(yellow))
        time.sleep(1)
        target_group = channel[option]
        all_participants = []
        mem_details = []
        all_participants = await client.get_participants(target_group)
    except ChatAdminRequiredError:
        input(
            "{0}[!] You don't have admin privileges for the Group or Channel '{1}'! (Press ENTER to skip): {2}".format(
                red, channel[option].title, reset))
        await main()
    for user in all_participants:
        try:
            new_mem = {
                "user_id": user.id,
                "access_hash": user.access_hash
            }
            mem_details.append(new_mem)
        except ValueError:
            continue

    with open("Users.json", 'w') as write:
        json.dump(mem_details, write)
    time.sleep(1)
    print("{0}[!] Please wait...".format(yellow))
    time.sleep(3)
    input("{0}[+] Users have been scraped successfully. (Press ENTER to skip): {1}".format(green, reset))

    await getmem()

    await client.disconnect()


with client:
    client.loop.run_until_complete(main())
