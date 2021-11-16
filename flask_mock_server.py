import logging
import os
from datetime import datetime

from flask import jsonify, Flask, request

app = Flask(__name__)
FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] <%(levelname)s> %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=FORMAT,
                    filename=r'.\log\{}截图服务日志.txt'.format(str(datetime.now())[0:10]),
                    filemode='a')  # 打印到控制台
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(FORMAT)
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

img_videoPreset_mapping = {'0': '/zlxstp/bjl/ywb/dkywb.JPG',
                           '1': '/zlxstp/bjl/ywb/dkywb.JPG',
                           '2': '/zlxstp/bjl/ywb/ywb0.jpg',
                           '3': '/zlxstp/bjl/ywb/ywb1.jpg',
                           '4': '/zlxstp/bjl/ywenb/ywenb.jpg',
                           '5': '/zlxstp/bjl/ywenb/ywenb2.jpg', '6': '/zlxstp/bjl/CT/CTtgywj.jpg',
                           '7': '/zlxstp/bjl/PT/PTtgywj.jpg',
                           '8': '/zlxstp/bjl/SF6/SF6xlb.JPG', '9': '/zlxstp/bjl/SF6/SF6xlb-2.jpg',
                           '10': '/zlxstp/bjl/xldlb/blqjcq.jpg',
                           '11': '/zlxstp/bjl/xldlb/blqxldlb.jpg', '12': '/zlxstp/bjl/zzxjsq/fdjsq.jpg',
                           '13': '/zlxstp/glkg/czssglkg/220kVglkg-fen.jpg',
                           '14': '/zlxstp/glkg/czssglkg/220kVglkg-he.jpg',
                           '15': '/zlxstp/glkg/szspssglkg/00001jsb50112dz_A.jpg',
                           '16': '/zlxstp/glkg/szspssglkg/00002jsb50112dz_B.jpg',
                           '17': '/zlxstp/glkg/szspssglkg/00003jsb50112dz_C.jpg',
                           '18': '/zlxstp/glkg/szspxzglkg/110kVglkg_fen.jpg',
                           '19': '/zlxstp/glkg/szspxzglkg/110KVglkg_he.jpg',
                           '20': '/zlxstp/ptkg/fhfhxkg/fhfhxkg-fen.jpg',
                           '21': '/zlxstp/ptkg/fhfhxkg/fhfhxkg-he.jpg',
                           '22': '/zlxstp/ptkg/fhwzxtpkg/fhwzxtpkg-fen.jpg',
                           '23': '/zlxstp/ptkg/fhwzxtpkg/fhwzxtpkg-he.jpg',
                           '24': '/zlxstp/ptkg/tyfhwzxkg/tyfhwzxkg-fen.jpg',
                           '25': '/zlxstp/ptkg/tyfhwzxkg/tyfhwzxkg-he.jpg',
                           '26': '/zlxstp/ptkg/tyfhwzxkg/ywfhkg-off.jpg',
                           '27': '/zlxstp/ptkg/tyfhwzxkg/ywfhkg-on.jpg', '28': '/zlxstp/ptkg/zzkg/zzkg-fen.jpg',
                           '29': '/zlxstp/ptkg/zzkg/zzkg-he.jpg', '30': '/zlxstp/qtkg/cnzs/cnzs-ycn.jpg',
                           '31': '/zlxstp/qtkg/dlqfh/dlq-fen.jpg',
                           '32': '/zlxstp/qtkg/dlqfh/dlq-he.jpg', '33': '/zlxstp/qtkg/dlqfh/dlqfhzs-he.jpg',
                           '34': '/zlxstp/qtkg/kqkg/kqkg.jpg',
                           '35': '/zlxstp/qtkg/kqkg/zbyzxjcpkk.jpg', '36': '/zlxstp/qtkg/zzxcnkg/zzxcn-ycn.jpg',
                           '37': '/zlxstp/xn/gbfhzsxn/gbfhzsxn-X.jpg', '38': '/zlxstp/xn/gbfhzsxn/gbfhzsxn-Y.jpg',
                           '39': '/zlxstp/xn/gbfhzsxn/gbfhzsxn-Z.jpg', '40': '/zlxstp/xn/sbqxn/sbqxn.jpg',
                           '41': '/zlxstp/xn/zbqxn/zhbs.jpg',
                           '42': '/zlxstp/xn/zbqxn/zbqxn.jpg', '43': '/zlxstp/yb/yb-I/yb-I.jpg',
                           '44': '/zlxstp/yb/zzjcdyb/yaban_1.jpg',
                           '45': '/zlxstp/yb/zzjcdyb/yaban_2.jpg', '46': '/zlxstp/yb/zzjcdyb/yaban_3.jpg',
                           '47': '/zlxstp/yb/zzjcdyb/zzyb.jpg',
                           '48': '/zlxstp/zsd/szp-LED/LEDszdlbdyb.jpg', '49': '/zlxstp/zsd/szp-LED/LEDszp.jpg',
                           '50': '/zlxstp/zsd/szxjsq/jsq.jpg', '51': '/zlxstp/zsd/szxjsq/kgdzcsjsq.jpg',
                           '52': '/zlxstp/zsd/xzsd/xzsd-1.jpg',
                           '53': '/zlxstp/zsd/xzsd/xzsd-2.jpg', '54': '/zlxstp/zsd/zsd/dykgzsd.jpg',
                           '55': '/zlxstp/zsd/zsd/zlkxpzsd-I.jpg',
                           '56': '/zlxstp/zsd/zsd/kgg_0014.JPG', '57': '/zlxstp/zsd/zsd/kgg_0015.JPG',
                           '58': '/zlxstp/zsd/zsd/kggfhzzszt_0024.jpg', '59': '/zlxstp/zsd/zsd/kggfhzzszt_0032.jpg',
                           '60': '/zlxstp/zsd/zsd/kggfhzzszt_0038.jpg', '61': '/zlxstp/zsd/zsd/kggybzt_0005.jpg',
                           '62': '/zlxstp/ygl/bjdsyc/dsyc_1.jpg',
                           '63': '/zlxstp/ygl/bjdsyc/dsyc_2.jpg',
                           '64': '/zlxstp/ygl/bjdsyc/dsyc_3.jpg',
                           '65': '/zlxstp/ygl/bpps/bpps_0.jpg',
                           '66': '/zlxstp/ygl/bpps/bpps_1.jpg',
                           '67': '/zlxstp/ygl/bpps/bpps_2.jpg',
                           '68': '/zlxstp/ygl/bpps/bpps_3.jpg',
                           '69': '/zlxstp/ygl/bjwkps/wkps_1.jpg',
                           '70': '/zlxstp/ygl/bjwkps/wkps_2.jpg',
                           '71': '/zlxstp/ygl/bjwkps/wkps_3.jpg',
                           '72': '/zlxstp/ygl/bmwh/bmwh.jpg',
                           '73': '/zlxstp/ygl/bpmh/bpmh_0.jpg',
                           '74': '/zlxstp/ygl/bpmh/bpmh_1.jpg', '75': '/zlxstp/ygl/bpmh/bpmh_2.jpg',
                           '76': '/zlxstp/ygl/bpmh/bpmh_3.jpg',
                           '77': '/zlxstp/ygl/bjbmyw/bjbmyw_0.jpg', '78': '/zlxstp/ygl/bjbmyw/bjbmyw_1.jpg',
                           '79': '/zlxstp/ygl/dmyw/sly_dmyw_0.jpg', '80': '/zlxstp/ygl/dmyw/sly_dmyw_1.jpg',
                           '81': '/zlxstp/ygl/dmyw/sly_dmyw_2.jpg', '82': '/zlxstp/ygl/dmyw/sly_dmyw_3.jpg',
                           '83': '/zlxstp/ygl/gbps/gbps_0.jpg',
                           '84': '/zlxstp/ygl/gbps/gbps_1.jpg', '85': '/zlxstp/ygl/gbps/gbps_2.jpg',
                           '86': '/zlxstp/ygl/gbps/gbps_3.jpg',
                           '87': '/zlxstp/ygl/gjptwss/gjptwss.jpg', '88': '/zlxstp/ygl/gkxfw/gkxfw_0.jpg',
                           '89': '/zlxstp/ygl/gkxfw/gkxfw_1.jpg',
                           '90': '/zlxstp/ygl/gkxfw/gkxfw_2.jpg', '91': '/zlxstp/ygl/gkxfw/gkxfw_3.jpg',
                           '92': '/zlxstp/ygl/hxqgjbs/gjbs_0.jpg',
                           '93': '/zlxstp/ygl/hxqgjbs/gjbs_1.jpg', '94': '/zlxstp/ygl/hxqgjbs/gjbs_2.jpg',
                           '95': '/zlxstp/ygl/hxqgjbs/gjbs_3.jpg',
                           '96': '/zlxstp/ygl/hxqgjtps/gjtps_1.JPG', '97': '/zlxstp/ygl/hxqgjtps/gjtps_2.jpg',
                           '98': '/zlxstp/ygl/hxqgjtps/gjtps_3.jpg', '99': '/zlxstp/ygl/hxqgjtps/gjtps_4.jpg',
                           '100': '/zlxstp/ygl/hxqgjtps/gjtps_5.jpg',
                           '101': '/zlxstp/ygl/hxqyfps/yfps.jpg',
                           '102': '/zlxstp/ygl/hxqywztyfyc/ywyc_1.jpg',
                           '103': '/zlxstp/ygl/hxqywztyfyc/ywyc_2.jpg',
                           '104': '/zlxstp/ygl/hxqywztyfyc/ywyc_3.jpg',
                           '105': '/zlxstp/ygl/hxqywztyfyc/ywyc_4.jpg',
                           '106': '/zlxstp/ygl/jsxs/jsxs_0.jpg',
                           '107': '/zlxstp/ygl/jsxs/jsxs_1.jpg',
                           '108': '/zlxstp/ygl/jyzpl/jyzpl_1.JPG',
                           '109': '/zlxstp/ygl/jyzpl/jyzpl_2.JPG',
                           '110': '/zlxstp/ygl/jyzpl/jyzpl_3.JPG',
                           '111': '/zlxstp/ygl/jyzpl/jyzpl_4.JPG',
                           '112': '/zlxstp/ygl/jyzpl/jyzpl_5.JPG',
                           '113': '/zlxstp/ygl/mcqdmps/mcqdmps.jpg',
                           '114': '/zlxstp/ygl/nw/nc_0.jpg',
                           '115': '/zlxstp/ygl/nw/nc_1.jpg',
                           '116': '/zlxstp/ygl/nw/nc_2.jpg',
                           '117': '/zlxstp/ygl/nw/nc_3.jpg',
                           '118': '/zlxstp/ygl/sly/sly_dmyw_1.jpg', '119': '/zlxstp/ygl/sly/sly_dmyw_2.jpg',
                           '120': '/zlxstp/ygl/sly/sly_dmyw_3.jpg', '121': '/zlxstp/ygl/wcgz/wcgz_0.jpg',
                           '122': '/zlxstp/ygl/wcgz/wcgz_1.jpg',
                           '123': '/zlxstp/ygl/wcgz/wcgz_2.jpg', '124': '/zlxstp/ygl/wcgz/wcgz_3.jpg',
                           '125': '/zlxstp/ygl/wcgqm/wcaqm_0.jpg',
                           '126': '/zlxstp/ygl/wcgqm/wcaqm_1.jpg', '127': '/zlxstp/ygl/wcgqm/wcaqm_2.jpg',
                           '128': '/zlxstp/ygl/wcgqm/wcaqm_3.jpg',
                           '129': '/zlxstp/ygl/xy/xiyan_1.jpg', '130': '/zlxstp/ygl/xy/xiyan_2.jpg',
                           '131': '/zlxstp/ygl/xy/xiyan_3.jpg',
                           '132': '/zlxstp/ygl/xy/xiyan_4.jpg', '133': '/zlxstp/ygl/xy/xiyan_5.jpg',
                           '134': '/zlxstp/ygl/xmbhyc/xmbhyc_0.jpg',
                           '135': '/zlxstp/ygl/xmbhyc/xmbhyc_1.jpg', '136': '/zlxstp/ygl/xmbhyc/xmbhyc_2.jpg',
                           '137': '/zlxstp/ygl/xmbhyc/xmbhyc_3.jpg', '138': '/zlxstp/ygl/xdwcr/xdwcr_1.jpg',
                           '139': '/zlxstp/ygl/xdwcr/xdwcr_2.jpg', '140': '/zlxstp/ygl/yh/yh_1.jpg',
                           '141': '/zlxstp/ygl/yh/yh_2.jpg',
                           '142': '/zlxstp/ygl/ylh/ylw_0.JPG', '143': '/zlxstp/ygl/ylh/ylw_1.JPG',
                           '144': '/zlxstp/ygl/ylh/ylw_2.JPG',
                           '145': '/zlxstp/ygl/ylh/ylw_3.JPG', '146': '/zlxstp/ygl/yxcr/yxcr_0.jpg',
                           '147': '/zlxstp/ygl/yxcr/yxcr_1.jpg',
                           '148': '/zlxstp/zsd/szp-LED/LEDszdlbdyb.jpg',
                           '149': '/zlxstp/zsd/szp-LED/LEDszp.jpg',
                           '150': '/zlxstp/zsd/szxjsq/jsq.jpg',
                           '151': '/zlxstp/zsd/szxjsq/kgdzcsjsq.jpg',
                           '152': '/zlxstp/zsd/xzsd/xzsd-1.jpg',
                           '153': '/zlxstp/zsd/xzsd/xzsd-2.jpg',
                           '154': '/zlxstp/zsd/zsd/dykgzsd.jpg',
                           '155': '/zlxstp/zsd/zsd/zlkxpzsd-I.jpg',
                           '156': '/zlxstp/zsd/zsd/kgg_0014.JPG',
                           '157': '/zlxstp/zsd/zsd/kgg_0015.JPG',
                           '158': '/zlxstp/zsd/zsd/kggfhzzszt_0024.jpg',
                           '159': '/zlxstp/zsd/zsd/kggfhzzszt_0032.jpg',
                           '160': '/zlxstp/zsd/zsd/kggfhzzszt_0038.jpg',
                           '161': '/zlxstp/zsd/zsd/kggybzt_0005.jpg',
                           '162': '/zlxstp/ygl/bjdsyc/dsyc_1.jpg',
                           '163': '/zlxstp/ygl/bjdsyc/dsyc_2.jpg',
                           '164': '/zlxstp/ygl/bjdsyc/dsyc_3.jpg',
                           '165': '/zlxstp/ygl/bpps/bpps_0.jpg',
                           '166': '/zlxstp/ygl/bpps/bpps_1.jpg',
                           '167': '/zlxstp/ygl/bpps/bpps_2.jpg',
                           '168': '/zlxstp/ygl/bpps/bpps_3.jpg',
                           '169': '/zlxstp/ygl/bjwkps/wkps_1.jpg',
                           '170': '/zlxstp/ygl/bjwkps/wkps_2.jpg',
                           '171': '/zlxstp/ygl/bjwkps/wkps_3.jpg',
                           '172': '/zlxstp/ygl/bmwh/bmwh.jpg',
                           '173': '/zlxstp/ygl/bpmh/bpmh_0.jpg',
                           '174': '/zlxstp/ygl/bpmh/bpmh_1.jpg',
                           '175': '/zlxstp/ygl/bpmh/bpmh_2.jpg',
                           '176': '/zlxstp/ygl/bpmh/bpmh_3.jpg',
                           '177': '/zlxstp/ygl/bjbmyw/bjbmyw_0.jpg',
                           '178': '/zlxstp/ygl/bjbmyw/bjbmyw_1.jpg',
                           '179': '/zlxstp/ygl/dmyw/sly_dmyw_0.jpg',
                           '180': '/zlxstp/ygl/dmyw/sly_dmyw_1.jpg',
                           '181': '/zlxstp/ygl/dmyw/sly_dmyw_2.jpg',
                           '182': '/zlxstp/ygl/dmyw/sly_dmyw_3.jpg',
                           '183': '/zlxstp/ygl/gbps/gbps_0.jpg',
                           '184': '/zlxstp/ygl/gbps/gbps_1.jpg',
                           '185': '/zlxstp/ygl/gbps/gbps_2.jpg',
                           '186': '/zlxstp/ygl/gbps/gbps_3.jpg',
                           '187': '/zlxstp/ygl/gjptwss/gjptwss.jpg',
                           '188': '/zlxstp/ygl/gkxfw/gkxfw_0.jpg',
                           '189': '/zlxstp/ygl/gkxfw/gkxfw_1.jpg',
                           '190': '/zlxstp/ygl/gkxfw/gkxfw_2.jpg',
                           '191': '/zlxstp/ygl/gkxfw/gkxfw_3.jpg',
                           '192': '/zlxstp/ygl/hxqgjbs/gjbs_0.jpg',
                           '193': '/zlxstp/ygl/hxqgjbs/gjbs_1.jpg',
                           '194': '/zlxstp/ygl/hxqgjbs/gjbs_2.jpg',
                           '195': '/zlxstp/ygl/hxqgjbs/gjbs_3.jpg',
                           '196': '/zlxstp/ygl/hxqgjtps/gjtps_1.jpg',
                           '197': '/zlxstp/ygl/hxqgjtps/gjtps_2.jpg',
                           '198': '/zlxstp/ygl/hxqgjtps/gjtps_3.jpg',
                           '199': '/zlxstp/ygl/hxqgjtps/gjtps_4.jpg',
                           '200': '/zlxstp/ygl/hxqgjtps/gjtps_5.jpg',
                           '201': '/zlxstp/ygl/hxqyfps/yfps.jpg',
                           '202': '/zlxstp/ygl/hxqywztyfyc/ywyc_1.jpg',
                           '203': '/zlxstp/ygl/hxqywztyfyc/ywyc_2.jpg',
                           '204': '/zlxstp/ygl/hxqywztyfyc/ywyc_3.jpg',
                           '205': '/zlxstp/ygl/hxqywztyfyc/ywyc_4.jpg',
                           '206': '/zlxstp/ygl/jsxs/jsxs_0.jpg',
                           '207': '/zlxstp/ygl/jsxs/jsxs_1.jpg',
                           '208': '/zlxstp/ygl/jyzpl/jyzpl_1.JPG',
                           '209': '/zlxstp/ygl/jyzpl/jyzpl_2.JPG',
                           '210': '/zlxstp/ygl/jyzpl/jyzpl_3.JPG',
                           '211': '/zlxstp/ygl/jyzpl/jyzpl_4.JPG',
                           '212': '/zlxstp/ygl/jyzpl/jyzpl_5.JPG',
                           '213': '/zlxstp/ygl/mcqdmps/mcqdmps.jpg',
                           '214': '/zlxstp/ygl/nw/nc_0.jpg',
                           '215': '/zlxstp/ygl/nw/nc_1.jpg',
                           '216': '/zlxstp/ygl/nw/nc_2.jpg',
                           '217': '/zlxstp/ygl/nw/nc_3.jpg',
                           '218': '/zlxstp/ygl/sly/sly_dmyw_1.jpg',
                           '219': '/zlxstp/ygl/sly/sly_dmyw_2.jpg',
                           '220': '/zlxstp/ygl/sly/sly_dmyw_3.jpg',
                           '221': '/zlxstp/ygl/wcgz/wcgz_0.jpg',
                           '222': '/zlxstp/ygl/wcgz/wcgz_1.jpg',
                           '223': '/zlxstp/ygl/wcgz/wcgz_2.jpg',
                           '224': '/zlxstp/ygl/wcgz/wcgz_3.jpg',
                           '225': '/zlxstp/ygl/wcgqm/wcaqm_0.jpg',
                           '226': '/zlxstp/ygl/wcgqm/wcaqm_1.jpg',
                           '227': '/zlxstp/ygl/wcgqm/wcaqm_2.jpg',
                           '228': '/zlxstp/ygl/wcgqm/wcaqm_3.jpg',
                           '229': '/zlxstp/ygl/xy/xiyan_1.jpg',
                           '230': '/zlxstp/ygl/xy/xiyan_2.jpg',
                           '231': '/zlxstp/ygl/xy/xiyan_3.jpg',
                           '232': '/zlxstp/ygl/xy/xiyan_4.jpg',
                           '233': '/zlxstp/ygl/xy/xiyan_5.jpg',
                           '234': '/zlxstp/ygl/xmbhyc/xmbhyc_0.jpg',
                           '235': '/zlxstp/ygl/xmbhyc/xmbhyc_1.jpg',
                           '236': '/zlxstp/ygl/xmbhyc/xmbhyc_2.jpg',
                           '237': '/zlxstp/ygl/xmbhyc/xmbhyc_3.jpg',
                           '238': '/zlxstp/ygl/xdwcr/xdwcr_1.jpg',
                           '239': '/zlxstp/ygl/xdwcr/xdwcr_2.jpg',
                           '240': '/zlxstp/ygl/yh/yh_1.jpg',
                           '241': '/zlxstp/ygl/yh/yh_2.jpg',
                           '242': '/zlxstp/ygl/ylh/ylw_0.JPG',
                           '243': '/zlxstp/ygl/ylh/ylw_1.JPG',
                           '244': '/zlxstp/ygl/ylh/ylw_2.JPG',
                           '245': '/zlxstp/ygl/ylh/ylw_3.JPG',
                           '246': '/zlxstp/ygl/yxcr/yxcr_0.jpg',
                           '247': '/zlxstp/ygl/yxcr/yxcr_1.jpg',
                           '248': '/zlxstp/ygl/ylh/ylw_0.JPG',
                           '249': '/zlxstp/ygl/ylh/ylw_1.JPG',
                           '250': '/zlxstp/ygl/ylh/ylw_2.JPG',
                           '251': '/zlxstp/glkg/jddz/daoza_fen_1.jpg',
                           '252': '/zlxstp/glkg/jddz/daoza_fen_2.jpg',
                           '253': '/zlxstp/glkg/jddz/daoza_fen_3.jpg',
                           '254': '/zlxstp/glkg/jddz/daoza_fen_4.jpg',
                           '255': '/zlxstp/glkg/jddz/daoza_fen_5.jpg',


                           }
