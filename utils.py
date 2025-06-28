import logging

def setup_logger():
    """Set up a basic logger"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('job_auto_apply')
    return logger

# We can add more utility functions as needed
