"""
TRANSIENT ANALYSIS: Evaluate the system transient phase, according to settings in 'config.yaml'
Results are stored in 'result.csv' and can be visualized running the Matlab script 'result.m'
"""

from core.simulation.simulation import Simulation as Simulation
from core.simulation.config.configuration import load_configuration
from core.utils.logutils import ConsoleHandler
import logging


# Configure logger
logging.basicConfig(level=logging.INFO, handlers=[ConsoleHandler(logging.INFO)])
logger = logging.getLogger(__name__)

# Configuration
CONFIG_PATH = "config.yaml"
RESULT_PATH = "result.csv"


if __name__ == "__main__":
    config = config = load_configuration(CONFIG_PATH)

    header_saved = False

    logger.info("Launching transient analysis with n_batch={}, t_batch={}, i_batch={}".format(
        config["general"]["n_batch"],
        config["general"]["t_batch"],
        config["general"]["i_batch"]))

    simulation = Simulation(config, "SIMULATION-TRANSIENT-ANALYSIS")
    simulation.run()
    simulation.statistics.save_csv(RESULT_PATH, skip_header=header_saved)
    header_saved = True