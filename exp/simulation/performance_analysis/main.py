"""
PERFORMANCE ANALYSIS: Evaluate the system performance, according to settings in 'config.yaml'
Results are stored in 'result.csv' and can be visualized running the Matlab script 'result.m'
"""

from core.simulation.simulation import Simulation as Simulation
from core.simulation.config.configuration import load_configuration
from core.utils.logutils import ConsoleHandler
import os
import logging


# Configure logger
logging.basicConfig(level=logging.INFO, handlers=[ConsoleHandler(logging.INFO)])
logger = logging.getLogger(__name__)

# Configuration
CONFIG_PATH = "config.yaml"

# Results
OUTDIR = "out"

# Parameters
THRESHOLDS = range(20, 21, 1)
THRESHOLD_FOR_DISTRIBUTION = 20


def run(config_path=CONFIG_PATH):
    """
    Execute the experiment.
    :param config_path: (string) the path of the configuration file.
    :return: None
    """
    config = load_configuration(config_path)

    simulation_counter = 0
    simulation_max = len(THRESHOLDS)

    logger.info("Launching performance analysis with t_stop={}, t_tran={}, n_batch={}, thresholds={}".format(
        config["general"]["t_stop"],
        config["general"]["t_tran"],
        config["general"]["n_batch"],
        THRESHOLDS
    ))

    for threshold in THRESHOLDS:
        simulation_counter += 1
        config["system"]["cloudlet"]["threshold"] = threshold
        logger.info("Simulating {}/{} with threshold {}".format(simulation_counter, simulation_max, threshold))
        outdir = "{}/{}".format(OUTDIR, threshold) if threshold == THRESHOLD_FOR_DISTRIBUTION else None
        simulation = Simulation(config, "SIMULATION-THRESHOLD-{}".format(threshold))
        simulation.run(outdir=outdir, show_progress=True)
        reportfilecsv = os.path.join(OUTDIR, "result.csv")
        reportfiletxt = os.path.join(OUTDIR, "result.txt")
        report = simulation.generate_report()
        report.save_csv(reportfilecsv, append=(simulation_counter > 1))
        report.save_txt(reportfiletxt, append=(simulation_counter > 1))


if __name__ == "__main__":
    run()