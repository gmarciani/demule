import copy

default_configuration = {

    "general": {
        "n_batch": 1,  # the number of batches
        "t_batch": 1000,  # the stop time for a batch (s)
        "confidence": 0.95,  # the confidence level for the statistics
        "random": {
            "generator": "MarcianiMultiStream",  # the class name of the random generator
            "seed": 123456789  # the initial seed for the random generator
        }
    },

    "tasks": {
        "arrival_rate_1": 3.25,  # the arrival rate for tasks of type 1 (tasks/s)
        "arrival_rate_2": 6.25  # the arrival rate for tasks of type 2 (tasks/s)
    },

    "system": {
        "cloudlet": {
            "service_rate_1": 0.45,  # the service rate for tasks of type 1 (tasks/s)
            "service_rate_2": 0.30,  # the service rate for tasks of type 2 (tasks/s)
            "n_servers": 20,  # the number of servers
            "threshold": 20,  # the occupancy threshold
            "server_selection": "ORDER"  # the server-selection rule
        },

        "cloud": {
            "service_rate_1": 0.25,  # the service rate for job of type 1 (tasks/s).
            "service_rate_2": 0.22,  # the service rate for job of type 2 (tasks/s).
            "t_setup_mean": 0.8  # the mean setup time to restart a task of type 2 in the Cloud (s).
        }
    }
}


def get_default_configuration():
    """
    Get a copy of default configuration.
    :return: a copy of default configuration.
    """
    return copy.deepcopy(default_configuration)


if __name__ == "__main__":
    # Creation
    config_1 = get_default_configuration()
    config_2 = get_default_configuration()

    # Equality check
    print("Config 1 equals Config 2 (before editing): {}".format(config_1 == config_2))
    config_2["general"]["t_stop"] = 25000
    print("Config 1 equals Config 2 (after editing): {}".format(config_1 == config_2))

