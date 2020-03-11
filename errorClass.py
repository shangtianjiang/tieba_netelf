import netelf_file
import conf
import traceback
class no_data(RuntimeError):
    def __init__(self,val):
        self.val = val
    def __str__(self):
        return repr(self.val)


def write_logs(text_logs,log_type):
    netelf_file.save_text_logs(text_logs,conf.read_conf('netelf_logs','./netelf_logs_'),log_type)


def new_error_log(error_type_info,e,error_type):
    error_info=error_type_info+traceback.format_exc()
    print(error_info)
    write_logs(error_info,error_type)