# Tai Sakuma <tai.sakuma@cern.ch>
from ..summary import Reader, Summarizer, NextKeyComposer, KeyValueComposer
from ..collector import CombineIntoList
from ..collector import WriteListToFile
from ..loop import Collector

##__________________________________________________________________||
def build_counter_collector_pair(tblcfg):
    keyValComposer = KeyValueComposer(
        keyAttrNames = tblcfg['keyAttrNames'],
        binnings = tblcfg['binnings'],
        keyIndices = tblcfg['keyIndices'],
        valAttrNames = tblcfg['valAttrNames'],
        valIndices = tblcfg['valIndices']
    )
    nextKeyComposer = NextKeyComposer(tblcfg['binnings']) if tblcfg['binnings'] is not None else None
    summarizer = Summarizer(
        Summary = tblcfg['summaryClass']
    )
    reader = Reader(
        keyValComposer = keyValComposer,
        summarizer = summarizer,
        nextKeyComposer = nextKeyComposer,
        weightCalculator = tblcfg['weight'],
        nevents = tblcfg['nevents']
    )
    resultsCombinationMethod = CombineIntoList(
        summaryColumnNames = tblcfg['keyOutColumnNames'] + tblcfg['valOutColumnNames']
    )
    deliveryMethod = WriteListToFile(tblcfg['outFilePath']) if tblcfg['outFile'] else None
    collector = Collector(resultsCombinationMethod, deliveryMethod)
    return reader, collector

##__________________________________________________________________||
