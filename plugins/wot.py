#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2013 Vit@liy <vitaliy@root.ua>                             #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

tanks_data = {8257: {'name_i18n': u'Renault UE 57', 'name': u'RenaultUE57', 'level': 3},
54609: {'name_i18n': u'Sexton I', 'name': u'Sexton_I', 'level': 3},
2849: {'name_i18n': u'T34', 'name': u'T34_hvy', 'level': 8},
9473: {'name_i18n': u'\u0422-50', 'name': u'T-50', 'level': 4},
12369: {'name_i18n': u'Conqueror Gun', 'name': u'Conqueror_Gun', 'level': 10},
5425: {'name_i18n': u'113', 'name': u'Ch22_113', 'level': 10},
64065: {'name_i18n': u'FCM 50 t', 'name': u'FCM_50t', 'level': 8},
51473: {'name_i18n': u'Pz.Kpfw. V/IV', 'name': u'PzV_PzIV', 'level': 6},
6721: {'name_i18n': u'BDR G1 B', 'name': u'BDR_G1B', 'level': 5},
15905: {'name_i18n': u'M60', 'name': u'M60', 'level': 10},
7953: {'name_i18n': u'Jagdtiger', 'name': u'JagdTiger', 'level': 9},
52497: {'name_i18n': u'Pz.Kpfw. 38H 735 (f)', 'name': u'H39_captured', 'level': 2},
8017: {'name_i18n': u'Valentine AT', 'name': u'Valentine_AT', 'level': 3},
3329: {'name_i18n': u'\u041c\u0421-1', 'name': u'MS-1', 'level': 1},
3345: {'name_i18n': u'Pz.Kpfw. 38 (t)', 'name': u'Pz38t', 'level': 3},
8785: {'name_i18n': u'AT2', 'name': u'AT2', 'level': 5},
54353: {'name_i18n': u'Excelsior', 'name': u'Excelsior', 'level': 5},
7457: {'name_i18n': u'M40/M43', 'name': u'M40M43', 'level': 8},
2321: {'name_i18n': u'VK 36.01 (H)', 'name': u'VK3601H', 'level': 6},
9985: {'name_i18n': u'\u0421\u0423-101', 'name': u'SU-101', 'level': 8},
13089: {'name_i18n': u'T110E4', 'name': u'T110E4', 'level': 10},
55297: {'name_i18n': u'\u0421\u0423-122-44', 'name': u'SU122_44', 'level': 7},
13569: {'name_i18n': u'\u041e\u0431\u044a\u0435\u043a\u0442 268', 'name': u'Object268', 'level': 10},
4145: {'name_i18n': u'121', 'name': u'Ch19_121', 'level': 10},
7489: {'name_i18n': u'Lorraine 155 mle. 51', 'name': u'Lorraine155_51', 'level': 8},
5377: {'name_i18n': u'\u0418\u0421-3', 'name': u'IS-3', 'level': 8},
3121: {'name_i18n': u'M5A1 Stuart', 'name': u'Ch09_M5', 'level': 4},
4673: {'name_i18n': u'AMX 13 F3 AM', 'name': u'AMX_13F3AM', 'level': 6},
1073: {'name_i18n': u'T-34-1', 'name': u'Ch04_T34_1', 'level': 7},
4385: {'name_i18n': u'T32', 'name': u'T32', 'level': 8},
55057: {'name_i18n': u'Pz.Kpfw. IV hydrostat.', 'name': u'PzIV_Hydro', 'level': 5},
16161: {'name_i18n': u'M53/M55', 'name': u'M53_55', 'level': 9},
3857: {'name_i18n': u'Jagdpanther', 'name': u'JagdPanther', 'level': 7},
7697: {'name_i18n': u'Ferdinand', 'name': u'Ferdinand', 'level': 8},
10817: {'name_i18n': u'AMX AC mle. 46', 'name': u'AMX_AC_Mle1946', 'level': 7},
5905: {'name_i18n': u'Wespe', 'name': u'Wespe', 'level': 3},
11601: {'name_i18n': u'FV3805', 'name': u'FV3805', 'level': 9},
53249: {'name_i18n': u'\u041a\u0412-5', 'name': u'KV-5', 'level': 8},
4865: {'name_i18n': u'\u0421\u0423-5', 'name': u'SU-5', 'level': 4},
13841: {'name_i18n': u'Indien-Panzer', 'name': u'Indien_Panzer', 'level': 8},
7441: {'name_i18n': u'VK 45.02 (P) Ausf. B', 'name': u'VK4502P', 'level': 9},
14353: {'name_i18n': u'Aufkl\xe4rungspanzer Panther', 'name': u'Auf_Panther', 'level': 7},
1313: {'name_i18n': u'M4A3E8 Sherman', 'name': u'M4A3E8_Sherman', 'level': 6},
8225: {'name_i18n': u'T28', 'name': u'T28', 'level': 8},
16913: {'name_i18n': u'Waffentr\xe4ger auf E 100', 'name': u'Waffentrager_E100', 'level': 10},
1793: {'name_i18n': u'\u0421-51', 'name': u'S-51', 'level': 7},
4881: {'name_i18n': u'Pz.Kpfw. III Ausf. A', 'name': u'PzIII_A', 'level': 3},
52225: {'name_i18n': u'\u0411\u0422-\u0421\u0412', 'name': u'BT-SV', 'level': 3},
10577: {'name_i18n': u'Loyd Carrier', 'name': u'Loyd_Carrier', 'level': 2},
64561: {'name_i18n': u'112', 'name': u'Ch23_112', 'level': 8},
10529: {'name_i18n': u'T49', 'name': u'T49', 'level': 5},
6993: {'name_i18n': u'Cruiser Mk II', 'name': u'Cruiser_Mk_II', 'level': 3},
55073: {'name_i18n': u'T7 Combat Car', 'name': u'T7_Combat_Car', 'level': 2},
3137: {'name_i18n': u'AMX 50 100', 'name': u'AMX_50_100', 'level': 8},
7169: {'name_i18n': u'\u0418\u0421-7', 'name': u'IS-7', 'level': 10},
3649: {'name_i18n': u'Bat.-Ch\xe2tillon 25 t', 'name': u'Bat_Chatillon25t', 'level': 10},
6913: {'name_i18n': u'\u0421\u0423-85\u0411', 'name': u'GAZ-74b', 'level': 4},
3409: {'name_i18n': u'Sexton', 'name': u'Sexton', 'level': 3},
7969: {'name_i18n': u'M12', 'name': u'M12', 'level': 7},
8961: {'name_i18n': u'\u041a\u0412-13', 'name': u'KV-13', 'level': 7},
5137: {'name_i18n': u'Tiger II', 'name': u'PzVIB_Tiger_II', 'level': 8},
54289: {'name_i18n': u'L\xf6we', 'name': u'Lowe', 'level': 8},
11025: {'name_i18n': u'Pz.Sfl. V', 'name': u'Sturer_Emil', 'level': 7},
1553: {'name_i18n': u'Jagdpanzer IV', 'name': u'JagdPzIV', 'level': 6},
2817: {'name_i18n': u'\u041a\u0412-1\u0421', 'name': u'KV-1s', 'level': 6},
6657: {'name_i18n': u'\u0422-43', 'name': u'T-43', 'level': 7},
9217: {'name_i18n': u'\u041e\u0431\u044a\u0435\u043a\u0442 252', 'name': u'IS-6', 'level': 8},
4641: {'name_i18n': u'M37', 'name': u'M37', 'level': 4},
54545: {'name_i18n': u'T-25', 'name': u'T-25', 'level': 5},
2097: {'name_i18n': u'WZ-111 model 1-4', 'name': u'Ch12_111_1_2_3', 'level': 9},
13313: {'name_i18n': u'\u041e\u0431\u044a\u0435\u043a\u0442 416', 'name': u'Object416', 'level': 8},
3841: {'name_i18n': u'\u0421\u0423-18', 'name': u'SU-18', 'level': 2},
1825: {'name_i18n': u'M2 Light Tank', 'name': u'M2_lt', 'level': 2},
5697: {'name_i18n': u'Lorraine 40 t', 'name': u'Lorraine40t', 'level': 9},
8705: {'name_i18n': u'\u041e\u0431\u044a\u0435\u043a\u0442 261', 'name': u'Object_261', 'level': 10},
15649: {'name_i18n': u'T71', 'name': u'T71', 'level': 7},
10753: {'name_i18n': u'\u0421\u0422-I', 'name': u'ST_I', 'level': 9},
2065: {'name_i18n': u'Pz.Kpfw. II', 'name': u'PzII', 'level': 2},
769: {'name_i18n': u'\u0411\u0422-7', 'name': u'BT-7', 'level': 3},
8977: {'name_i18n': u'G.W. Panther', 'name': u'G_Panther', 'level': 7},
5393: {'name_i18n': u'VK 16.02 Leopard', 'name': u'VK1602', 'level': 5},
14113: {'name_i18n': u'M48A1 Patton', 'name': u'M48A1', 'level': 10},
56577: {'name_i18n': u'\u041b\u0422\u041f', 'name': u'LTP', 'level': 3},
4433: {'name_i18n': u'Conqueror', 'name': u'Conqueror', 'level': 9},
11009: {'name_i18n': u'\u041a\u0412-4', 'name': u'KV4', 'level': 8},
3889: {'name_i18n': u'WZ-132', 'name': u'Ch17_WZ131_1_WZ132', 'level': 8},
5153: {'name_i18n': u'M5 Stuart', 'name': u'M5_Stuart', 'level': 4},
52001: {'name_i18n': u'MTLS-1G14', 'name': u'MTLS-1G14', 'level': 3},
4897: {'name_i18n': u'M2 Medium Tank', 'name': u'M2_med', 'level': 3},
1089: {'name_i18n': u'B1', 'name': u'B1', 'level': 4},
4401: {'name_i18n': u'Type 2597 Chi-Ha', 'name': u'Ch08_Type97_Chi_Ha', 'level': 3},
6161: {'name_i18n': u'Pz.Kpfw. II Luchs', 'name': u'PzII_Luchs', 'level': 4},
4657: {'name_i18n': u'Type T-34', 'name': u'Ch21_T34', 'level': 5},
273: {'name_i18n': u'Hummel', 'name': u'Hummel', 'level': 6},
6145: {'name_i18n': u'\u0418\u0421-4', 'name': u'IS-4', 'level': 10},
10513: {'name_i18n': u'VK 45.02 (P) Ausf. A', 'name': u'VK4502A', 'level': 8},
64049: {'name_i18n': u'T-34-3', 'name': u'Ch14_T34_3', 'level': 8},
15105: {'name_i18n': u'\u0422-70', 'name': u'T-70', 'level': 3},
8449: {'name_i18n': u'212\u0410', 'name': u'Object_212', 'level': 9},
51457: {'name_i18n': u'\u041c\u0430\u0442\u0438\u043b\u044c\u0434\u0430 IV', 'name': u'Matilda_II_LL', 'level': 5},
12305: {'name_i18n': u'E 50 Ausf. M', 'name': u'E50_Ausf_M', 'level': 10},
4129: {'name_i18n': u'M41', 'name': u'M41', 'level': 5},
57617: {'name_i18n': u'Panther/M10', 'name': u'Panther_M10', 'level': 7},
57361: {'name_i18n': u'Pz.Kpfw. IV Schmalturm', 'name': u'PzIV_schmalturm', 'level': 6},
10065: {'name_i18n': u'AT7', 'name': u'AT7', 'level': 7},
2305: {'name_i18n': u'\u0421\u0423-152', 'name': u'SU-152', 'level': 7},
7249: {'name_i18n': u'FV4202 105', 'name': u'FV4202_105', 'level': 10},
257: {'name_i18n': u'\u0421\u0423-85', 'name': u'SU-85', 'level': 5},
54033: {'name_i18n': u'Pz.Kpfw. V/IV Alpha', 'name': u'PzV_PzIV_ausf_Alfa', 'level': 6},
5969: {'name_i18n': u'Centurion', 'name': u'Centurion', 'level': 8},
12097: {'name_i18n': u'AMX AC mle. 48', 'name': u'AMX_AC_Mle1948', 'level': 8},
1105: {'name_i18n': u'Cromwell', 'name': u'Cromwell', 'level': 6},
2385: {'name_i18n': u'Vickers Medium Mk III', 'name': u'Vickers_Medium_Mk_III', 'level': 3},
54529: {'name_i18n': u'\u0422\u0435\u0442\u0440\u0430\u0440\u0445', 'name': u'Tetrarch_LL', 'level': 2},
11281: {'name_i18n': u'Marder 38T', 'name': u'Marder_III', 'level': 4},
8737: {'name_i18n': u'T95', 'name': u'T95', 'level': 9},
16145: {'name_i18n': u'Pz.Sfl. IVc', 'name': u'Pz_Sfl_IVc', 'level': 5},
9297: {'name_i18n': u'FV215b 183', 'name': u'FV215b_183', 'level': 10},
51201: {'name_i18n': u'\u041a\u0412-220', 'name': u'KV-220_test', 'level': 5},
529: {'name_i18n': u'Tiger I', 'name': u'PzVI', 'level': 7},
1569: {'name_i18n': u'T20', 'name': u'T20', 'level': 7},
16129: {'name_i18n': u'\u0421\u0423-14-1', 'name': u'SU14_1', 'level': 7},
7681: {'name_i18n': u'\u0421\u0423-26', 'name': u'SU-26', 'level': 3},
16897: {'name_i18n': u'\u041e\u0431\u044a\u0435\u043a\u0442 140', 'name': u'Object_140', 'level': 10},
8209: {'name_i18n': u'Pz.Kpfw. 38 (t) n.A.', 'name': u'Pz38_NA', 'level': 4},
16657: {'name_i18n': u'Rhm.-Borsig Waffentr\xe4ger', 'name': u'RhB_Waffentrager', 'level': 8},
15633: {'name_i18n': u'Pz.Sfl. IVb', 'name': u'Pz_Sfl_IVb', 'level': 4},
305: {'name_i18n': u'Type 62', 'name': u'Ch02_Type62', 'level': 7},
15889: {'name_i18n': u'VK 30.02 (M)', 'name': u'VK3002M', 'level': 6},
52481: {'name_i18n': u'\u0412\u0430\u043b\u0435\u043d\u0442\u0430\u0439\u043d II', 'name': u'Valentine_LL', 'level': 4},
3153: {'name_i18n': u'Black Prince', 'name': u'Black_Prince', 'level': 7},
14337: {'name_i18n': u'\u041e\u0431\u044a\u0435\u043a\u0442 263', 'name': u'Object263', 'level': 10},
53537: {'name_i18n': u'T1E6', 'name': u'T1_E6', 'level': 2},
2881: {'name_i18n': u'AMX 40', 'name': u'AMX40', 'level': 4},
4113: {'name_i18n': u'VK 30.02 (D)', 'name': u'VK3002DB', 'level': 7},
10785: {'name_i18n': u'T110E5', 'name': u'T110', 'level': 10},
14609: {'name_i18n': u'Leopard 1', 'name': u'Leopard1', 'level': 10},
6177: {'name_i18n': u'T18', 'name': u'T18', 'level': 2},
2833: {'name_i18n': u'Sturmpanzer I Bison', 'name': u'Bison_I', 'level': 3},
5121: {'name_i18n': u'\u0410\u0422-1', 'name': u'AT-1', 'level': 2},
4353: {'name_i18n': u'\u0422-44', 'name': u'T-44', 'level': 8},
3921: {'name_i18n': u'Caernarvon', 'name': u'Caernarvon', 'level': 8},
785: {'name_i18n': u'Pz.Kpfw. 35 (t)', 'name': u'Pz35t', 'level': 2},
3393: {'name_i18n': u'Lorraine 39L AM', 'name': u'Lorraine39_L_AM', 'level': 3},
1809: {'name_i18n': u'Hetzer', 'name': u'Hetzer', 'level': 4},
33: {'name_i18n': u'T14', 'name': u'T14', 'level': 5},
2577: {'name_i18n': u'VK 30.01 (H)', 'name': u'VK3001H', 'level': 5},
1841: {'name_i18n': u'WZ-120', 'name': u'Ch18_WZ-120', 'level': 9},
11089: {'name_i18n': u'Bishop', 'name': u'Bishop', 'level': 5},
849: {'name_i18n': u'Matilda', 'name': u'Matilda', 'level': 4},
2049: {'name_i18n': u'\u0410-20', 'name': u'A-20', 'level': 4},
1537: {'name_i18n': u'\u0422-28', 'name': u'T-28', 'level': 4},
2561: {'name_i18n': u'\u0422-34-85', 'name': u'T-34-85', 'level': 6},
7425: {'name_i18n': u'\u0418\u0421\u0423-152', 'name': u'ISU-152', 'level': 8},
53585: {'name_i18n': u'Matilda Black Prince', 'name': u'Matilda_Black_Prince', 'level': 5},
53841: {'name_i18n': u'TOG II', 'name': u'TOG_II', 'level': 6},
11777: {'name_i18n': u'\u041a\u0412-1', 'name': u'KV1', 'level': 5},
8721: {'name_i18n': u'G.W. Tiger', 'name': u'G_Tiger', 'level': 9},
51745: {'name_i18n': u'Ram II', 'name': u'Ram-II', 'level': 5},
513: {'name_i18n': u'\u0418\u0421', 'name': u'IS', 'level': 7},
11297: {'name_i18n': u'T28 Prototype', 'name': u'T28_Prototype', 'level': 8},
54785: {'name_i18n': u'\u0421\u0423-100Y', 'name': u'SU100Y', 'level': 6},
4625: {'name_i18n': u'Sturmpanzer II', 'name': u'Sturmpanzer_II', 'level': 4},
9249: {'name_i18n': u'T25 AT', 'name': u'T25_AT', 'level': 7},
15361: {'name_i18n': u'\u0422-60', 'name': u'T-60', 'level': 2},
15121: {'name_i18n': u'G.Pz. Mk. VI (e)', 'name': u'GW_Mk_VIe', 'level': 2},
6673: {'name_i18n': u'Marder II', 'name': u'G20_Marder_II', 'level': 3},
2593: {'name_i18n': u'T30', 'name': u'T30', 'level': 9},
16641: {'name_i18n': u'\u041c\u0422-25', 'name': u'MT25', 'level': 6},
337: {'name_i18n': u'Vickers Medium Mk II', 'name': u'Vickers_Medium_Mk_II', 'level': 2},
16401: {'name_i18n': u'Waffentr\xe4ger auf Pz. IV', 'name': u'Waffentrager_IV', 'level': 9},
54097: {'name_i18n': u'AT 15A', 'name': u'AT_15A', 'level': 7},
1345: {'name_i18n': u'Hotchkiss_H35', 'name': u'_Hotchkiss_H35', 'level': 2},
3361: {'name_i18n': u'T1 Heavy Tank', 'name': u'T1_hvy', 'level': 5},
11345: {'name_i18n': u'Crusader 5inch', 'name': u'Crusader_5inch', 'level': 7},
51985: {'name_i18n': u'Pz.Kpfw. S35 739 (f)', 'name': u'S35_captured', 'level': 3},
6929: {'name_i18n': u'Maus', 'name': u'Maus', 'level': 10},
11265: {'name_i18n': u'\u0422-150', 'name': u'T150', 'level': 6},
5665: {'name_i18n': u'T2 Medium Tank', 'name': u'T2_med', 'level': 2},
8465: {'name_i18n': u'Panther II', 'name': u'Panther_II', 'level': 8},
10049: {'name_i18n': u'S35 CA', 'name': u'S_35CA', 'level': 5},
11521: {'name_i18n': u'\u0418\u0421-8', 'name': u'IS8', 'level': 9},
52737: {'name_i18n': u'\u041c3 \u043b\u0451\u0433\u043a\u0438\u0439', 'name': u'M3_Stuart_LL', 'level': 3},
13329: {'name_i18n': u'Durchbruchswagen 2', 'name': u'DW_II', 'level': 4},
10257: {'name_i18n': u'E 50', 'name': u'E-50', 'level': 9},
13857: {'name_i18n': u'T110E3', 'name': u'T110E3', 'level': 10},
4945: {'name_i18n': u'Valentine', 'name': u'Valentine', 'level': 4},
8193: {'name_i18n': u'\u041e\u0431\u044a\u0435\u043a\u0442 704', 'name': u'Object_704', 'level': 9},
7713: {'name_i18n': u'T40', 'name': u'T40', 'level': 4},
16385: {'name_i18n': u'\u0421\u0423-122\u0410', 'name': u'SU122A', 'level': 5},
6433: {'name_i18n': u'T82', 'name': u'T82', 'level': 3},
14657: {'name_i18n': u'AMX 105 AM mle. 47', 'name': u'AMX_Ob_Am105', 'level': 4},
12561: {'name_i18n': u'Pz.Kpfw. I Ausf. C', 'name': u'PzI_ausf_C', 'level': 3},
15137: {'name_i18n': u'T21', 'name': u'T21', 'level': 6},
9489: {'name_i18n': u'E 100', 'name': u'E-100', 'level': 10},
1585: {'name_i18n': u'T-34-2', 'name': u'Ch05_T34_2', 'level': 8},
57105: {'name_i18n': u'Dicker Max', 'name': u'DickerMax', 'level': 6},
11585: {'name_i18n': u'ARL V39', 'name': u'ARL_V39', 'level': 6},
55313: {'name_i18n': u'8,8 cm Pak 43 Jagdtiger', 'name': u'JagdTiger_SdKfz_185', 'level': 8},
52241: {'name_i18n': u'Pz.Kpfw. B2 740 (f)', 'name': u'B-1bis_captured', 'level': 4},
2369: {'name_i18n': u'FCM 36 Pak 40', 'name': u'FCM_36Pak40', 'level': 3},
3089: {'name_i18n': u'Leichttraktor', 'name': u'Ltraktor', 'level': 1},
2113: {'name_i18n': u'105 leFH18B2', 'name': u'_105_leFH18B2', 'level': 5},
6209: {'name_i18n': u'F10_AMX_50B', 'name': u'AMX_50_68t', 'level': 10},
14625: {'name_i18n': u'T69', 'name': u'T69', 'level': 8},
3601: {'name_i18n': u'Panzerj\xe4ger I', 'name': u'PanzerJager_I', 'level': 2},
1329: {'name_i18n': u'Renault NC-31', 'name': u'Ch06_Renault_NC31', 'level': 1},
53761: {'name_i18n': u'\u0421\u0423-85\u0418', 'name': u'SU_85I', 'level': 5},
2625: {'name_i18n': u'ARL 44', 'name': u'ARL_44', 'level': 6},
10001: {'name_i18n': u'VK 28.01', 'name': u'VK2801', 'level': 6},
52257: {'name_i18n': u'M4A2E4 Sherman', 'name': u'M4A2E4', 'level': 5},
7505: {'name_i18n': u'Cruiser Mk IV', 'name': u'Cruiser_Mk_IV', 'level': 3},
3873: {'name_i18n': u'T29', 'name': u'T29', 'level': 7},
3633: {'name_i18n': u'IS-2', 'name': u'Ch10_IS2', 'level': 7},
8529: {'name_i18n': u'AT15', 'name': u'AT15', 'level': 8},
9745: {'name_i18n': u'E 75', 'name': u'E-75', 'level': 9},
3073: {'name_i18n': u'\u0422-46', 'name': u'T-46', 'level': 3},
289: {'name_i18n': u'M3 Stuart', 'name': u'M3_Stuart', 'level': 3},
577: {'name_i18n': u'Renault FT', 'name': u'RenaultFT', 'level': 1},
4609: {'name_i18n': u'\u0422-26', 'name': u'T-26', 'level': 2},
15393: {'name_i18n': u'T54E1', 'name': u'T54E1', 'level': 9},
10241: {'name_i18n': u'\u0421\u0423-100\u041c1', 'name': u'SU100M1', 'level': 7},
10017: {'name_i18n': u'M4A3E2 Sherman Jumbo', 'name': u'Sherman_Jumbo', 'level': 6},
53505: {'name_i18n': u'\u0422-127', 'name': u'T-127', 'level': 3},
9233: {'name_i18n': u'G.W. E 100', 'name': u'G_E', 'level': 10},
1025: {'name_i18n': u'\u0411\u0422-2', 'name': u'BT-2', 'level': 2},
5649: {'name_i18n': u'Grille', 'name': u'Grille', 'level': 5},
5953: {'name_i18n': u'AMX 38', 'name': u'AMX38', 'level': 3},
6401: {'name_i18n': u'\u0421\u0423-76', 'name': u'SU-76', 'level': 3},
54801: {'name_i18n': u'T-15', 'name': u'T-15', 'level': 3},
17: {'name_i18n': u'Pz.Kpfw. IV', 'name': u'PzIV', 'level': 5},
5185: {'name_i18n': u'AMX 13 75', 'name': u'AMX_13_75', 'level': 7},
3377: {'name_i18n': u'WZ-131', 'name': u'Ch16_WZ_131', 'level': 7},
2897: {'name_i18n': u'Churchill I', 'name': u'Churchill_I', 'level': 5},
11537: {'name_i18n': u'Jagdpanther II', 'name': u'JagdPantherII', 'level': 8},
12817: {'name_i18n': u'Pz.Kpfw. I', 'name': u'PzI', 'level': 2},
4689: {'name_i18n': u'Churchill VII', 'name': u'Churchill_VII', 'level': 6},
2129: {'name_i18n': u'Crusader', 'name': u'Crusader', 'level': 5},
9505: {'name_i18n': u'M103', 'name': u'M103', 'level': 9},
51729: {'name_i18n': u'Pz.Kpfw. II Ausf. J', 'name': u'PzII_J', 'level': 3},
7761: {'name_i18n': u'Cruiser Mk III', 'name': u'Cruiser_Mk_III', 'level': 2},
10497: {'name_i18n': u'\u041a\u0412-2', 'name': u'KV2', 'level': 6},
2353: {'name_i18n': u'Vickers Mk. E Type B', 'name': u'Ch07_Vickers_MkE_Type_BT26', 'level': 2},
51489: {'name_i18n': u'T2 Light Tank', 'name': u'T2_lt', 'level': 2},
11857: {'name_i18n': u'FV304', 'name': u'FV304', 'level': 6},
12033: {'name_i18n': u'\u0421\u0423-122-54', 'name': u'SU122_54', 'level': 9},
52993: {'name_i18n': u'\u0410-32', 'name': u'A-32', 'level': 4},
3617: {'name_i18n': u'M7 Priest', 'name': u'M7_Priest', 'level': 3},
3905: {'name_i18n': u'AMX 50 120', 'name': u'AMX_50_120', 'level': 9},
52513: {'name_i18n': u'M6A2E1', 'name': u'M6A2E1', 'level': 8},
10273: {'name_i18n': u'M8A1', 'name': u'M8A1', 'level': 4},
2865: {'name_i18n': u'110', 'name': u'Ch11_110', 'level': 8},
7937: {'name_i18n': u'\u0422-54', 'name': u'T-54', 'level': 9},
4369: {'name_i18n': u'Pz.Kpfw. III', 'name': u'PzIII', 'level': 4},
15873: {'name_i18n': u'\u0422-80', 'name': u'T80', 'level': 4},
2081: {'name_i18n': u'T57', 'name': u'T57', 'level': 2},
14401: {'name_i18n': u'Bat.-Ch\xe2tillon 155 55', 'name': u'Bat_Chatillon155_55', 'level': 9},
14097: {'name_i18n': u'VK 30.01 (D)', 'name': u'VK3002DB_V1', 'level': 6},
12545: {'name_i18n': u'\u0410-44', 'name': u'A44', 'level': 7},
5409: {'name_i18n': u'M7', 'name': u'M7_med', 'level': 5},
16417: {'name_i18n': u'M5', 'name': u'_M44', 'level': 6},
13345: {'name_i18n': u'T26E4 SuperPershing', 'name': u'T26_E4_SuperPershing', 'level': 8},
545: {'name_i18n': u'T1 Cunningham', 'name': u'T1_Cunningham', 'level': 1},
6481: {'name_i18n': u'Covenanter', 'name': u'Covenanter', 'level': 4},
64817: {'name_i18n': u'Type 64', 'name': u'Ch24_Type64', 'level': 6},
8273: {'name_i18n': u'Universal CarrierQF2', 'name': u'Universal_CarrierQF2', 'level': 2},
5889: {'name_i18n': u'\u041a\u0412-3', 'name': u'KV-3', 'level': 7},
6945: {'name_i18n': u'M10 Wolverine', 'name': u'M10_Wolverine', 'level': 5},
9793: {'name_i18n': u'Somua SAu 40', 'name': u'Somua_Sau_40', 'level': 4},
3585: {'name_i18n': u'\u0421\u0423-100', 'name': u'SU-100', 'level': 6},
81: {'name_i18n': u'Medium Mark I', 'name': u'Medium_Mark_I', 'level': 1},
51713: {'name_i18n': u'\u0427\u0435\u0440\u0447\u0438\u043b\u043b\u044c III', 'name': u'Churchill_LL', 'level': 5},
13585: {'name_i18n': u'VK 20.01 (D)', 'name': u'VK2001DB', 'level': 4},
4161: {'name_i18n': u'AMX 13 105 AM mle. 50', 'name': u'AMX_105AM', 'level': 5},
49: {'name_i18n': u'Type 59', 'name': u'Ch01_Type59', 'level': 8},
11073: {'name_i18n': u'AMX 50 Foch', 'name': u'AMX50_Foch', 'level': 9},
7201: {'name_i18n': u'M36 Jackson', 'name': u'M36_Slagger', 'level': 6},
6465: {'name_i18n': u'AMX 12 t', 'name': u'AMX_12t', 'level': 6},
6417: {'name_i18n': u'Pz.Kpfw. III/IV', 'name': u'PzIII_IV', 'level': 5},
51553: {'name_i18n': u'Type 3 Chi-Nu Kai', 'name': u'Chi_Nu_Kai', 'level': 5},
5457: {'name_i18n': u'Comet', 'name': u'Comet', 'level': 7},
1: {'name_i18n': u'\u0422-34', 'name': u'T-34', 'level': 5},
3105: {'name_i18n': u'M3 Lee', 'name': u'M3_Grant', 'level': 4},
321: {'name_i18n': u'D2', 'name': u'D2', 'level': 3},
5921: {'name_i18n': u'M26 Pershing', 'name': u'Pershing', 'level': 8},
10833: {'name_i18n': u'Birch Gun', 'name': u'Birch_Gun', 'level': 4},
6225: {'name_i18n': u'FV215b', 'name': u'FV215b', 'level': 10},
10769: {'name_i18n': u'Tiger (P)', 'name': u'PzVI_Tiger_P', 'level': 7},
7185: {'name_i18n': u'VK 30.01 (P)', 'name': u'VK3001P', 'level': 6},
54017: {'name_i18n': u'KV-220_action', 'name': u'KV-220', 'level': 5},
1297: {'name_i18n': u'Panther I', 'name': u'PzV', 'level': 7},
6977: {'name_i18n': u'AMX M4 mle. 45', 'name': u'AMX_M4_1945', 'level': 7},
14865: {'name_i18n': u'Leopard Prototyp A', 'name': u'Pro_Ag_A', 'level': 9},
4097: {'name_i18n': u'\u0421\u0423-14-2', 'name': u'SU-14', 'level': 8},
833: {'name_i18n': u'Renault FT 75 BS', 'name': u'RenaultBS', 'level': 2},
5713: {'name_i18n': u'Centurion Mk3', 'name': u'Centurion_Mk3', 'level': 9},
5169: {'name_i18n': u'Type 58', 'name': u'Ch20_Type58', 'level': 6},
7745: {'name_i18n': u'Renault FT AC', 'name': u'RenaultFT_AC', 'level': 2},
52769: {'name_i18n': u'M22 Locust', 'name': u'M22_Locust', 'level': 3},
5201: {'name_i18n': u'Cruiser Mk I', 'name': u'Cruiser_Mk_I', 'level': 2},
11553: {'name_i18n': u'M18 Hellcat', 'name': u'M18_Hellcat', 'level': 6},
9761: {'name_i18n': u'M24 Chaffee', 'name': u'M24_Chaffee', 'level': 5},
52561: {'name_i18n': u'Tortoise', 'name': u'Tortoise', 'level': 9},
7233: {'name_i18n': u'Lorraine 155 mle. 50', 'name': u'Lorraine155_50', 'level': 7},
11041: {'name_i18n': u'T25/2', 'name': u'T25_2', 'level': 7},
55569: {'name_i18n': u'E 25', 'name': u'E-25', 'level': 7},
9553: {'name_i18n': u'AT8', 'name': u'AT8', 'level': 6},
9041: {'name_i18n': u'Alecto', 'name': u'Alecto', 'level': 4},
12049: {'name_i18n': u'Jagdpanzer E 100', 'name': u'JagdPz_E100', 'level': 10},
12289: {'name_i18n': u'\u0410-43', 'name': u'A43', 'level': 6},
13825: {'name_i18n': u'\u0422-62\u0410', 'name': u'T62A', 'level': 10},
1041: {'name_i18n': u'StuG III', 'name': u'StuGIII', 'level': 5},
13073: {'name_i18n': u'Pz.Kpfw. II Ausf. G', 'name': u'Pz_II_AusfG', 'level': 3},
14145: {'name_i18n': u'ELC AMX', 'name': u'ELC_AMX', 'level': 5},
9809: {'name_i18n': u'Gun Carrier Churchill', 'name': u'Gun_Carrier_Churchill', 'level': 6},
1601: {'name_i18n': u'D1', 'name': u'D1', 'level': 2},
8993: {'name_i18n': u'M46 Patton', 'name': u'M46_Patton', 'level': 9},
1057: {'name_i18n': u'M4 Sherman', 'name': u'M4_Sherman', 'level': 5},
4913: {'name_i18n': u'59-16', 'name': u'Ch15_59_16', 'level': 6},
15377: {'name_i18n': u'G.W. Tiger (P)', 'name': u'GW_Tiger_P', 'level': 8},
5633: {'name_i18n': u'\u0421\u0423-8', 'name': u'SU-8', 'level': 6},
8481: {'name_i18n': u'T92', 'name': u'T92', 'level': 10},
11793: {'name_i18n': u'Nashorn', 'name': u'Nashorn', 'level': 6},
12113: {'name_i18n': u'FV206', 'name': u'FV206', 'level': 8},
14881: {'name_i18n': u'T57 Heavy Tank', 'name': u'T57_58', 'level': 10},
13889: {'name_i18n': u'AMX 50 Foch (155)', 'name': u'AMX_50Fosh_155', 'level': 10},
801: {'name_i18n': u'M6', 'name': u'M6', 'level': 6},
4929: {'name_i18n': u'AMX 13 90', 'name': u'AMX_13_90', 'level': 8},
11841: {'name_i18n': u'Bat_Chatillon155_58', 'name': u'Bat_Chatillon155', 'level': 10}
}

