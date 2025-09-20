import time
import logging
import json
import os
import atexit

from ACController import ACController
from Bot import TelegramBot

# Configure logging
def setup_logging(config=None):
    """Setup logging configuration with file and console output"""
    # Default logging config
    log_config = {
        "level": "INFO",
        "keep_console_output": True,
        "max_log_files": 7
    }
    
    # Update with user config if provided
    if config and "logging" in config:
        log_config.update(config["logging"])
    
    log_filename = f"ac_controller_{time.strftime('%Y%m%d')}.log"
    
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_filepath = os.path.join(logs_dir, log_filename)
    
    # Clean up old log files if max_log_files is set
    if log_config["max_log_files"] > 0:
        cleanup_old_logs(logs_dir, log_config["max_log_files"])
    
    # Configure handlers
    handlers = [logging.FileHandler(log_filepath, encoding='utf-8')]
    
    # Configure logging with both file and console handlers
    logging.basicConfig(
        level=getattr(logging, log_config["level"].upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers,
        force=True  # Override any existing configuration
    )
    
    # Create logger instance
    logger = logging.getLogger('ACController')
    logger.info(f"Logging initialized. Log file: {log_filepath}")
    logger.info(f"Log level: {log_config['level']}, Console output: {log_config['keep_console_output']}")
    return logger

def cleanup_old_logs(logs_dir, max_files):
    """Remove old log files, keeping only the most recent max_files"""
    try:
        log_files = []
        for filename in os.listdir(logs_dir):
            if filename.startswith("ac_controller_") and filename.endswith(".log"):
                filepath = os.path.join(logs_dir, filename)
                log_files.append((filepath, os.path.getctime(filepath)))
        
        # Sort by creation time (newest first)
        log_files.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old files
        for filepath, _ in log_files[max_files:]:
            try:
                os.remove(filepath)
                print(f"Removed old log file: {filepath}")
            except Exception as e:
                print(f"Error removing log file {filepath}: {e}")
                
    except Exception as e:
        print(f"Error cleaning up old logs: {e}")

def check_log_file_exists():
    """Check if a log file exists for today"""
    logs_dir = "logs"
    log_filename = f"ac_controller_{time.strftime('%Y%m%d')}.log"
    log_filepath = os.path.join(logs_dir, log_filename)
    return os.path.exists(log_filepath)

# Initialize logger (will be properly configured later in main)
logger = None

def load_config():
    """Load configuration from config.json"""
    config_file = "config.json"
    
    default_config = {
        "bot_token": "YOUR_BOT_TOKEN_HERE",
        "auto_start_enabled": False,
        "default_interval_minutes": 10,
        "logging": {
            "level": "INFO",
            "keep_console_output": True,
            "max_log_files": 7
        }
    }
    
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        print(f"Created {config_file}. Please add your bot token and restart the script.")
        return None
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        if config.get("bot_token") == "YOUR_BOT_TOKEN_HERE":
            print("Please update your bot token in config.json")
            return None
            
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None


def main():
    """Main function"""
    # Load config first to get logging preferences
    config = load_config()
    if not config:
        return
    
    # Setup logging with config preferences
    setup_logging(config)
    
    # Now we can use loggers safely
    config_logger = logging.getLogger('Config')
    config_logger.info("Configuration loaded successfully")
    
    main_logger = logging.getLogger('Main')
    main_logger.info("=== AC Controller Bot Starting ===")
    
    # Initialize AC controller
    main_logger.info("Initializing AC Controller...")
    ac_controller = ACController()
    
    # Start auto-toggle if enabled in config
    if config.get("auto_start_enabled", False):
        interval = config.get("default_interval_minutes", 10) * 60
        main_logger.info(f"Auto-start enabled with {config.get('default_interval_minutes', 10)} minute interval")
        ac_controller.start_auto_toggle(interval)
    
    # Initialize and start Telegram bot
    main_logger.info("Initializing Telegram Bot...")
    bot = TelegramBot(ac_controller, config["bot_token"])
    try:
        bot.run()
    except KeyboardInterrupt:
        main_logger.info("Received keyboard interrupt, shutting down...")
        ac_controller.on_exit()  # Add parentheses to actually call the function
        print("\nShutting down...")
    except Exception as e:
        main_logger.error(f"Bot error: {e}")
        print(f"Bot error: {e}")
    finally:
        main_logger.info("=== AC Controller Bot Stopped ===")


if __name__ == "__main__":
    main()

