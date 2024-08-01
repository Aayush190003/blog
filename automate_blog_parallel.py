from playwright.sync_api import sync_playwright
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
TOTAL_EXECUTIONS = 1000
LOG_FILE_PATH = 'process_log.log'
COUNT_FILE_PATH = 'execution_count.txt'
BLOG_URL = "https://psychocoder001.blogspot.com/2024/07/how-to-increase-your-youtube.html"
NUM_THREADS = 3  # Number of parallel threads

# Set up logging
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def visit_and_scroll(url, execution_number):
    try:
        with sync_playwright() as p:
            # Launch Brave browser
            browser = p.chromium.launch(headless=False, args=["--incognito", "--disable-extensions"])
            page = browser.new_page()

            try:
                # Navigate to the URL
                page.goto(url)
                logging.info(f"Execution {execution_number}: Navigating to {url}")

                # Scroll to the bottom of the page
                page.evaluate('''
                    (async () => {
                        let lastHeight = document.body.scrollHeight;
                        while (true) {
                            window.scrollTo(0, document.body.scrollHeight);
                            await new Promise(resolve => setTimeout(resolve, 2000));
                            let newHeight = document.body.scrollHeight;
                            if (newHeight === lastHeight) break;
                            lastHeight = newHeight;
                        }
                    })();
                ''')

                logging.info(f"Execution {execution_number}: Scrolled through {url}")
            finally:
                browser.close()  # Ensure browser is closed even if an error occurs
    except Exception as e:
        logging.error(f"Execution {execution_number}: An error occurred while visiting and scrolling: {e}")

def update_execution_count(count):
    try:
        with open(COUNT_FILE_PATH, 'w') as file:
            file.write(str(count))
        logging.info(f"Process executed {count} times.")
    except Exception as e:
        logging.error(f"An error occurred while updating execution count: {e}")

def main():
    logging.info("Process started.")
    print("Process started.")

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # Create a list of tasks
        futures = [executor.submit(visit_and_scroll, BLOG_URL, i) for i in range(1, TOTAL_EXECUTIONS + 1)]
        
        # Wait for all tasks to complete
        for future in as_completed(futures):
            try:
                future.result()  # This will raise any exception caught during execution
            except Exception as e:
                logging.error(f"An error occurred in a parallel execution: {e}")

    # Update execution count after all parallel processes are done
    update_execution_count(TOTAL_EXECUTIONS)

    logging.info("Process finished.")
    print("Process finished.")

if __name__ == "__main__":
    main()
