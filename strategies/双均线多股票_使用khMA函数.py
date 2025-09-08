# coding: utf-8
# 策略说明：
# - 策略名称：双均线多股票（使用 khMA）
# - 功能：对股票池内每只股票，比较当日 khMA5 与 khMA20；khMA5>khMA20 买入，khMA5<khMA20 卖出
# - 指标来源：使用 khQTTools 中的 khMA（内部封装的行情获取 + 移动平均）
# - 与使用 MyTT.MA 的版本区别：khMA 中内置了行情获取 + 移动平均，更加方便，MyTT.MA 需要在策略文档中先拉取历史行情再计算
from khQuantImport import *  # 导入所有量化工具

def init(stocks=None, data=None):  # 策略初始化函数
    """本策略不需初始化"""

def khHandlebar(data: Dict) -> List[Dict]:  # 主策略函数
    """策略主逻辑，支持多只股票的双均线策略"""
    signals = []  # 初始化信号列表
    stock_list = khGet(data, "stocks")  # 获取股票池列表
    current_date_str = khGet(data, "date_num")  # 获取当前日期数字格式

    for stock_code in stock_list:  # 遍历每只股票
        current_price = khPrice(data, stock_code, "open")  # 获取当前开盘价
        ma_short = khMA(stock_code, 5, end_time=current_date_str)  # 计算5日均线
        ma_long = khMA(stock_code, 20, end_time=current_date_str)  # 计算20日均线
            
        has_position = khHas(data, stock_code)  # 检查是否持有该股票
        
        if ma_short > ma_long and not has_position:  # 金叉且无持仓
            signals.extend(generate_signal(data, stock_code, current_price, 0.5, 'buy', f"{stock_code[:6]} 金叉买入"))  # 单股票20%仓位
            
        elif ma_short < ma_long and has_position:  # 死叉且有持仓
            signals.extend(generate_signal(data, stock_code, current_price, 1, 'sell', f"{stock_code[:6]} 死叉卖出"))  # 全部卖出
    
    return signals  # 返回交易信号

# khPreMarket 和 khPostMarket 函数省略，本次策略未使用 