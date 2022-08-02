import os
from macd_strategy import SimpleMACD
from autotrader.autotrader import AutoTrader

def test_macd_backtest():
    config = {'NAME': 'MACD Strategy',
              'MODULE': 'macd_strategy',
              'CLASS': 'SimpleMACD',
              'INTERVAL': 'H4',
              'PERIOD': 300,
              'RISK_PC': 1.5,
              'SIZING': 'risk',
              'PARAMETERS': {'ema_period': 200,
                             'MACD_fast': 5,
                             'MACD_slow': 19,
                             'MACD_smoothing': 9,
                             'RR': 1.5},
              'WATCHLIST': ['EUR_USD'],}
    home_dir = os.path.abspath(os.path.dirname(__file__))
    
    at = AutoTrader()
    at.configure(verbosity=1, show_plot=False)
    at.add_strategy(config_dict=config, strategy=SimpleMACD)
    at.plot_settings(show_cancelled=True)
    at.add_data({'EUR_USD': 'EUR_USD_H4.csv'}, 
                data_directory=os.path.join(home_dir, 'data'))
    at.backtest(start = '1/1/2021', end = '1/1/2022')
    at.virtual_account_config(initial_balance=1000, leverage=30,
                spread=0.5*1e-4, commission=0.005, hedging=True)
    at.run()
    bot = at.get_bots_deployed()
    bt_results = at.trade_results.summary()
    
    # Test backtest results
    assert bt_results['no_trades'] == 35, "Incorrect number of trades " + \
        "(single instrument backtest)"
    assert round(bt_results['ending_balance'], 3) == 922.059, "Incorrect "+\
        "ending balance (single instrument backtest)"
    assert bt_results['long_trades']['no_trades'] == 10, "Incorrect number "+\
        "of long trades (single instrument backtest)"
    assert bt_results['short_trades']['no_trades'] == 25, "Incorrect number "+\
        "of short trades (single instrument backtest)"


def test_multibot_macd_backtest():
    config = {'NAME': 'MACD Strategy',
              'MODULE': 'macd_strategy',
              'CLASS': 'SimpleMACD',
              'INTERVAL': 'H4',
              'PERIOD': 300,
              'RISK_PC': 1.5,
              'SIZING': 'risk',
              'PARAMETERS': {'ema_period': 200,
                              'MACD_fast': 5,
                              'MACD_slow': 19,
                              'MACD_smoothing': 9,
                              'RR': 1.5},
              'WATCHLIST': ['EUR_USD', 'EUR_USD2'],}
    home_dir = os.path.abspath(os.path.dirname(__file__))
    
    at = AutoTrader()
    at.configure(verbosity=0, show_plot=False)
    at.add_strategy(config_dict=config, strategy=SimpleMACD)
    at.plot_settings(show_cancelled=False)
    at.add_data({'EUR_USD': 'EUR_USD_H4.csv',
                  'EUR_USD2': 'EUR_USD_H4.csv'}, 
                data_directory=os.path.join(home_dir, 'data'))
    at.backtest(start = '1/1/2021', end = '1/1/2022')
    at.virtual_account_config(initial_balance=1000, leverage=30,
                spread=0.5*1e-4, commission=0.005, hedging=True)
    at.run()
    bt_results = at.trade_results.summary()
    
    assert bt_results['no_trades'] == 66, "Incorrect number of trades"+\
        " (multi-instrument backtest)"
    assert round(bt_results['ending_balance'], 3) == 838.269, "Incorrect "+\
        "ending balance (multi-instrument backtest)"
    assert bt_results['long_trades']['no_trades'] == 18, "Incorrect number "+\
        "of long trades (multi-instrument backtest)"
    assert bt_results['short_trades']['no_trades'] == 48, "Incorrect number "+\
        "of short trades (multi-instrument backtest)"
        
test_macd_backtest()