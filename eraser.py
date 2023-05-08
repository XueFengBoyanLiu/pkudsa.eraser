from external.tag_loader import RecordBase, RecordDeco


@RecordDeco(7)
class EraserRecord(RecordBase):
    def i_holder(_, match, record):
        # try:
        return record['order']
        # except Exception:
        #     pass
        #     with open("/home/lab409/django_ai_arena/eraser-log/log.txt", "a") as f:
        #         f.write("Keyerror: record is %s\n" % record)
    def i_winner(_, match, record):
        
        if record['order']==0:
            return record['winner']
        else:
            if record['winner']==None:
                return None
            else:
                return 1-record['winner']
    def r_length(_, match, record):
        return record['length']

    def r_win_desc(_, match, record):
        return record['reason'] 

    def r_desc_plus(_, match, record):
        return  record['score']