HOST = [a for a in os.popen('route print').readlines() if ' 0.0.0.0 ' in a][0].split()[-2]
# 截图服务的地址
image_host = "192.168.4.181"
image_host_port = "20202"
img_server = "http://" + image_host + ":" + image_host_port + "/image"
# 方法为get的回复内容
res1 = {
    "code": 200,
    "data": [
        {

            "img_url": "methods is GET"
        }
    ],
    "message": "restapi.ok",
    "timestamp": "2021-04-01 14:51:49"
}


@app.route('/media/appserver/image/video_snop', methods=['GET', 'POST'])
def app_screenshot1():
    if request.method == 'GET':
        return jsonify(res1)
    else:
        import time
        time.sleep(0)
        json_data = request.json
        videoPreset = request.json.get('videoPreset')
        logging.info("**** 【json_data】**** ：{}".format(json_data))
        # 图片服务的地址

        # img_url = "http://192.168.4.77:20205/image" + img_videoPreset_mapping[str(videoPreset)]
        img_url = img_server + img_videoPreset_mapping[str(videoPreset)]
        # print(img_url)
        res = {
            "code": 200,
            "data": [
                {

                    "img_url": img_url
                }
            ],
            "message": "restapi.ok",
            "timestamp": "2021-04-04 16:01:01"
        }
        # test_data = request.json(res)
        return jsonify(res)


