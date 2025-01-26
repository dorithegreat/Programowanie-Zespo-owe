import configparser as cp
import subprocess as sp
import os
import platform
import psutil as ps
import shutil as sh
from computer_controller.log import get_logger


logger = get_logger(__name__)

'''OS''' 

def is_installed(app_names: list[str]) -> bool:
    """Check if the given application(s) are installed."""
    return True in [(sh.which(name) is not None) for name in app_names]


def is_running(app_name):
    """Check if the given application is currently running."""
    for process in ps.process_iter(['name']):
        if process.info['name'] and app_name in process.info['name'].lower():
            return True
    return False


def get_path(app_name: str) -> str:
    """Get the full path to the given application."""
    return sh.which(app_name)


def get_platform() -> str:
    """Get the current operating system."""
    return platform.system()


def open_program(app_name: str, args: list[str] = None):
    """
    Open a program if it is installed and not already running.
    
    :param app_name: The name of the program to open.
    :param args: Optional list of arguments to pass to the program.
    """
    if not is_installed([app_name]):
        logger.warning(f"Program '{app_name}' is not installed.")
        return False

    if is_running(app_name):
        logger.info(f"Program '{app_name}' is already running.")
        return True

    try:
        program_path = get_path(app_name)
        if not program_path:
            logger.warning(f"Could not find the path for '{app_name}'.")
            return False

        # Open the program with optional arguments
        if args:
            sp.Popen([program_path] + args)
        else:
            sp.Popen([program_path])

        logger.info(f"Successfully opened '{app_name}'.")
        return True
    except Exception as e:
        logger.error(f"Failed to open '{app_name}': {e}")
        return False


'''FIREFOX'''

def ff_create_profile(profile_name="selenium"):
    """Creates a new Firefox profile if it doesn't exist."""
    home_dir = os.path.expanduser("~")
    profiles_ini_path = os.path.join(home_dir, '.mozilla', 'firefox', 'profiles.ini')
    firefox_dir = os.path.dirname(profiles_ini_path)

    if not os.path.exists(profiles_ini_path):
        logger.warning("Profiles.ini file not found. Creating a new one.")
        os.makedirs(firefox_dir, exist_ok=True)
        open(profiles_ini_path, 'a').close()  # Create an empty profiles.ini file

    config = cp.ConfigParser()
    config.read(profiles_ini_path)

    # Check if the profile already exists
    for section in config.sections():
        if config[section].get("Name") == profile_name:
            profile_path = os.path.join(firefox_dir, config[section].get("Path"))
            logger.info(f"Profile '{profile_name}' already exists. Path: {profile_path}")
            return profile_path

    # Create a new profile
    profile_path = os.path.join(firefox_dir, profile_name)
    os.makedirs(profile_path, exist_ok=True)

    # Add the new profile to profiles.ini
    new_section = f"Profile{len(config.sections()) + 1}"
    config[new_section] = {
        "Name": profile_name,
        "Path": profile_name,
        "IsRelative": "1",
        "Default": "0"
    }

    with open(profiles_ini_path, 'w') as configfile:
        config.write(configfile)

    logger.info(f"Created new Firefox profile '{profile_name}'. Path: {profile_path}")
    return profile_path


def ff_get_profile_path(profile_name="selenium"):
    """Returns the path to the specified Firefox profile. Creates it if it doesn't exist."""
    if get_platform() == "Windows":
        profiles_ini_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'profiles.ini')
        firefox_dir = os.path.dirname(profiles_ini_path)
    elif get_platform() == "Linux":
        home_dir = os.path.expanduser("~")
        profiles_ini_path = os.path.join(home_dir, '.mozilla', 'firefox', 'profiles.ini')
        firefox_dir = os.path.dirname(profiles_ini_path)
    else:
        logger.warning("Firefox profile not found. Reason - Unhandled OS.")
        return None

    if not os.path.exists(profiles_ini_path):
        logger.warning("Profiles.ini file not found. Creating a new profile.")
        return ff_create_profile(profile_name)

    config = cp.ConfigParser()
    config.read(profiles_ini_path)

    # Check if the profile exists
    for section in config.sections():
        if config[section].get("Name") == profile_name:
            profile_path = os.path.join(firefox_dir, config[section].get("Path"))
            logger.info(f"Profile '{profile_name}' found. Path: {profile_path}")
            return profile_path

    # If the profile doesn't exist, create it
    return ff_create_profile(profile_name)