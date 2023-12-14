import logging
import os
import sys
from datetime import datetime
from from_root import from_root

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(from_root(), "logs", log_file)

os.makedirs(logs_path, exist_ok=True)

log_file_path = os.path.join(logs_path, log_file)

logging.basicConfig(
    # filename=LOG_FILE_PATH,
    format=logging_str,
    level=logging.INFO,

    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("cnnClassifierLogger")