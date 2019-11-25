###########################################################################################
# trade_interface config.

# config_account_name = 'DQN_v3.0_4c_55_month'
# config_currency_balance = {'USD': 100000, 'EUR': 100000, 'GBP': 100000, 'JPY': 100000}
# config_from = "2015-01-01T00:00:00Z"
# config_to = "2019-08-01T00:00:00Z" # 1202 rows
# config_interval = "D"


config_account_name = 'DQN_v3.0_4c_1000_row'
config_currency_balance = {'USD': 100000, 'EUR': 100000, 'GBP': 100000, 'JPY': 100000}
config_from = "2018-04-13T18:30:00Z"
config_to = "2018-04-16T11:10:00Z" # 1000 rows
config_interval = "M1"


config_output_arena_csv = True
config_output_raw_csv = False

###########################################################################################


# FX_env config.
config_base_currency = 'USD'
config_n_features = 300
config_anita_switch = False


# RL_brain config.
config_learning_rate = 0.01
config_reward_decay = 0.9
config_e_greedy = 0.9
config_replace_target_iter = 100
config_memory_size = 2000
config_output_graph = False


# model_interface config.
config_train_episode = 2
config_learn_threshold = 200
config_learn_interval = 5
config_base_currency = 'USD'
config_trade_log_mode = 'TWOENDS'
#False, 'TWOENDS', 'ALL'
config_trade_log_raw = False
config_trade_log_to_file = True
config_show_checkout = True
config_show_step = False