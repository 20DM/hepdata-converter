import yaml
from hepdata_converter.parsers import Parser, ParsedData, Table
import os


class YAML(Parser):
    def __init__(self, *args, **kwargs):
        super(YAML, self).__init__(*args, **kwargs)

    def parse(self, data_in, *args, **kwargs):
        """

        :param data_in: path to submission.yaml
        :param args:
        :param kwargs:
        :raise ValueError:
        """
        if not os.path.exists(data_in):
            raise ValueError("File does not exist: %s" % data_in)

        with open(data_in, 'r') as submission_file:
            submission_data = list(yaml.load_all(submission_file))

        if len(submission_data) == 0:
            raise RuntimeError("Submission file (%s) is empty" % data_in)

        tables = []

        for i in range(1, len(submission_data)):
            table_filepath = os.path.join(os.path.dirname(data_in), submission_data[i]['data_file'])
            if not os.path.exists(table_filepath):
                raise ValueError("table file: %s does not exist" % table.data_file)

            with open(table_filepath, 'r') as table_file:
                table_data = yaml.load(table_file)

            table = Table(index=i, metadata=submission_data[i], data=table_data)
            tables.append(table)

        return ParsedData(submission_data[0], tables)
