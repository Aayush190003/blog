from playwright.sync_api import sync_playwright
import logging
import os

# Configuration
TOTAL_EXECUTIONS = 1000
LOG_FILE_PATH = 'process_log.log'
COUNT_FILE_PATH = 'execution_count.txt'
BLOG_URL = "https://psychocoder001.blogspot.com/2024/07/how-to-increase-your-youtube.html"

# Set up logging
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def visit_and_scroll(url):
    try:
        with sync_playwright() as p:
            # Launch Brave browser
            browser = p.chromium.launch(headless=False, args=["--incognito", "--disable-extensions"])
            page = browser.new_page()

            # Navigate to the URL
            page.goto(url)
            logging.info(f"Navigating to: {url}")

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

            logging.info(f"Scrolled through: {url}")
            browser.close()
    except Exception as e:
        logging.error(f"An error occurred while visiting and scrolling: {e}")

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

    for i in range(1, TOTAL_EXECUTIONS + 1):
        logging.info(f"Execution {i} of {TOTAL_EXECUTIONS}")
        print(f"Execution {i} of {TOTAL_EXECUTIONS}")

        visit_and_scroll(BLOG_URL)

        update_execution_count(i)

    logging.info("Process finished.")
    print("Process finished.")

if __name__ == "__main__":
    main()
