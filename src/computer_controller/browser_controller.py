from datetime import datetime as dt
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.firefox import GeckoDriverManager
from spotipy.oauth2 import SpotifyOAuth
from src.computer_controller.utils import ff_get_profile_path, is_installed
from src.computer_controller.log import get_logger
from googleapiclient.discovery import build
from dotenv import load_dotenv
import spotipy as sp
import atexit
import json
import os
import re



load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Spotify API credentials
SP_CLIENT_ID     = os.getenv("SPOTIPY_CLIENT_ID")
SP_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SP_REDIRECT_URI  = os.getenv("SPOTIPY_REDIRECT_URI")

RESTORE_DELAY = 0.75


class BrowserController:
    _instance = None  # Singleton instance
    _state_file = "browser_state.json"  # File to save the browser state

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BrowserController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, /, headless=False):
        if self._initialized: return

        self.logger = get_logger(__name__)
        self.youtube = build('youtube', 'v3', developerKey=GOOGLE_API_KEY)
        self.spotify = spotify = sp.Spotify(auth_manager=SpotifyOAuth(
            client_id=SP_CLIENT_ID,
            client_secret=SP_CLIENT_SECRET,
            redirect_uri=SP_REDIRECT_URI,
            scope="user-read-playback-state, user-modify-playback-state"
        ))


        self.headless = headless
        self.profile_path = ff_get_profile_path()

        # Configure Firefox options
        options = FirefoxOptions()
        options.add_argument("--no-remote")
        if self.headless:
            options.add_argument("--headless")  # Run in headless mode

        # Set a real user-agent to avoid detection
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        # Set page load strategy to "eager" (do not wait for full page load)
        options.set_capability("pageLoadStrategy", "eager")

        # If a profile path is provided, use it
        if self.profile_path:
            options.add_argument("--profile")
            options.add_argument(self.profile_path)
            self.logger.info(f"Launching Firefox with profile: {self.profile_path}")

        # Initialize the Firefox WebDriver
        try:
            self.driver = wd.Firefox(service=Service(GeckoDriverManager().install()), options=options)
            self.driver.maximize_window()  # Maximize the browser window
            self.window_handles = [self.driver.current_window_handle]  # Track open tabs
            self._initialized = True

            # Restore the browser state automatically
            self.restore_state()

            # Ensure state is saved when the browser is closed
            atexit.register(self.close_browser)
        except Exception as e:
            self.logger.error(e)

    def save_state(self, filename="browser_state.json"):
        """Save the state of the browser (tabs, cookies, localStorage, sessionStorage)."""
        if not hasattr(self, "driver") or self.driver.service.process is None:
            self.logger.warning("Browser is not running. Cannot save state.")
            return
        
        # Create the "browser_state" folder if it doesn't exist
        browser_state_folder = "browser_state"
        if not os.path.exists(browser_state_folder):
            os.makedirs(browser_state_folder)

        # Define file paths
        browser_state_path = os.path.join(browser_state_folder, filename)
        cookies_path = os.path.join(browser_state_folder, "cookies.json")
        local_storage_path = os.path.join(browser_state_folder, "local_storage.json")

        # Save the state
        state = {
            "tabs": [],
            "cookies": [],
            "local_storage": {},
            "session_storage": {},
        }

        # Save URLs of all open tabs
        for handle in self.window_handles:
            self.driver.switch_to.window(handle)
            if self.driver.current_url != "about:blank":  # Skip blank pages
                state["tabs"].append(self.driver.current_url)

        # Save cookies, localStorage, and sessionStorage for each valid tab
        for url in state["tabs"]:
            self.driver.get(url)  # Navigate to the URL to ensure the domain is active
            try:
                # Save cookies for the domain
                state["cookies"].extend(self.driver.get_cookies())

                # Save localStorage and sessionStorage
                state["local_storage"][url] = self.driver.execute_script("return JSON.stringify(window.localStorage);")
                state["session_storage"][url] = self.driver.execute_script("return JSON.stringify(window.sessionStorage);")
            except Exception as e:
                self.logger.warning(f"Error saving session details for {url}: {e}")

        # Save the state to files
        try:
            with open(browser_state_path, "w") as file:
                json.dump(state, file, indent=4)
            self.logger.info(f"Browser state saved to {browser_state_path}")

            # Save cookies separately
            with open(cookies_path, "w") as file:
                json.dump(state["cookies"], file, indent=4)
            self.logger.info(f"Cookies saved to {cookies_path}")

            # Save localStorage separately
            with open(local_storage_path, "w") as file:
                json.dump(state["local_storage"], file, indent=4)
            self.logger.info(f"LocalStorage saved to {local_storage_path}")
        except Exception as e:
            self.logger.warning(f"Error saving state files: {e}")

    def restore_state(self, filename="browser_state.json"):
        if not os.path.exists(filename):
            self.logger.warning(f"No state file found at {filename}")
            return

        with open(filename, "r") as file:
            state = json.load(file)

        # Open saved tabs
        for i, url in enumerate(state["tabs"]):
            if re.search(r"https?://([^/]+)/sorry", url): continue

            if i != 0: self.new_tab()
            try:
                self.driver.get(url)
                sleep(RESTORE_DELAY)
            except Exception as e:
                self.logger.error(f"Failed to open {url}: {e}")
                continue

            # Restore cookies for the domain
            for cookie in state["cookies"]:
                if cookie["domain"] in url:
                    try:
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        self.logger.warning(f"Error restoring cookie for {url}: {e}")

            # Restore localStorage and sessionStorage
            try:
                self.driver.execute_script(f"window.localStorage.clear(); Object.assign(window.localStorage, {state['local_storage'][url]});")
                sleep(RESTORE_DELAY)
                self.driver.execute_script(f"window.sessionStorage.clear(); Object.assign(window.sessionStorage, {state['session_storage'][url]});")
                sleep(RESTORE_DELAY)
            except Exception as e:
                self.logger.warning(f"Error restoring storage for {url}: {e}")

        self.logger.info(f"Browser state restored from {filename}")


    def close_browser(self):
        """Save the state and close the browser."""
        if hasattr(self, "driver"):
            try:
                # Check if the browser and WebDriver are still running
                if self.driver.service.process is not None and self.driver.service.process.poll() is None:
                    self.save_state()
            except Exception as e:
                self.logger.warning(f"Error saving state before closing browser: {e}")
            finally:
                # Close the browser
                try:
                    self.driver.quit()
                    self.logger.info("Browser closed")
                except Exception as e:
                    self.logger.warning(f"Error closing browser: {e}")
        else:
            self.logger.warning("Browser is already closed.")

    def open_url(self, url):
        try:
            self.driver.get(url)
            self.logger.info(f"Opened URL: {url}")
        except Exception as e:
            self.logger.error(f"Failed to open {url}: {e}")

    def search(self, term):
        try:
            # Wait for the search box to be present
            search_box = WebDriverWait(self.driver, 50).until(
                ec.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(term)
            search_box.send_keys(Keys.RETURN)
            self.logger.info(f"Searched for: {term}")
        except Exception as e:
            self.logger.warning(f"Error during search: {e}")

    def refresh_page(self):
        self.driver.refresh()
        self.logger.info("Page refreshed")

    def go_back(self):
        self.driver.back()
        self.logger.info("Navigated back")

    def go_forward(self):
        self.driver.forward()
        self.logger.info("Navigated forward")

    def new_tab(self):
        """Open a new tab in the same browser window."""
        self.driver.execute_script("window.open('');")  # Open a new tab
        self.window_handles = self.driver.window_handles  # Update the list of window handles
        self.driver.switch_to.window(self.window_handles[-1])  # Switch to the new tab
        self.logger.info("New tab opened")

    def switch_to_tab(self, index):
        """Switch to a specific tab by index."""
        if 0 <= index < len(self.window_handles):
            self.driver.switch_to.window(self.window_handles[index])
            self.logger.info(f"Switched to tab {index}")
        else:
            self.logger.warning("Invalid tab index")

    def close_tab(self, index=None):
        """Close the current tab or a specific tab by index."""
        if index is None:
            index = self.window_handles.index(self.driver.current_window_handle)
        if 0 <= index < len(self.window_handles):
            self.driver.switch_to.window(self.window_handles[index])
            self.driver.close()
            self.window_handles.pop(index)
            if self.window_handles:
                self.driver.switch_to.window(self.window_handles[-1])  # Switch to the last tab
            self.logger.info(f"Closed tab {index}")
        else:
            self.logger.warning("Invalid tab index")

    def scroll_down(self):
        self.driver.execute_script("window.scrollBy(0, 500);")  # Scroll down by 500 pixels
        self.logger.info("Scrolled down")

    def scroll_up(self):
        self.driver.execute_script("window.scrollBy(0, -500);")  # Scroll up by 500 pixels
        self.logger.info("Scrolled up")

    def click_element_by_text(self, text):
        try:
            element = self.driver.find_element(By.XPATH, f"//*[text()='{text}']")
            element.click()
            self.logger.info(f"Clicked element with text: {text}")
        except Exception as e:
            self.logger.warning(f"Error clicking element: {e}")

    def fill_form_field(self, field_name, value):
        try:
            field = self.driver.find_element(By.NAME, field_name)
            field.clear()
            field.send_keys(value)
            self.logger.info(f"Filled field '{field_name}' with '{value}'")
        except Exception as e:
            self.logger.warning(f"Error filling form field: {e}")

    def take_screenshot(self, filename="screenshot.png"):
        # Create the "screenshots" folder if it doesn't exist
        screenshots_folder = "screenshots"
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)

        # Generate a timestamped filename
        timestamp = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_{filename}"

        # Save the screenshot to the "screenshots" folder
        screenshot_path = os.path.join(screenshots_folder, filename)

        try:
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"Screenshot saved as {screenshot_path}")
        except Exception as e:
            self.logger.warning(f"Error taking screenshot: {e}")
        

    def play_video(self, query):
        request = self.youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            maxResults=1
        )
        response = request.execute()

        if 'items' not in response or len(response['items']) == 0:
            self.logger.warning("No videos found for the query:", query)
            return 
        
        video_id = response['items'][0]['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        self.logger.info("Opening YouTube video:", video_url)
        self.open_url(video_url)

    
    def play_song(self, query: str, in_browser=True):
        results = self.spotify.search(q=query, type='track', limit=1)

        if not results['tracks']['items']:
            self.logger.info("No track found for the query:", query)
            return 
        
        track = results['tracks']['items'][0]
        track_name = track['name']
        track_url = track['external_urls']['spotify']

        self.logger.info(f"Now playing (Spotify): {track_name}")

        if is_installed("spotify") and not in_browser:
            self.logger.info(f"Opening spotify in app. Playing track: {track_name}")
            self.spotify.start_playback(uris=[track['uri']])
        else:
            self.logger.info(f"Opening spotify in web browser. Playing track: {track_name}")
            self.open_url(track_url)




# Example usage
if __name__ == "__main__":
    from time import sleep

    # Create a singleton instance of BrowserController
    browser_manager = BrowserController(headless=False)

    # Open a URL
    browser_manager.open_url("https://www.google.com")

    # Save the browser state
    browser_manager.save_state()

    # Wait for a while
    sleep(30)

    # Close the browser
    browser_manager.close_browser()