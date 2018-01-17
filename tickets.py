# coding: utf-8
"""Train tickets query via command-line.

Usage:
   tickets [-gdtkz] <from> <to> <date>

Options:
   -h,--help   显示帮助菜单
   -g          高铁
   -d          动车
   -t           特快
   -k          快速
   -z          直达

Example:
   tickets 上海 北京 2017-12-05
"""
from docopt import docopt
from stations import station1, station2
import requests
from prettytable import PrettyTable
from termcolor import colored


class TrainCollection(object):
    # 显示车次、出发/到达站、 出发/到达时间、历时、商务特等座、一等座、二等座、高级软卧、软卧、动卧、硬卧、软座、硬座、无座、其他、备注
    header = '车次、出发/到达站、 出发/到达时间、历时、商务特等座、一等座、二等座、高级软卧、软卧、动卧、硬卧、软座、硬座、无座、其他、备注'.split('、')

    def __init__(self,rows):
        self.rows = rows

    @property
    def trains(self):
        for row in self.rows:
            trainrow = row.split('|')
            # 用字典station2转换
            trainrow[6] = station2[trainrow[6]]
            trainrow[7] = station2[trainrow[7]]
            trainrow[10] = trainrow[10].replace(':', 'h ') + 'min'
            train=[
                #车次
                trainrow[3],
                #出发/到达站   出发车站和时间设置为黄色
                '\n'.join([colored(trainrow[6], "yellow"), colored(trainrow[7],'green')]),
                #出发/到达时间 到达车站和时间设置为绿色
                '\n'.join([colored(trainrow[8], 'yellow'), colored(trainrow[9],'green')]),
                #历时
                trainrow[10]
             ]
                #商务特等座~无座
            train.extend(list(trainrow[32:21:-1]))
            #备注
            train.append(colored(trainrow[1], "red"))
            yield train

    def pretty_print(self):
        """
        `prettytable`这个库可以提取的信息像MySQL数据库那样格式化显示

        """

        pt = PrettyTable()
        #设置每一列得标题
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


def cli():

    """command-line interface"""
    arguments = docopt(__doc__)
    print(arguments['<date>'], arguments['<from>'], arguments['<to>'])
    #用字典station1转换
    from_station=station1[arguments['<from>']]
    to_station = station1[arguments['<to>']]
    date = arguments['<date>']
    #构建url
    url='https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,from_station,to_station)
    r = requests.get(url)
    re = r.json()
    #获取有效数据
    rows = re['data']['result']
    # print(rows)
    trains = TrainCollection(rows)
    trains.pretty_print()





if __name__ == '__main__':
    cli()