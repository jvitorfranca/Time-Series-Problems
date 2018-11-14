import featuretools as ft
import pandas as pd
import utilities as ut


data_path = 'data/train_FD004.txt'

dataset = ut.load_data(data_path)

cutoff_times = ut.make_cutoff_times(dataset)

es = ft.EntitySet('Dataset')

es = es.entity_from_dataframe(entity_id='recordings',
                              dataframe=dataset,
                              index='index',
                              time_index='time')

es = es.normalize_entity(base_entity_id='recordings',
                         new_entity_id='engines',
                         index='engine_no')

es = es.normalize_entity(base_entity_id='recordings',
                         new_entity_id='cycles',
                         index='time_in_cycles')

features_matrix, features_defs = ft.dfs(entityset=es,
                                        target_entity='engines',
                                        agg_primitives=['sum', 'min', 'max', 'mode', 'mean'],
                                        cutoff_time=cutoff_times,
                                        verbose=True,
                                        max_depth=3)

targets = features_matrix.pop('RUL')
