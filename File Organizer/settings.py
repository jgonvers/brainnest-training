import logging

log_level = logging.INFO
logging.basicConfig(
    encoding="utf-8",
    level=log_level,
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
)
logger = logging.getLogger("settings")
