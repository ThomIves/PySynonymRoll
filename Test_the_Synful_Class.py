from Syns_Module_Builder import Syns_Module_Builder as SMB
import json

###############################################################################
base_dir = 'D:/GH_Repositories/PySynRoll'
synonym_module_name = 'Test'
word_list = ["barrier", ]
smb = SMB(base_dir, synonym_module_name, word_list)

pretty_dict = json.dumps(smb.syns_dict, indent=4)
print(pretty_dict)