# RU
API_ADDR = 'http://api.worldoftanks.ru';
APP_ID = '171745d21f7f98fd8878771da1000a31';

def wot(type, jid, nick, text):
	text = text.strip()
	if text:
		text = text.split(' ', 1)
		if len(text) == 1:
			name, tank = text[0], ''
		else:
			name, tank = text[0], text[1].lower()
		try:
			data = load_page('%s/2.0/account/list/?application_id=%s&search=%s&fields=id&limit=1' % (API_ADDR, APP_ID, name))
			v = json.loads(data)
			player_id = str(v['data'][0]['id'])
			
			data = load_page('%s/2.0/account/tanks/?application_id=%s&account_id=%s&fields=statistics,tank_id' % (API_ADDR, APP_ID, player_id))
			vdata = json.loads(data)
			
			data = load_page('%s/2.0/account/info/?application_id=%s&account_id=%s&fields=clan,nickname,statistics.all' % (API_ADDR, APP_ID, player_id))
			pdata = json.loads(data)
			
			if pdata['data'][player_id]['clan']:
				clan_id = str(pdata['data'][player_id]['clan']['clan_id'])
				data = load_page('%s/2.0/clan/info//?application_id=%s&clan_id=%s&fields=abbreviation' % (API_ADDR, APP_ID, clan_id))
				cdata = json.loads(data)
				cname = cdata['data'][clan_id]['abbreviation']
		except:
			pdata = {'status': ''}
		
		if pdata['status'] == 'ok' and pdata['data'][player_id]:
			wotname = pdata['data'][player_id]['nickname'] + ('[%s]' % cname if pdata['data'][player_id]['clan'] else '')
			
			if tank:
				if len(tank) == 1:
					msg = L('Use more characters in the name of the tank','%s/%s'%(jid,nick))
				else:
					try:

						msg = '%s:' % wotname
						tids = [tid for tid in tanks_data if tank in tanks_data[tid]['name'].lower() or tank in tanks_data[tid]['name_i18n'].lower()]
						
						for t in vdata['data'][player_id]:
							if t['tank_id'] in tids:
								tank_win = t['statistics']['wins']
								tank_battle = t['statistics']['battles']
								if tank_battle:
									msg += '\n%s (%s/%s - %s%%)' % (tanks_data[t['tank_id']]['name_i18n'], tank_win, tank_battle, round(100.0*tank_win/tank_battle, 2))
								else:
									msg += '\n%s (%s/%s)' % (tanks_data[t['tank_id']]['name_i18n'], tank_win, tank_battle)
						if not msg.count('\n'):
							msg += L(' not founded tank','%s/%s'%(jid,nick))
					except:
						msg = L('Impossible to get tanks\' statistics','%s/%s'%(jid,nick))
			else:
				
				wins = pdata['data'][player_id]['statistics']['all']['wins']
				battles = pdata['data'][player_id]['statistics']['all']['battles']
				
				if not battles:
					msg = '%s: %s/%s' % (wotname, wins, battles)
					
				else:

					try:
						win_percent = round(100.0 * wins / battles, 2)
						msg = '%s: %s/%s  (%s%%)' % (wotname, wins, battles, win_percent)
						
						np = int(win_percent) + 1
						np_int = int((np * battles - 100 * wins) / (100 - np) + 1)
						np05 = int(win_percent + 0.5) + 0.5
						np_round = int((np05 * battles - 100 * wins) / (100 - np05) + 1)
						
						msg += L('\nUp to %s%% win left: %s battles', '%s/%s'%(jid,nick)) % (np, np_int)
						msg += L('\nUp to %s%% win left: %s battles', '%s/%s'%(jid,nick)) % (np05, np_round)

						avg_exp = pdata['data'][player_id]['statistics']['all']['battle_avg_xp']
						
						DAMAGE = pdata['data'][player_id]['statistics']['all']['damage_dealt'] / float(battles)
						msg += L('\nAv. damage: %s','%s/%s'%(jid,nick)) % int(round(DAMAGE))
						FRAGS = pdata['data'][player_id]['statistics']['all']['frags'] / float(battles)
						msg += L('\nAv. destroyed: %s','%s/%s'%(jid,nick)) % round(FRAGS, 2)
						SPOT = pdata['data'][player_id]['statistics']['all']['spotted'] / float(battles)
						msg += L('\nAv. spotted: %s','%s/%s'%(jid,nick)) % round(SPOT, 2)
						CAP = pdata['data'][player_id]['statistics']['all']['capture_points'] / float(battles)
						msg += L('\nAv. captured points: %s','%s/%s'%(jid,nick)) % round(CAP, 2)
						DEF = pdata['data'][player_id]['statistics']['all']['dropped_capture_points'] / float(battles)
						msg += L('\nAv. defense points: %s','%s/%s'%(jid,nick)) % round(DEF, 2)
						
						
						tanks = vdata['data'][player_id]
						s = sum([t['statistics']['all']['battles'] * tanks_data[t['tank_id']]['level'] for t in tanks])
						TIER = s / float(battles)
						
						WINRATE = wins / float(battles)
						
						msg += L('\nAv. tank lvl: %s','%s/%s'%(jid,nick)) % round(TIER, 2)
						
						er = DAMAGE * (10 / (TIER + 2)) * (0.23 + 2 * TIER / 100) + FRAGS * 250 + SPOT * 150 + math.log(CAP + 1) / math.log(1.732) * 150 + DEF * 150
						
						if er < 420:
							er_xvm = 0
						else:
							er_xvm = max(min(er*(er*(er*(er*(er*(4.5254e-17*er - 3.3131e-13) + 9.4164e-10) - 1.3227e-6) + 9.5664e-4) - 0.2598) + 13.23, 100), 0)
						
						msg += L('\nEfficiency rating: %s (XVM: %s)','%s/%s'%(jid,nick)) % (int(round(er)), round(er_xvm, 1))
						
						if er < 630:
							msg += L(' - bad player','%s/%s'%(jid,nick))
						elif er < 860:
							msg += L(' - player below average','%s/%s'%(jid,nick))
						elif er < 1140:
							msg += L(' - average player','%s/%s'%(jid,nick))
						elif er < 1460:
							msg += L(' - good player','%s/%s'%(jid,nick))
						elif er < 1735:
							msg += L(' - great player','%s/%s'%(jid,nick))
						elif er >= 1735:
							msg += L(' - unicum','%s/%s'%(jid,nick))
						
						wn6 = (1240 - 1040 / math.pow((min(TIER, 6)), 0.164)) * FRAGS + DAMAGE * 530 / (184 * math.exp(0.24 * TIER) + 130) + SPOT * 125 + min(DEF, 2.2) * 100 + ((185 / (0.17 + math.exp((WINRATE * 100 - 35) * -0.134))) - 500) * 0.45 + (6 - min(TIER, 6)) * (-60)

						if wn6 > 2160:
							wn6_xvm = 100
						else:
							wn6_xvm = max(min(wn6*(wn6*(wn6*(-1.268e-11*wn6 + 5.147e-8) - 6.418e-5) + 7.576e-2) - 7.25, 100), 0)
						
						msg += L('\nWN6 rating: %s (XVM: %s)','%s/%s'%(jid,nick)) % (int(round(wn6)), round(wn6_xvm, 1))
						
						if wn6 < 425:
							msg += L(' - bad player','%s/%s'%(jid,nick))
						elif wn6 < 795:
							msg += L(' - player below average','%s/%s'%(jid,nick))
						elif wn6 < 1175:
							msg += L(' - average player','%s/%s'%(jid,nick))
						elif wn6 < 1570:
							msg += L(' - good player','%s/%s'%(jid,nick))
						elif wn6 < 1885:
							msg += L(' - great player','%s/%s'%(jid,nick))
						elif wn6 >= 1885:
							msg += L(' - unicum','%s/%s'%(jid,nick))
						
						armor = math.log(battles) / 10 * (avg_exp + DAMAGE * (WINRATE * 2 + FRAGS * 0.9 + (SPOT + CAP + DEF) * 0.5))
						
						msg += L('\nArmor-rating: %s','%s/%s'%(jid,nick)) % int(round(armor))
					except:
						msg = L('Impossible to get statistics','%s/%s'%(jid,nick))
		elif not pdata['status']:
			msg = L('Query error','%s/%s'%(jid,nick))
		else:
			msg = L('Player not found','%s/%s'%(jid,nick))
	else:
		msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type,jid,nick,msg)

