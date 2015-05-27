import unittest
import cStringIO

##____________________________________________________________________________||
hasPandas = False
try:
    import pandas as pd
    from AlphaTwirl.Aggregate import stack_counts_categories
    hasPandas = True
except ImportError:
    class PD:
        def read_table(self, *args, **kargs): pass
    pd = PD()

##____________________________________________________________________________||
def assertDataFrameEqual(df1, df2, **kwds):
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort(axis = 1), df2.sort(axis = 1),
                              check_less_precise = True, check_names = True)

##____________________________________________________________________________||
tbl_process_met = pd.read_table(cStringIO.StringIO(
"""   process    met_pt          n         nvar
       QCD    7.9433    26.3231     692.9077
       QCD   10.0000     0.0000       0.0000
       QCD   12.5893    26.3231     692.9077
       QCD   15.8489   212.6875    5547.6816
       QCD   19.9526  1242.0908 1016628.1773
       QCD   25.1189  1244.1932 1016632.5972
       QCD   31.6228  2255.6828 2027037.8649
       QCD   39.8107  1311.5560 1018049.3519
       QCD   50.1187  1261.0120 1016667.9564
       QCD   63.0957   401.1542   10406.8753
       QCD   79.4328  2200.9342 2025647.6296
       QCD  100.0000    93.6859    2109.6624
       QCD  125.8925    93.6859    2109.6624
       QCD  158.4893    26.3231     692.9077
       QCD  199.5262     0.0000       0.0000
       QCD  316.2278     2.1024       4.4199
       QCD  398.1072     0.0000       0.0000
         T    1.5849     0.2909       0.0423
         T    1.9953     0.4375       0.0638
         T    2.5119     1.8240       0.2418
         T    3.1623     2.3267       0.2493
         T    3.9811     5.9041       0.6021
         T    5.0119    12.0431       1.2536
         T    6.3096    19.7344       1.9705
         T    7.9433    40.0911       4.1284
         T   10.0000    63.7880       6.2705
         T   12.5893   102.8810       9.9490
         T   15.8489   172.6150      16.8659
         T   19.9526   249.2194      23.7527
         T   25.1189   355.7493      33.7162
         T   31.6228   502.7835      46.9075
         T   39.8107   668.9664      62.2640
         T   50.1187   860.8914      79.9122
         T   63.0957  1004.5319      93.0611
         T   79.4328   975.8055      91.6994
         T  100.0000   806.2589      78.9610
         T  125.8925   607.5041      61.6699
         T  158.4893   386.3233      40.1414
         T  199.5262   201.6600      21.7206
         T  251.1886    94.5197      10.4213
         T  316.2278    37.5770       4.2719
         T  398.1072    17.8687       2.1320
         T  501.1872     7.3094       0.8824
         T  630.9573     1.7342       0.2224
         T  794.3282     0.0000       0.0000
         T 1000.0000     0.0187       0.0003
         T 1258.9254     0.1444       0.0209
         T 1584.8932     0.0000       0.0000
    TTJets    1.2589     0.5087       0.0647
    TTJets    1.5849     0.8903       0.1132
    TTJets    1.9953     4.5786       0.5823
    TTJets    2.5119     7.8853       1.0029
    TTJets    3.1623    22.8928       2.9115
    TTJets    3.9811    44.7681       5.6937
    TTJets    5.0119    89.4090      11.3712
    TTJets    6.3096   179.4538      22.8233
    TTJets    7.9433   308.0349      39.1765
    TTJets   10.0000   525.1346      66.7877
    TTJets   12.5893   868.2717     110.4285
    TTJets   15.8489  1389.8451     176.7633
    TTJets   19.9526  2121.3961     269.8034
    TTJets   25.1189  3150.5530     400.6937
    TTJets   31.6228  4338.1787     551.7383
    TTJets   39.8107  5836.3829     742.2830
    TTJets   50.1187  7494.3278     953.1438
    TTJets   63.0957  8625.9934    1097.0713
    TTJets   79.4328  8389.8164    1067.0338
    TTJets  100.0000  6914.2506     879.3684
    TTJets  125.8925  4917.2385     625.3843
    TTJets  158.4893  3019.4284     384.0170
    TTJets  199.5262  1461.1942     185.8376
    TTJets  251.1886   577.5336      73.4519
    TTJets  316.2278   212.2668      26.9965
    TTJets  398.1072    62.9551       8.0068
    TTJets  501.1872    16.4065       2.0866
    TTJets  630.9573     3.5611       0.4529
    TTJets  794.3282     0.5087       0.0647
    TTJets 1000.0000     0.2544       0.0324
    TTJets 1258.9254     0.0000       0.0000
WJetsToLNu    0.6310     0.0202       0.0004
WJetsToLNu    0.7943     0.0202       0.0004
WJetsToLNu    1.0000     0.2981       0.0129
WJetsToLNu    1.2589     2.8891       1.1248
WJetsToLNu    1.5849     3.0943       0.7426
WJetsToLNu    1.9953    15.5244       5.7190
WJetsToLNu    2.5119    44.8231      24.0571
WJetsToLNu    3.1623    76.6457      31.3266
WJetsToLNu    3.9811   140.7064      55.0289
WJetsToLNu    5.0119   283.2494     120.3916
WJetsToLNu    6.3096   515.1818     223.8924
WJetsToLNu    7.9433   959.7474     425.3242
WJetsToLNu   10.0000  1541.2840     689.4449
WJetsToLNu   12.5893  2477.9011    1094.4075
WJetsToLNu   15.8489  3731.0325    1665.2434
WJetsToLNu   19.9526  5412.4631    2371.5143
WJetsToLNu   25.1189  7539.2005    3279.1717
WJetsToLNu   31.6228  9921.8442    4331.0058
WJetsToLNu   39.8107 12041.8424    5265.2648
WJetsToLNu   50.1187 14169.2429    6211.5671
WJetsToLNu   63.0957 14934.1775    6482.6438
WJetsToLNu   79.4328 12940.1846    5420.0540
WJetsToLNu  100.0000 10235.0347    4265.4833
WJetsToLNu  125.8925  7665.4247    3015.7176
WJetsToLNu  158.4893  5339.8176    1880.6610
WJetsToLNu  199.5262  3016.4575     825.4832
WJetsToLNu  251.1886  1513.6495     269.6217
WJetsToLNu  316.2278   689.1128      48.7868
WJetsToLNu  398.1072   294.7563      10.1951
WJetsToLNu  501.1872   116.7979       2.5968
WJetsToLNu  630.9573    39.2654       0.7931
WJetsToLNu  794.3282    12.2199       0.2468
WJetsToLNu 1000.0000     3.1509       0.0636
WJetsToLNu 1258.9254     0.6665       0.0135
WJetsToLNu 1584.8932     0.1212       0.0024
WJetsToLNu 1995.2623     0.0000       0.0000
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_stack_process_met = pd.read_table(cStringIO.StringIO(
"""   process    met_pt          n         nvar stack
       QCD    7.9433    26.3231     692.9077     1
       QCD   10.0000     0.0000       0.0000     1
       QCD   12.5893    26.3231     692.9077     1
       QCD   15.8489   212.6875    5547.6816     1
       QCD   19.9526  1242.0908 1016628.1773     1
       QCD   25.1189  1244.1932 1016632.5972     1
       QCD   31.6228  2255.6828 2027037.8649     1
       QCD   39.8107  1311.5560 1018049.3519     1
       QCD   50.1187  1261.0120 1016667.9564     1
       QCD   63.0957   401.1542   10406.8753     1
       QCD   79.4328  2200.9342 2025647.6296     1
       QCD  100.0000    93.6859    2109.6624     1
       QCD  125.8925    93.6859    2109.6624     1
       QCD  158.4893    26.3231     692.9077     1
       QCD  199.5262     0.0000       0.0000     1
       QCD  316.2278     2.1024       4.4199     1
       QCD  398.1072     0.0000       0.0000     1
         T    1.5849     0.2909       0.0423     2
         T    1.9953     0.4375       0.0638     2
         T    2.5119     1.8240       0.2418     2
         T    3.1623     2.3267       0.2493     2
         T    3.9811     5.9041       0.6021     2
         T    5.0119    12.0431       1.2536     2
         T    6.3096    19.7344       1.9705     2
         T    7.9433    66.4142     697.0361     2
         T   10.0000    63.7880       6.2705     2
         T   12.5893   129.2041     702.8567     2
         T   15.8489   385.3025    5564.5475     2
         T   19.9526  1491.3102 1016651.9300     2
         T   25.1189  1599.9425 1016666.3134     2
         T   31.6228  2758.4663 2027084.7724     2
         T   39.8107  1980.5224 1018111.6159     2
         T   50.1187  2121.9034 1016747.8686     2
         T   63.0957  1405.6861   10499.9364     2
         T   79.4328  3176.7397 2025739.3290     2
         T  100.0000   899.9448    2188.6234     2
         T  125.8925   701.1900    2171.3323     2
         T  158.4893   412.6464     733.0491     2
         T  199.5262   201.6600      21.7206     2
         T  251.1886    94.5197      10.4213     2
         T  316.2278    39.6794       8.6918     2
         T  398.1072    17.8687       2.1320     2
         T  501.1872     7.3094       0.8824     2
         T  630.9573     1.7342       0.2224     2
         T  794.3282     0.0000       0.0000     2
         T 1000.0000     0.0187       0.0003     2
         T 1258.9254     0.1444       0.0209     2
         T 1584.8932     0.0000       0.0000     2
    TTJets    1.2589     0.5087       0.0647     3
    TTJets    1.5849     1.1812       0.1555     3
    TTJets    1.9953     5.0161       0.6461     3
    TTJets    2.5119     9.7093       1.2447     3
    TTJets    3.1623    25.2195       3.1608     3
    TTJets    3.9811    50.6722       6.2958     3
    TTJets    5.0119   101.4521      12.6248     3
    TTJets    6.3096   199.1882      24.7938     3
    TTJets    7.9433   374.4491     736.2126     3
    TTJets   10.0000   588.9226      73.0582     3
    TTJets   12.5893   997.4758     813.2852     3
    TTJets   15.8489  1775.1476    5741.3108     3
    TTJets   19.9526  3612.7063 1016921.7334     3
    TTJets   25.1189  4750.4955 1017067.0071     3
    TTJets   31.6228  7096.6450 2027636.5107     3
    TTJets   39.8107  7816.9053 1018853.8989     3
    TTJets   50.1187  9616.2312 1017701.0124     3
    TTJets   63.0957 10031.6795   11597.0077     3
    TTJets   79.4328 11566.5561 2026806.3628     3
    TTJets  100.0000  7814.1954    3067.9918     3
    TTJets  125.8925  5618.4285    2796.7166     3
    TTJets  158.4893  3432.0748    1117.0661     3
    TTJets  199.5262  1662.8542     207.5582     3
    TTJets  251.1886   672.0533      83.8732     3
    TTJets  316.2278   251.9462      35.6883     3
    TTJets  398.1072    80.8238      10.1388     3
    TTJets  501.1872    23.7159       2.9690     3
    TTJets  630.9573     5.2953       0.6753     3
    TTJets  794.3282     0.5087       0.0647     3
    TTJets 1000.0000     0.2731       0.0327     3
    TTJets 1258.9254     0.1444       0.0209     3
    TTJets 1584.8932     0.0000       0.0000     3
WJetsToLNu    0.6310     0.0202       0.0004     4
WJetsToLNu    0.7943     0.0202       0.0004     4
WJetsToLNu    1.0000     0.2981       0.0129     4
WJetsToLNu    1.2589     3.3978       1.1895     4
WJetsToLNu    1.5849     4.2755       0.8981     4
WJetsToLNu    1.9953    20.5405       6.3651     4
WJetsToLNu    2.5119    54.5324      25.3018     4
WJetsToLNu    3.1623   101.8652      34.4874     4
WJetsToLNu    3.9811   191.3786      61.3247     4
WJetsToLNu    5.0119   384.7015     133.0164     4
WJetsToLNu    6.3096   714.3700     248.6862     4
WJetsToLNu    7.9433  1334.1965    1161.5368     4
WJetsToLNu   10.0000  2130.2066     762.5031     4
WJetsToLNu   12.5893  3475.3769    1907.6927     4
WJetsToLNu   15.8489  5506.1801    7406.5542     4
WJetsToLNu   19.9526  9025.1694 1019293.2477     4
WJetsToLNu   25.1189 12289.6960 1020346.1788     4
WJetsToLNu   31.6228 17018.4892 2031967.5165     4
WJetsToLNu   39.8107 19858.7477 1024119.1637     4
WJetsToLNu   50.1187 23785.4741 1023912.5795     4
WJetsToLNu   63.0957 24965.8570   18079.6515     4
WJetsToLNu   79.4328 24506.7407 2032226.4168     4
WJetsToLNu  100.0000 18049.2301    7333.4751     4
WJetsToLNu  125.8925 13283.8532    5812.4342     4
WJetsToLNu  158.4893  8771.8924    2997.7271     4
WJetsToLNu  199.5262  4679.3117    1033.0414     4
WJetsToLNu  251.1886  2185.7028     353.4949     4
WJetsToLNu  316.2278   941.0590      84.4751     4
WJetsToLNu  398.1072   375.5801      20.3339     4
WJetsToLNu  501.1872   140.5138       5.5658     4
WJetsToLNu  630.9573    44.5607       1.4684     4
WJetsToLNu  794.3282    12.7286       0.3115     4
WJetsToLNu 1000.0000     3.4240       0.0963     4
WJetsToLNu 1258.9254     0.8109       0.0344     4
WJetsToLNu 1584.8932     0.1212       0.0024     4
WJetsToLNu 1995.2623     0.0000       0.0000     4
"""), delim_whitespace = True)

##____________________________________________________________________________||
@unittest.skipUnless(hasPandas, "has no pandas")
class Test_combine_MC_yields_in_datasets_into_xsec_in_processes(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(pd.core.frame.DataFrame, assertDataFrameEqual)

    def test_one(self):
        expect = tbl_stack_process_met
        actual = stack_counts_categories(
            tbl_process_met,
            variables = ('n', 'nvar'),
            category = 'process',
            order = ('QCD', 'T', 'DYJetsToLL', 'GJets', 'TTJets', 'WJetsToLNu', 'ZJetsToNuNu'),
            )
        self.assertEqual(expect, actual)

##____________________________________________________________________________||
