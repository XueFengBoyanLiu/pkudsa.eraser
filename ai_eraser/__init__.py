from os import path, makedirs
import sys
eraser_path = path.join(path.dirname(__file__), 'pkudsa.eraser', 'Code')
sys.path.append(eraser_path)
from interaction import *
import eraserconfig
import time
from functools import lru_cache
import json
from external._base import BasePairMatch
from external.factory import FactoryDeco
import traceback

# 比赛进程
@FactoryDeco(7)
class EraserMatch(BasePairMatch):
    class Meta(BasePairMatch.Meta):
        pass
        # required_functions = ['play']
        # module_whitelist=['random','numpy']
        # required_classes=['Player',['__init__','output']]

    @classmethod
    def pre_run(cls, d_local, d_global):
        '''
        初始化环境,返回cls.init_params参量,记录先后手顺序
        '''
        return 1
    
    def get_timeout(self):
        '''
        得到最大允许时长
        '''
        return self.params['rounds'] * (eraserconfig.MAX_TIME*2+0.2)#suppose a 400ms time limit
    
    @classmethod
    def run_once(cls, d_local, d_global):
        '''
        运行一局比赛
        并返回比赛记录对象record
        希望能够从Game_play中得到直接传出的比赛结果:
        {'winner': self.replay['winner'],
                'errorMessage': '',
                'errorStatus': self.replay['exitStatus'] - 1,
                'length': self.turn,
                'score': 1000,
                'reason': None}
        '''
        cls.init_params=1-cls.init_params
        if cls.init_params==0:
                cls.seed=int(time.time()*1000)
        play=Game_play(d_local['players'][0],d_local['players'][1],cls.init_params,cls.seed)
        play.start_game()
        return play.log_data
        # if cls.init_params[0]==0:    
        #     play=Game_runner(d_local['players'][0],d_local['players'][1])
        #     re, cls.init_params[1]=play.start_games()
        #     cls.init_params[0]=1
        #     re['order']=0
        #     log_name1 = path.join(d_local['match_dir'], '%02d.zlog' % d_local['rid'])
        #     log_name2 = path.join(d_local['match_dir'], '%02d.zlog' % (d_local['rid']+1))
        #     play.save_game_log(log_name1,log_name2)
        #     return re
        # else:
        #     re=cls.init_params[1]
        #     cls.init_params=[0,None]
        #     re['order']=1
        #     return re
        
    # @classmethod 
    # def swap_fields(cls,d_local,d_global):
    #     '''
    #     交换先后手比赛
    #     '''
        
    #     pass
    @classmethod
    def output_queue(cls, match_log):
        '''
        读取比赛记录:此处传入参量来自run_once或者runner_fail_log
        返回比赛结果元组
        '''
        
        return (match_log['winner'],match_log['score'],match_log['errorMessage'])
    
    @classmethod
    def runner_fail_log(cls, winner, descrip, d_local, d_global):
        ''' 内核错误 '''
        descrip = [cls.stringfy_error(e) for e in descrip]
        if winner != None:
            descrip = descrip[1 - winner]
        order=1-cls.init_params
        faillog={
            'order': order,
            'names': d_local['names'],
            'winner': winner,
            'errorMessage': descrip,
            'score': 1000,
            'length':0,
            'reason':None,
            'errorstatus':True
        }
        return faillog

    @classmethod
    def get_winner(cls, record):
        ''' 判断胜者 ,以初始的code1胜利为0'''
        return record['winner']