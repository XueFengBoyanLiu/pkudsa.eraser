from os import path, makedirs
import sys
eraser_path = path.join(path.dirname(__file__), 'pkudsa.eraser', 'Code')
sys.path.append(eraser_path)
from interaction import Game_play
import config

#from functools import lru_cache
import json
from .._base import BasePairMatch
from ..factory import FactoryDeco
# 比赛进程
@FactoryDeco(0)
class EraserMatch(BasePairMatch):
    class Meta(BasePairMatch.Meta):
        required_functions = ['play']
    @classmethod
    def pre_run(self):
        '''
        初始化环境，返回cls.init_params参量，记录先后手顺序
        '''
        return {'order':0,'boardStorage':None}
    
    @classmethod
    def get_timeout(self):
        '''
        得到最大允许时长
        '''
        return self.params['rounds'] * (config.MAX_TIME*2+0.2)#suppose a 400ms time limit
    @classmethod

    def run_once(cls, d_local, d_global):
        '''
        运行一局比赛
        并返回比赛记录对象record
        希望能够从Game_play中得到直接传出的比赛结果
        '''
        
        play=Game_play(d_local['players'][0],d_local['players'][1],d_local['names'],swapped=cls.init_params['order'])
        play.perform_turn()
        play.start_game()
        filename = 'replay.json'
        with open(filename, 'w') as f:
            replay=json.loads(f)
        
        return {'order':None,'winner':replay['winner'],'scores':replay['scores'],'Errormessage':replay['errorMessage']}
    @classmethod 
    def swap_fields(cls,d_local,d_global):
        '''
        交换先后手比赛
        '''
        cls.init_params
        if cls.init_params['order']==1:
            cls.init_params['boardStorage']=None
        cls.init_params['order']=1-cls.init_params['order']
        return
    @classmethod
    def output_queue(cls, match_log):
        '''
        读取比赛记录:此处传入参量来自run_once或者runner_fail_log
        返回比赛结果元组
        '''
        
        return tuple(match_log['winner'],match_log['scores'],match_log['Errormessage'])

    @classmethod
    def runner_fail_log(cls, winner, descrip, d_local, d_global):
        ''' 内核错误 '''
        descrip = [cls.stringfy_error(e) for e in descrip]
        if winner != None:
            descrip = descrip[1 - winner]
        faillog={
            'order': None,
            'names': d_local['names'],
            'winner': winner,
            'Errormessage': descrip,
            'scores': 0,
        }
        return faillog

    @classmethod
    def get_winner(cls, record):
        ''' 判断胜者 ,以初始的code1胜利为0'''
        winner=record['winner']
        if record['order']==1:
            winner=1-winner
        return winner