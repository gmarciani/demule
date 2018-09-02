"""
MARKOV ANALYSIS: Generate the Markov Chain model of the system, according to settings in 'markov_analysis.yaml'
Results are stored in 'out/markov_analysis' and can be visualized running the Matlab Live Script 'pmcsn.mlx'
"""

from core.simulation.model.config import load_configuration
from core.utils.logutils import ConsoleHandler
from core.simulation.model.scope import TaskScope
from core.utils import markovutils
from core.utils import file_utils
import logging
import os


# Configure logger
logging.basicConfig(level=logging.INFO, handlers=[ConsoleHandler(logging.INFO)])
logger = logging.getLogger(__name__)

# Configuration
CONFIG_PATH = "markov_analysis.yaml"

# Results
OUTDIR = "out/markov_analysis"


def run(config_path=CONFIG_PATH):
    """
    Execute the experiment.
    :param config_path: (string) the path of the configuration file.
    :return: None
    """
    config = load_configuration(config_path, norm=False)

    clt_n_servers = config["system"]["cloudlet"]["n_servers"]
    clt_threshold = config["system"]["cloudlet"]["threshold"]
    arrival_1 = config["arrival"][TaskScope.TASK_1.name]["parameters"]["r"]
    arrival_2 = config["arrival"][TaskScope.TASK_2.name]["parameters"]["r"]
    clt_service_1 = config["system"]["cloudlet"]["service"][TaskScope.TASK_1.name]["parameters"]["r"]
    clt_service_2 = config["system"]["cloudlet"]["service"][TaskScope.TASK_2.name]["parameters"]["r"]

    logger.info("Launching Markov Chain generation with clt_n_servers={}, clt_threshold={}, arrival_1={}, arrival_2={}, clt_service_1={}, clt_service_2={}".format(
        clt_n_servers, clt_threshold, arrival_1, arrival_2, clt_service_1, clt_service_2
    ))

    MC = markovutils.generate_markov_chain(clt_n_servers, clt_threshold, arrival_1, arrival_2, clt_service_1, clt_service_2)
    M, S = MC.transition_matrix()

    outdir = OUTDIR
    tmatrix_file_csv = os.path.join(outdir, "transition_matrix.csv")
    states_file_csv = os.path.join(outdir, "states.csv")

    str_tmatrix = markovutils.matrixs(M)
    str_states = "state\n" + "\n".join(map(markovutils.MarkovState.pretty_str,S))

    file_utils.save_txt(str_tmatrix, tmatrix_file_csv, append=True, empty=True)
    file_utils.save_txt(str_states, states_file_csv, append=True, empty=True)


if __name__ == "__main__":
    run()