@app.route('/media/appserver/image', methods=['GET', 'POST'])
def app_screenshot2():
    if request.method == 'GET':
        return jsonify(res1)
    else:
        import time
        time.sleep(0)
        json_data = request.json
        videoPreset = request.json.get('videoPreset')
        logging.info("**** 【json_data】**** ：{}".format(json_data))
        # 图片服务的地址

        # img_url = "http://192.168.4.77:20205/image" + img_videoPreset_mapping[str(videoPreset)]
        img_url = img_server + img_videoPreset_mapping[str(videoPreset)]
        # print(img_url)
        res = {
            "code": 200,
            "data": [
                {

                    "img_url": img_url
                }
            ],
            "message": "restapi.ok",
            "timestamp": "2021-04-04 16:02:02"
        }
        # test_data = request.json(res)
        return jsonify(res)


@app.route('/media/appserver/image/video_snap', methods=['GET', 'POST'])
def app_screenshot3():
    if request.method == 'GET':
        return jsonify(res1)
    else:
        import time
        time.sleep(0)
        json_data = request.json
        videoPreset = request.json.get('videoPreset')
        logging.info("**** 【json_data】**** ：{}".format(json_data))
        # 图片服务的地址

        # img_url = "http://192.168.4.77:20205/image" + img_videoPreset_mapping[str(videoPreset)]
        img_url = img_server + img_videoPreset_mapping[str(videoPreset)]
        # print(img_url)
        res = {
            "code": 200,
            "data": [
                {

                    "img_url": img_url
                }
            ],
            "message": "restapi.ok",
            "timestamp": "2021-04-04 16:03:03"
        }
        # test_data = request.json(res)
        return jsonify(res)


