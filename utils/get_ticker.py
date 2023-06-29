import pandas as pd

hose_path = 'data/tickers/hose_tickers.csv'
hnx_path = 'data/tickers/hnx_tickers.csv'
uc_path = 'data/tickers/uc_tickers.csv'

result = ''

def get_ticker(get_market=False):
    """
        Trả về mã cổ phiếu của 3 sàn chứng khoán (HoSE, HNX, UpCOM)
        Parameter:
            get_market: True thì Kết quả sẽ trả về mã chứng khoán và sàn chứng khoán ứng với mã chứng khoán đó
                        False thì chỉ trả về mã chứng khoán
    """
    hose_ticker = pd.read_csv(hose_path)['Stock Code']
    hnx_ticker = pd.read_csv(hnx_path)['Stock Code']
    uc_ticker = pd.read_csv(uc_path)['Stock Code']
    # print(len(hose_ticker))
    tickers = [*hose_ticker, *hnx_ticker, *uc_ticker]
    if get_market:
        market = ['HoSe'] * len(hose_ticker) + ['HNX'] * len(hnx_ticker) + ['UpCOM'] * len(uc_ticker)
        return tickers, market
    else:
        return tickers