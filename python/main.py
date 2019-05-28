#!/usr/bin/python

import requests_html as html
from functools import reduce
import toml

import argparse
import wichtel
import common

import sys


def main():
    parser = argparse.ArgumentParser(description="Which 'wichtel' url should be seached for which keywords?")
    parser.add_argument('-c', '--config-file', dest='cfg_file', metavar='toml_path', type=str, help='The Path to the toml configuration file', default = './config.toml')
    parser.add_argument('-d', '--debug',action ='store_true', help='Enables the debug mode (no email will be send)')

    
    
    args = parser.parse_args()
    cfg = toml.load(args.cfg_file)
    cfg_r = cfg['restaurants']
    cfg_e = cfg['email']
    print(cfg_e)
    wichtel_menu = common.FoodSite(name='Wichtel', menu_url=wichtel.url, keywords=cfg_r['wichtel']['keywords'], extract_menu_fn=wichtel.gen_week_menu_wichtel)
    wichtel_matches = list(wichtel_menu.get_interesting_entrys(keywords=None, comparator_fn=lambda a, b: common.simplify_string(a)in common.simplify_string(b)))

    mail_text = ""
    wichtel_bool = len(wichtel_matches) > 0
    if (wichtel_bool):
        mail_text+="Interessantes beim Wichtel:\n\t"+str(reduce(lambda a,b:str(a)+'\n\t'+str(b)if b != None else "", wichtel_matches))+'\n'

    print(mail_text)
    
    if (wichtel_bool and cfg_e['email_enabled'] and not args.debug):
        send_cfg = cfg_e['sender']
        common.send_emails(send_cfg['server']
            , send_cfg['port']
            , send_cfg['email_address']
            , send_cfg['password']
            , cfg_e['receiver']['receiver_emails']
            , cfg_e['subject']
            , mail_text)



if __name__ == "__main__":
    main()
