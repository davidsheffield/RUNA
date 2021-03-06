import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

#options.register('NAME', False,
#		    VarParsing.multiplicity.singleton,
#		        VarParsing.varType.bool,
#			    "Run this on real data"
#			    )
options.register('PROC', 
		'RPVSt350tojj_pythia8_13TeV_PU20bx25',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"name"
		)

options.register('local', 
		True,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run locally or crab"
		)
options.register('debug', 
		False,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run just pruned"
		)
options.register('HT', 
		0.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"HT cut"
		)
options.register('MassRes', 
		0.15,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"MassRes cut"
		)
options.register('Delta', 
		70.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Delta cut"
		)
options.register('EtaBand', 
		1.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"EtaBand cut"
		)
options.register('JetPt', 
		80.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"JetPt cut"
		)





options.parseArguments()

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

NAME = options.PROC

if options.local:
	process.load(NAME+'_RUNA_cfi')
	#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')
else:
	process.source = cms.Source("PoolSource",
	   fileNames = cms.untracked.vstring(
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_1.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_10.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_100.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_101.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_102.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_103.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_104.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_105.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_106.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_107.root',
		#'file:RUNtuple_1.root'
	    )
	)

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )

if 'bj' in NAME: bjsample = True
else: bjsample = False

if 'JetHT' in NAME: HTtrigger = 'HLT_PFHT800'
else: HTtrigger = 'HLT_PFHT900'

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNAnalysis_'+NAME+'.root' ) )

process.AnalysisPlots = cms.EDAnalyzer('RUNAnalysis',
		cutHT	 		= cms.double( options.HT ),
		cutMassRes 		= cms.double( options.MassRes ),
		cutDelta 		= cms.double( options.Delta ),
		cutEtaBand 		= cms.double( options.EtaBand ),
		cutJetPt 		= cms.double( options.JetPt ),
		bjSample		= cms.bool( bjsample ),
		triggerPass 		= cms.vstring( ['HLT_PFHT800', 'HLT_PFHT750_4JetPt'] ) 
)



if options.debug:
	process.p = cms.Path( process.AnalysisPlots )
else:

	process.p = cms.Path( process.AnalysisPlots
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