def wotclan(type, jid, nick, text):
	text = text.strip().upper()
	try:
		data = load_page('http://api.worldoftanks.ru/2.0/clan/list/?application_id=171745d21f7f98fd8878771da1000a31&search=%s' % text)	
		data = json.loads(data)
		claninfo = [i for i in data['data'] if i['abbreviation'] == text]
		if claninfo:
			claninfo = claninfo[0]
			clid = claninfo['clan_id']
			owner = claninfo['owner_name']
			created_at = claninfo['created_at']
			abbrev = claninfo['abbreviation']
			data = load_page('http://api.worldoftanks.ru/2.0/clan/info/?application_id=171745d21f7f98fd8878771da1000a31&clan_id=%s' % clid)	
			data = json.loads(data)
			claninfo2 = data['data'][str(clid)]
			msg = L('Name: %s [%s]','%s/%s'%(jid,nick)) % (claninfo2['name'], abbrev)
			msg += L('\nOwner: %s','%s/%s'%(jid,nick)) % owner
			msg += L('\nCreated at: %s','%s/%s'%(jid,nick)) % time.ctime(created_at)
			msg += L('\nCount of members: %s','%s/%s'%(jid,nick)) % claninfo2['members_count']
			msg += L('\nMotto: %s','%s/%s'%(jid,nick)) % claninfo2['motto']
			msg += '\n%s' % claninfo2['description']
		else:
			msg = L('Clan not found','%s/%s'%(jid,nick))
	except:
		msg = L('Impossible to get info','%s/%s'%(jid,nick))
	send_msg(type,jid,nick,msg)
		
global execute

execute = [(3, 'wot', wot, 2, 'World of Tanks - info about user. Usage: wot nick [tank]'),
			(3, 'wotclan', wotclan, 2, 'World of Tanks - info about clan. Usage: wotclan clan')]
