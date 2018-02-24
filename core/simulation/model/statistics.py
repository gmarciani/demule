from core.statistics.batch_means import BatchedSampleStatistic, BatchedMeasure
from core.statistics.batch_means import BatchedSamplePathStatistic
from core.utils.csv_utils import save


class BatchStatistics:
    """
    The set of statistics for the simulation.
    """

    def __init__(self):
        """
        Create a new set of statistics.
        """

        # Measures
        self.arrived = BatchedMeasure()
        self.completed = BatchedMeasure()
        self.switched = BatchedMeasure()
        self.service = BatchedMeasure()

        # Sample Statistics
        self.n = BatchedSampleStatistic()
        self.response = BatchedSampleStatistic()

        # Sample Path Statistics
        self.throughput = BatchedSamplePathStatistic()

        # Batch management
        self.n_batches = 0

    def register_batch(self):
        """
        Register and close the current batch statistics.
        :return: None
        """
        self.arrived.register_batch()
        self.completed.register_batch()
        self.switched.register_batch()
        self.service.register_batch()

        self.n.register_batch()
        self.response.register_batch()
        self.throughput.register_batch()

        self.n_batches += 1

    def discard_batch(self):
        """
        Discard the current batch statistics.
        :return: None
        """
        self.arrived.discard_batch()
        self.completed.discard_batch()
        self.switched.discard_batch()
        self.service.discard_batch()

        self.n.discard_batch()
        self.response.discard_batch()
        self.throughput.discard_batch()

    def save_csv(self, filename, skip_header=False, append=False):
        """
        Save the current statistics as CSV.
        :param filename: (string) the filename.
        :param skip_header: (bool) if True, skip the CSV header.
        :param append: (bool) if True, append to an existing file.
        :return: None
        """
        header = ["batch", "arrived", "completed", "switched", "service", "n", "response", "throughput"]
        data = []
        for b in range(self.n_batches):
            sample = [
                b,
                self.arrived.get_value(b),
                self.completed.get_value(b),
                self.switched.get_value(b),
                self.service.get_value(b),
                self.n.get_value(b),
                self.response.get_value(b),
                self.throughput.get_value(b)
            ]
            data.append(sample)
        save(filename, header, data, skip_header, append)