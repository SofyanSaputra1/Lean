configs = {
  "target_crypto": "ETHUSD",
  "indicator_name": "bollinger",
  "warmup_lookback": 30,
  "time_resolution": Resolution.Minute,
  "resubmit_order_threshold": .01,
  "bar_size": 5,
  "moving_average_type": MovingAverageType.Exponential,
  "bollinger_period": 20,
  "k": 2,
  "momentum_period": 5,
  "momentum_buy_threshold": 2,
  "momentum_sell_threshold": 0,
  "MACD_fast_period": 12,
  "MACD_slow_period": 26,
  "MACD_signal_period": 9,
  "MACD_moving_average_type": MovingAverageType.Exponential,
  "MACD_tolerance": 0.0025,
  "tenkanPeriod": 9,
  "kijunPeriod": 26,
  "senkouAPeriod": 26,
  "senkouBPeriod": 52,
  "senkouADelayedPeriod": 26,
  "senkouBDelayedPeriod": 26,
  "rsi_period": 14,
  "rsi_moving_average_type": MovingAverageType.Wilders,
  "rsi_lower": 30,
  "rsi_upper": 70,
  "volume_min": 100
}