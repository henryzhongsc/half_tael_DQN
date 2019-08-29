###########################################################################################
# Trade_Interface config.

config_account_name = 'DQN_v3.0_trial_data_4c_1000_row'
config_currency_balance = {'USD': 100000, 'EUR': 100000, 'GBP': 100000, 'JPY': 100000}
# _currency_balance = {'USD': 0, 'EUR': 100000, 'GBP': 0, 'JPY': 0, 'AUD': 300} # Five currencies
config_from = "2018-04-13T18:30:00Z"
config_to = "2018-04-16T11:10:00Z" # 1000 rows
config_interval = "M1"

# _account_name = 'DQN_v3.0_trial_data_890_row'
# _currency_balance = {'USD': 0, 'EUR': 100000, 'GBP': 0}
# _from = "2018-04-13T18:30:00Z"
# _to = "2018-04-16T09:30:00Z" # 890 rows
# _interval = "M1"

###########################################################################################


# FX config.
config_base_currency = 'USD'
config_n_features = 300
config_anita_switch = True


# DQN config.
config_learning_rate = 0.01
config_reward_decay = 0.9
config_e_greedy = 0.9
config_replace_target_iter = 200
config_memory_size = 2000
config_output_graph = False


# run_model() config.
config_train_episode = 2
config_learn_threshold = 200
config_learn_interval = 5
config_base_currency = 'USD'
config_trade_log_mode = False
#False, 'TWOENDS', 'ALL'
config_trade_log_to_file = True
config_show_checkout = True
config_show_step = False