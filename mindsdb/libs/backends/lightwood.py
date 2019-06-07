from mindsdb.libs.constants.mindsdb import *

import lighwood


class LightwoodBackend():

    def __init__(self, transaction):
        self.transaction = transaction

    def _create_lightwood_config(self):
        config = {}

        config['name'] = self.transaction.lmd['name']

        config['input_features'] = []
        config['output_features'] = []

        for col_name in self.transaction.input_data.columns:
            if col in self.transaction.lmd['malformed_columns']['names']:
                continue

            col_stats = self.transaction.lmd['column_stats'][col_name]
            data_subtype = col_stats['data_subtype']
            data_type = col_stats['data_type']

            ludwig_data_type = None

            if data_type in (DATA_TYPES.NUMERIC):
                ludwig_data_type = 'numeric'

            elif data_type in (DATA_TYPES.CATEGORICAL):
                ludwig_data_type = 'categorical'

            elif data_type in (DATA_TYPES.DATE):
                ludwig_data_type = 'datetime'

            elif data_subtype in (DATA_SUBTYPES.IMAGE):
                ludwig_data_type = 'image'

            elif data_subtype in (DATA_SUBTYPES.TEXT):
                ludwig_data_type = 'text'

            # @TODO Handle lightwood's time_series data type

            else:
                self.transaction.log.error(f'The lightwood model backend is unable to handle data of type {data_type} and subtype {data_subtype} !')
                raise Exception('Failed to build data definition for Lightwood model backend')

            if col not in self.transaction.lmd['predict_columns']:
                config['input_features'].append({
                    'name': col_name
                    'tpye': ludwig_data_type
                })
            else:
                config['output_features'].append({
                    'name': col_name
                    'tpye': ludwig_data_type
                })

    def train(self):
        pass

    def predict(self, mode='predict', ignore_columns=[]):
        pass