@app.route('/virtual/snap', methods=['GET', 'POST'])
def app_screenshot4():
    if request.method == 'GET':
        return jsonify(res1)
    else:
        import time
        time.sleep(0)
        json_data = request.json
        videoPreset = request.json.get('videoPreset')
        logging.info("**** 【json_data】**** ：{}".format(json_data))
        # 图片服务的地址

        # img_url = "http://192.168.4.77:20205/image" + img_videoPreset_mapping[str(videoPreset)]
        img_url = img_server + img_videoPreset_mapping[str(videoPreset)]
        # print(img_url)
        res = {
            "code": 200,
            "data": [
                {

                    "img_url": img_url
                }
            ],
            "message": "restapi.ok",
            "timestamp": "2021-04-04 16:04:04"
        }
        # test_data = request.json(res)
        return jsonify(res)


if __name__ == "__main__":
    # HOST = [a for a in os.popen('route print').readlines() if ' 0.0.0.0 ' in a][0].split()[-2]
    PORT = 20202

    # try:
    #     confirm = input("自动获取的IP地址为：{}，如需修改，请输入y:".format(HOST))
    #     if confirm == "y":
    #         HOST = input("请输入分析服务上报IP(本地ip):")
    #     else:
    #         pass
    # except:
    #     print("无ip地址")
    #
    # try:
    #     confirm = input("自动获取的端口为：{}，如需修改，请输入y:".format(PORT))
    #     if confirm == "y":
    #         PORT = input("请输入端口(分析服务上报端口):")
    #         PORT = int(PORT)
    #
    #     else:
    #         pass
    # except:
    #     print("无端口信息")
    logging.info("**** 【截图服务 启动时间】**** ：{}".format(str(datetime.now())[0:16]))
    logging.info("**** 【请确认图片服务器】 **** ：{}".format(img_server))
    logging.info("**** 【截图服务】 **** ：http://{}:{}/".format(HOST, PORT))
    app.run(
        host=HOST,
        port=PORT,
        # 是否调试
        debug=False
    )
